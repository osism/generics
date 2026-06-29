"""Local-or-remote source reads for OSISM repos.

A repo may carry a per-repo override in config.sources (owner and/or branch).
A set `branch` *pins* the repo: it is always read remotely at that ref, so the
result is deterministic regardless of any local checkout's current branch.
"""

import subprocess
from pathlib import Path

import requests


class SourceError(Exception):
    """Raised on any read/list failure that should abort the run."""


def _source(repo: str, config):
    return config.sources.get(repo)


def _owner(repo: str, config) -> str:
    s = _source(repo, config)
    if s is not None and s.owner:
        return s.owner
    return config.remote.default_owner


def _ref(repo: str, config) -> str:
    s = _source(repo, config)
    if s is not None and s.branch:
        return s.branch
    return config.remote.branch


def _is_pinned(repo: str, config) -> bool:
    s = _source(repo, config)
    return s is not None and s.branch is not None


def _local_repo_dir(repo: str, config) -> Path | None:
    """First --base-dir (in order) that contains <repo-dir> (hyphenated name)."""
    name = repo.replace("_", "-")
    for base in config.base_dirs:
        cand = Path(base).expanduser() / name
        if cand.is_dir():
            return cand
    return None


def _resolve(repo: str, config):
    """('local', dir) | ('remote', None); raise SourceError on mode-B not-found.

    A pinned (upstream) repo resolves local only if its discovered dir is a git
    checkout — it is read at named refs via git objects, so a non-git dir cannot
    serve it (it falls to --remote-fallback / mode B). Unpinned (consumer) repos
    resolve local from any discovered dir (read as the working tree).
    """
    if not config.base_dirs:
        return ("remote", None)
    d = _local_repo_dir(repo, config)
    usable = d is not None and (not _is_pinned(repo, config) or (d / ".git").exists())
    if usable:
        return ("local", d)
    if config.remote_fallback:
        return ("remote", None)
    raise SourceError(
        f"repo {repo!r} not found under any --base-dir "
        f"({', '.join(config.base_dirs)}); pass --remote-fallback to fetch it remotely"
    )


def _git(d, *args):
    return subprocess.run(
        ["git", "-C", str(d), *args], capture_output=True, check=False
    )


def _resolve_local_ref(d, ref):
    """Clone-local name that resolves `ref` to a commit, or None. Tries the ref
    as-given, then <remote>/<ref> for EVERY configured remote, so a ref held only
    under a non-origin remote (e.g. gerrit/unmaintained/2024.1) still resolves."""
    cands = [ref]
    cands += [f"{r}/{ref}" for r in _git(d, "remote").stdout.decode().split()]
    for cand in cands:
        if (
            _git(d, "rev-parse", "--verify", "--quiet", f"{cand}^{{commit}}").returncode
            == 0
        ):
            return cand
    return None


def _git_show(d, ref, rel_path, optional=False):
    rref = _resolve_local_ref(d, ref)
    if rref is None:
        raise SourceError(
            f"ref {ref!r} not found in {d} — fetch it "
            f"(this repo is read at named refs via git)"
        )
    r = _git(d, "show", f"{rref}:{rel_path}")
    if r.returncode != 0:
        if optional:
            return None
        raise SourceError(f"{rel_path} absent at {ref} in {d}")
    return r.stdout


def _git_ls_tree(d, ref, rel_path, dirs_only=False):
    rref = _resolve_local_ref(d, ref)
    if rref is None:
        raise SourceError(
            f"ref {ref!r} not found in {d} — fetch it "
            f"(this repo is read at named refs via git)"
        )
    # Colon (subtree) form lists DIRECT CHILDREN by BASENAME (not full paths).
    r = _git(d, "ls-tree", f"{rref}:{rel_path}")
    if r.returncode != 0:
        raise SourceError(f"cannot list {rel_path} at {ref} in {d}")
    out = []
    for line in r.stdout.decode().splitlines():
        meta, _, name = line.partition("\t")  # "<mode> <type> <sha>\t<basename>"
        if not dirs_only or meta.split()[1] == "tree":
            out.append(name)
    return out


def _git_ref_exists(d, ref):
    return _resolve_local_ref(d, ref) is not None


def _remote_url(repo: str, rel_path: str, config) -> str:
    owner = _owner(repo, config)
    return (
        f"{config.remote.github_raw}{owner}/{repo.replace('_', '-')}/"
        f"{_ref(repo, config)}/{rel_path}"
    )


def read(repo: str, rel_path: str, config) -> bytes:
    """Read `rel_path` from `repo`; raise SourceError if it is absent."""
    where, d = _resolve(repo, config)
    if where == "local":
        if _is_pinned(repo, config):
            return _git_show(d, _ref(repo, config), rel_path)
        p = d / rel_path
        if not p.exists():
            raise SourceError(f"{rel_path} not found in local {repo} ({d})")
        return p.read_bytes()
    url = _remote_url(repo, rel_path, config)
    try:
        r = requests.get(url, timeout=30)
    except requests.RequestException as e:
        raise SourceError(f"network error fetching {url}: {e}") from e
    if r.status_code == 404:
        raise SourceError(f"404 not found: {url}")
    if not r.ok:
        raise SourceError(f"HTTP {r.status_code} fetching {url}")
    return r.content


def read_optional(repo: str, rel_path: str, config) -> bytes | None:
    """Like read(), but return None instead of raising when absent."""
    where, d = _resolve(repo, config)
    if where == "local":
        if _is_pinned(repo, config):
            return _git_show(d, _ref(repo, config), rel_path, optional=True)
        p = d / rel_path
        return p.read_bytes() if p.exists() else None
    url = _remote_url(repo, rel_path, config)
    try:
        r = requests.get(url, timeout=30)
    except requests.RequestException as e:
        raise SourceError(f"network error fetching {url}: {e}") from e
    if r.status_code == 404:
        return None
    if not r.ok:
        raise SourceError(f"HTTP {r.status_code} fetching {url}")
    return r.content


def list_dir(repo: str, rel_path: str, config, dirs_only: bool = False) -> list[str]:
    """List entries under `rel_path` in `repo` (directories only if `dirs_only`)."""
    where, d = _resolve(repo, config)
    if where == "local":
        if _is_pinned(repo, config):
            return _git_ls_tree(d, _ref(repo, config), rel_path, dirs_only)
        p = d / rel_path
        if not p.is_dir():
            raise SourceError(f"{rel_path} not a directory in local {repo} ({d})")
        return [x.name for x in p.iterdir() if (not dirs_only or x.is_dir())]
    owner = _owner(repo, config)
    url = (
        f"{config.remote.github_api}{owner}/{repo.replace('_', '-')}/"
        f"contents/{rel_path}?ref={_ref(repo, config)}"
    )
    try:
        r = requests.get(
            url, timeout=30, headers={"Accept": "application/vnd.github.v3+json"}
        )
    except requests.RequestException as e:
        raise SourceError(f"network error listing {url}: {e}") from e
    if r.status_code == 404:
        raise SourceError(f"404 not found: {url}")
    if not r.ok:
        raise SourceError(f"HTTP {r.status_code} listing {url}")
    items = r.json()
    if dirs_only:
        items = [it for it in items if it.get("type") == "dir"]
    return [item["name"] for item in items]


def list_dir_at_ref(
    repo: str, rel_path: str, ref: str, config, dirs_only: bool = False
) -> list[str]:
    """List a repo directory at an explicit git ref.

    Local (the repo resolves under a --base-dir): list the git tree at `ref`
    (objects, never the working tree). Remote: the GitHub contents API at `ref`.
    Either way the explicit ref is read, ignoring any per-repo pin, so a range
    check is deterministic.
    """
    where, d = _resolve(repo, config)
    if where == "local" and _is_pinned(repo, config):
        return _git_ls_tree(d, ref, rel_path, dirs_only)
    owner = _owner(repo, config)
    url = (
        f"{config.remote.github_api}{owner}/{repo.replace('_', '-')}/"
        f"contents/{rel_path}?ref={ref}"
    )
    try:
        r = requests.get(
            url, timeout=30, headers={"Accept": "application/vnd.github.v3+json"}
        )
    except requests.RequestException as e:
        raise SourceError(f"network error listing {url}: {e}") from e
    if r.status_code == 404:
        raise SourceError(f"404 not found: {url}")
    if not r.ok:
        raise SourceError(f"HTTP {r.status_code} listing {url}")
    items = r.json()
    if dirs_only:
        items = [it for it in items if it.get("type") == "dir"]
    return [item["name"] for item in items]


def ref_exists(repo: str, ref: str, config) -> bool:
    """True if `ref` (branch/tag/sha) resolves in the upstream repo (local clone
    when it resolves under a --base-dir, else the GitHub commits API)."""
    where, d = _resolve(repo, config)
    if where == "local" and _is_pinned(repo, config):
        return _git_ref_exists(d, ref)
    owner = _owner(repo, config)
    url = f"{config.remote.github_api}{owner}/{repo.replace('_', '-')}/commits/{ref}"
    try:
        r = requests.get(
            url, timeout=30, headers={"Accept": "application/vnd.github.v3+json"}
        )
    except requests.RequestException as e:
        raise SourceError(f"network error checking ref {url}: {e}") from e
    # GitHub's commits API returns 422 (not 404) for a ref that does not
    # resolve; treat both as "absent" so the resolver probes the next candidate.
    if r.status_code in (404, 422):
        return False
    if not r.ok:
        raise SourceError(f"HTTP {r.status_code} checking ref {url}")
    return True


_REF_CANDIDATES = ("stable/{r}", "unmaintained/{r}", "{r}-eol", "{r}-eom")


def release_to_ref(repo: str, release: str, config) -> str:
    """Resolve an OSISM release (e.g. '2024.2') to an existing upstream ref.

    OSISM builds releases upstream has moved past EOL, so ref naming is
    non-uniform: a release_refs override wins, else probe stable/ ->
    unmaintained/ -> <r>-eol -> <r>-eom and take the first that exists. None
    exists -> SourceError (loud, never a silent 404 mid-listing). Each
    (repo, release) is resolved once per run, so no caching is needed.
    """
    override = (config.release_refs.get(repo) or {}).get(release)
    if override:
        return override
    for tmpl in _REF_CANDIDATES:
        cand = tmpl.format(r=release)
        if ref_exists(repo, cand, config):
            return cand
    tried = ", ".join(t.format(r=release) for t in _REF_CANDIDATES)
    raise SourceError(
        f"no upstream ref for {repo} release {release}: tried {tried} "
        f"(set release_refs to override)"
    )


def read_at_ref(
    repo: str, rel_path: str, ref: str, config, optional: bool = False
) -> bytes | None:
    """Read a repo file at an explicit git ref. Always remote.

    Local (the repo resolves under a --base-dir): read the git object at `ref`.
    Remote: github_raw at `ref`. The explicit ref is read either way, ignoring
    any per-repo pin. optional=True maps an absent path (local) or a 404 (remote)
    to None so the caller can probe an alternative (e.g. monolithic all.yml ->
    split all/ dir).
    """
    where, d = _resolve(repo, config)
    if where == "local" and _is_pinned(repo, config):
        return _git_show(d, ref, rel_path, optional=optional)
    owner = _owner(repo, config)
    url = (
        f"{config.remote.github_raw}{owner}/{repo.replace('_', '-')}/"
        f"{ref}/{rel_path}"
    )
    try:
        r = requests.get(url, timeout=30)
    except requests.RequestException as e:
        raise SourceError(f"network error fetching {url}: {e}") from e
    if r.status_code == 404:
        if optional:
            return None
        raise SourceError(f"404 not found: {url}")
    if not r.ok:
        raise SourceError(f"HTTP {r.status_code} fetching {url}")
    return r.content


def describe_resolution(repos, config) -> list[str]:
    """One human log line per repo (sorted). Raises SourceError on a mode-B
    not-found, so the driver can abort before any comparison runs."""
    lines = []
    for repo in sorted(repos):
        where, d = _resolve(repo, config)
        if where == "local" and _is_pinned(repo, config):
            lines.append(
                f"  {repo:<32} local  {d} @ {_ref(repo, config)} "
                f"(+per-release range refs)  [git refs, must be current]"
            )
        elif where == "local":
            lines.append(f"  {repo:<32} local  {d}  [working tree, as-is]")
        elif _is_pinned(repo, config):
            owner = _owner(repo, config)
            lines.append(
                f"  {repo:<32} remote {owner}/{repo.replace('_', '-')} "
                f"@ {_ref(repo, config)} (+per-release range refs)  [remote]"
            )
        else:
            owner = _owner(repo, config)
            tail = ", not found locally" if config.base_dirs else ""
            lines.append(
                f"  {repo:<32} remote {owner}/{repo.replace('_', '-')} "
                f"@ {config.remote.branch}  [remote{tail}]"
            )
    return lines

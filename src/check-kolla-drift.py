#!/usr/bin/env python3
"""Drift detector for the OSISM kolla container-image toolchain.

Catches divergence between the OSISM consumer repos (`defaults`, `release`,
`generics`, the container-image repos) and upstream `openstack/kolla` /
`openstack/kolla-ansible` *when it is introduced* — before it breaks a deploy or
a CI gate.

Each check is a plugin (see `osism_drift.drift`) that compares one
authoritative source against one consumer and emits `DriftEntry` items. The
plugins run in the order a service travels from upstream definition to a
deployed container:

- `kolla_enablement_orphan`   — the OSISM enable flag still exists upstream
- `kolla_enablement_build`    — the enabled service is actually built
- `kolla_version_chain_upstream` — the built image has a version-pin line
- `kolla_version_chain_inner` — that pin line resolves to a real version
- `kolla_inventory`           — the service is present in the deploy inventory

Sources resolve remotely (GitHub) by default. A repeatable `--base-dir DIR`
reads local checkouts instead, with pinned upstream repos read from git objects
at the release refs (fully offline). An allowlist marks known or
intentional drift as expected; allowlist entries that match nothing are
reported as stale.

Findings print two ways:

- text (default) — grouped, narrated blocks per check (`osism_drift.report`)
- `--format json` — one JSON object per entry, for machines

Exit codes:

- 0 — no actionable drift and no stale allowlist entries
- 1 — actionable drift or stale allowlist entries found
- 2 — input error (missing file, unparseable, bad config)

Run with `-h` for the per-plugin reference and the inputs each one reads.
"""

import argparse
import dataclasses
import json
import sys
from pathlib import Path

from osism_drift.config import (
    Allowlist,
    ConfigError,
    load_allowlist,
    load_config,
    to_remote_only,
)
from osism_drift.drift import PLUGINS
from osism_drift import report, source
from osism_drift.source import SourceError


def _build_parser():
    p = argparse.ArgumentParser(
        description="Check OSISM container image versions for drift across repos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_format_plugin_help() + "\n" + _exit_codes_help(),
    )
    here = Path(__file__).resolve().parent
    p.add_argument(
        "--config",
        default=here / "kolla-drift-config.yml",
        help="config file (default: alongside script)",
    )
    p.add_argument(
        "--allowlist",
        default=here / "kolla-drift-allowlist.yml",
        help="allowlist (default: alongside script)",
    )
    p.add_argument(
        "--plugin",
        action="append",
        help="run only this plugin (repeatable); default: all enabled",
    )
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument(
        "--no-allowlist",
        action="store_true",
        help="ignore allowlist; report everything",
    )
    p.add_argument(
        "--base-dir",
        action="append",
        metavar="DIR",
        help="local checkout root (repeatable); repos found by dir name, first match wins",
    )
    p.add_argument(
        "--remote-fallback",
        action="store_true",
        help="for repos not found under any --base-dir, fetch remotely instead of erroring",
    )
    p.add_argument(
        "--remote-only",
        action="store_true",
        help="ignore --base-dir; HTTP fetch everywhere",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-q", "--quiet", action="store_true")
    return p


def _format_plugin_help() -> str:
    lines = ["Plugins:"]
    for plugin in PLUGINS:
        lines.append(f"  {plugin.NAME}")
        lines.append(f"    {plugin.DESCRIPTION}")
        lines.append("    Reads:")
        col_w = max(len(repo) for repo, _ in plugin.INPUT_FILES) + 4
        for repo, rel in plugin.INPUT_FILES:
            lines.append(f"      {repo:<{col_w}}{rel}")
        lines.append("")
    return "\n".join(lines)


def _exit_codes_help() -> str:
    return (
        "Exit codes:\n"
        "  0   no actionable drift and no stale allowlist entries\n"
        "  1   actionable drift or stale allowlist entries found\n"
        "  2   input error (missing file, unparseable, bad config)"
    )


def _format_stale_text(stale) -> list[str]:
    out = []
    if stale:
        out.append("STALE ALLOWLIST (entries that matched no drift):")
        for e in stale:
            extra = []
            if e.alias is not None:
                extra.append(f"alias={e.alias}")
            if e.found_src is not None:
                extra.append(f"found_src={e.found_src}")
            suffix = (" " + " ".join(extra)) if extra else ""
            out.append(f"  {e.plugin}: {e.image}{suffix} -- {e.reason}")
        out.append("")
    return out


def _load_runtime(args):
    """Build the resolved config and allowlist from parsed CLI args.

    Raises ConfigError on invalid config or allowlist input.
    """
    config = load_config(args.config)
    config = dataclasses.replace(
        config,
        base_dirs=tuple(args.base_dir or ()),
        remote_fallback=args.remote_fallback,
    )
    if args.remote_only:
        config = to_remote_only(config)
    allowlist = (
        Allowlist(entries=()) if args.no_allowlist else load_allowlist(args.allowlist)
    )
    return config, allowlist


def _emit(args, drifts, actionable, allowlisted, stale):
    """Print the findings and stale-allowlist report in the chosen format."""
    if args.format == "json":
        for d in drifts if args.verbose else actionable:
            print(json.dumps(d.to_dict()))
        for e in stale:
            print(
                json.dumps(
                    {
                        "type": "stale_allowlist",
                        "plugin": e.plugin,
                        "image": e.image,
                        "alias": e.alias,
                        "found_src": e.found_src,
                        "reason": e.reason,
                    }
                )
            )
        return
    for line in report.format_text(drifts, PLUGINS):
        print(line)
    for line in _format_stale_text(stale):
        print(line)
    if not args.quiet:
        plural = "entry" if len(stale) == 1 else "entries"
        print(
            f"Summary: {len(actionable)} to act on, {len(allowlisted)} "
            f"allowlisted, {len(stale)} stale allowlist {plural} "
            f"({len(drifts)} total)"
        )


def main(argv=None) -> int:
    """CLI entry point: run the configured plugins and report drift."""
    args = _build_parser().parse_args(argv)
    try:
        config, allowlist = _load_runtime(args)
    except ConfigError as e:
        print(f"config error: {e}", file=sys.stderr)
        return 2

    selected = [
        p
        for p in PLUGINS
        if (args.plugin is None or p.NAME in args.plugin)
        and config.plugins.get(p.NAME) is not None
        and config.plugins[p.NAME].enabled
    ]

    repos = {repo for p in selected for repo, _ in p.INPUT_FILES}
    try:
        resolution = source.describe_resolution(repos, config)
    except SourceError as e:
        print(f"source error: {e}", file=sys.stderr)
        return 2
    if not args.quiet:
        print(
            f"Resolving sources ({len(config.base_dirs)} base dir(s)):", file=sys.stderr
        )
        for line in resolution:
            print(line, file=sys.stderr)

    drifts = []
    try:
        for plugin in selected:
            drifts.extend(plugin.run(config, allowlist, verbose=args.verbose))
    except SourceError as e:
        print(f"source error: {e}", file=sys.stderr)
        return 2

    actionable = [d for d in drifts if not d.allowlisted]
    allowlisted = [d for d in drifts if d.allowlisted]
    ran = {p.NAME for p in selected}
    stale = allowlist.stale(drifts, ran)

    _emit(args, drifts, actionable, allowlisted, stale)
    return 1 if (actionable or stale) else 0


if __name__ == "__main__":
    sys.exit(main())

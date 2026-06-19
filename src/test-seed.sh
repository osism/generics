#!/usr/bin/env bash
#
# Command-assembly tests for the seed-container path of
# environments/manager/run.sh (the SEED_CONTAINER flag).
#
# No container engine and no image are needed: CONTAINER_ENGINE is pointed at a
# recording stub that prints its run argv (one element per line), so each test
# can assert exactly what run.sh would have executed. The stub also answers an
# `info` subcommand with ${STUB_INFO_RC:-0}, which is how the `auto` mode probes
# whether the engine daemon is up. stdin is redirected from /dev/null so
# `[[ -t 0 ]]` is reliably false (no `-t` in CI).

# The `cond && ok || ko` assertion idiom below is deliberate: `ok` is an
# assignment that always returns 0, so the `ko` branch runs only when `cond`
# fails. SC2015's "C may run when A is true" caveat cannot occur here.
# shellcheck disable=SC2015

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
RUN_SH="$REPO_ROOT/environments/manager/run.sh"

pass=0
fail=0
ok() { pass=$((pass + 1)); }
ko() { fail=$((fail + 1)); echo "FAIL: $1"; }

# Optional static check (tier 1).
if command -v shellcheck >/dev/null 2>&1; then
    if shellcheck "$RUN_SH"; then ok; else ko "shellcheck reported issues"; fi
fi

# make_repo [--with-vault] -> prints path to a throwaway config-repo root
make_repo() {
    local tmp
    tmp="$(mktemp -d)"
    mkdir -p "$tmp/environments/manager"
    cp "$RUN_SH" "$tmp/environments/manager/run.sh"
    chmod +x "$tmp/environments/manager/run.sh"
    cat > "$tmp/engine-stub" <<'STUB'
#!/usr/bin/env bash
if [[ ${1:-} == info ]]; then
    exit "${STUB_INFO_RC:-0}"
fi
printf '%s\n' "$@"
STUB
    chmod +x "$tmp/engine-stub"
    if [[ ${1:-} == --with-vault ]]; then
        printf '#!/usr/bin/env bash\ncat /opt/configuration/secrets/vaultpass\n' \
            > "$tmp/environments/.vault_pass"
        chmod +x "$tmp/environments/.vault_pass"
    fi
    echo "$tmp"
}

# run_run <repo> [VAR=val ...] -- <run.sh args ...>
# Forces SEED_CONTAINER=true and CONTAINER_ENGINE=<stub> by default; a caller
# VAR=val pair (e.g. SEED_CONTAINER=auto) appears later in the env list and
# therefore wins. Captures recorded argv into global $OUT, exit code into $RC.
run_run() {
    local repo=$1; shift
    local -a envs=()
    while [[ ${1:-} != "--" ]]; do envs+=("$1"); shift; done
    shift
    OUT=$(cd "$repo/environments/manager" \
          && env SEED_CONTAINER=true CONTAINER_ENGINE="$repo/engine-stub" \
                 "${envs[@]}" \
                 ./run.sh "$@" </dev/null 2>"$repo/stderr.txt")
    RC=$?
}

# Assertions operate on $OUT (one argv element per line).
has()    { grep -qxF -- "$2" <<<"$1" && ok || ko "missing line '$2'"; }
absent() { grep -qxF -- "$2" <<<"$1" && ko "unexpected line '$2'" || ok; }
count()  { local n; n=$(grep -cE -- "$2" <<<"$1"); [[ $n -eq $3 ]] && ok || ko "count /$2/ = $n want $3"; }
before() {
    local i j
    i=$(grep -nxF -- "$2" <<<"$1" | head -1 | cut -d: -f1)
    j=$(grep -nxF -- "$3" <<<"$1" | head -1 | cut -d: -f1)
    [[ -n $i && -n $j && $i -lt $j ]] && ok || ko "'$2'($i) not before '$3'($j)"
}

IMG="registry.osism.tech/osism/seed:latest"

# --- Usage / mode-decision guards ------------------------------------------

# usage guard: no playbook -> non-zero, usage text (run.sh prints it to stdout)
repo=$(make_repo)
run_run "$repo" --
[[ $RC -ne 0 ]] && ok || ko "usage guard should exit non-zero"
grep -q "PLAYBOOK" <<<"$OUT" && ok || ko "usage text missing"

# invalid SEED_CONTAINER value -> non-zero, error names value + accepted set
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER=flase -- manager
[[ $RC -ne 0 ]] && ok || ko "invalid SEED_CONTAINER should exit non-zero"
grep -q "invalid SEED_CONTAINER" "$repo/stderr.txt" && ok || ko "invalid-value error text missing"

# forced container with a missing engine command -> non-zero error
repo=$(make_repo)
run_run "$repo" CONTAINER_ENGINE=definitely-not-an-engine-xyz -- operator
[[ $RC -ne 0 ]] && ok || ko "forced container, missing engine should exit non-zero"
grep -q "not found on PATH" "$repo/stderr.txt" && ok || ko "missing-engine error text missing"

# auto, engine up (info exits 0) -> container branch taken
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER=auto STUB_INFO_RC=0 -- manager
has "$OUT" "run"
has "$OUT" "$IMG"

# auto, daemon down (info exits non-zero) -> local fallback, no error
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER=auto STUB_INFO_RC=1 \
        INSTALL_ANSIBLE=false INSTALL_ANSIBLE_ROLES=false -- manager
absent "$OUT" "run"
absent "$OUT" "$IMG"
grep -q "not found on PATH" "$repo/stderr.txt" && ko "auto fallback must not emit forced-engine error" || ok

# auto, engine command missing -> local fallback, no hard error
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER=auto CONTAINER_ENGINE=definitely-not-an-engine-xyz \
        INSTALL_ANSIBLE=false INSTALL_ANSIBLE_ROLES=false -- manager
absent "$OUT" "run"
grep -q "not found on PATH" "$repo/stderr.txt" && ko "auto missing-engine must not hard error" || ok

# override: SEED_CONTAINER=false -> local path, engine never run
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER=false \
        INSTALL_ANSIBLE=false INSTALL_ANSIBLE_ROLES=false -- manager
absent "$OUT" "run"
absent "$OUT" "$IMG"

# --- Base / image assembly --------------------------------------------------

# base assembly: fixed flags, image, playbook+args; order and TTY-absence
repo=$(make_repo)
run_run "$repo" -- network
has "$OUT" "run"
has "$OUT" "--rm"
has "$OUT" "-i"
absent "$OUT" "-t"
has "$OUT" "--pull"
has "$OUT" "always"
has "$OUT" "$IMG"
has "$OUT" "network"
before "$OUT" "$IMG" "network"          # image precedes entrypoint args
before "$OUT" "--rm" "$IMG"             # engine flags precede image

# image assembly: tag override swaps only the tag
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER_TAG=dev -- manager
has "$OUT" "registry.osism.tech/osism/seed:dev"
absent "$OUT" "$IMG"

# image assembly: empty registry drops the registry segment
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER_REGISTRY= -- manager
has "$OUT" "osism/seed:latest"
absent "$OUT" "$IMG"

# playbook args with spaces and globs survive as single argv elements
repo=$(make_repo)
run_run "$repo" -- manager --limit 'a b' --tags '*'
has "$OUT" "a b"
has "$OUT" "*"

# --- Env forwarding ---------------------------------------------------------

# env forwarding: only set vars forwarded, as -e VAR=value
repo=$(make_repo)
run_run "$repo" ANSIBLE_USER=osism -- operator
has "$OUT" "-e"
has "$OUT" "ANSIBLE_USER=osism"
absent "$OUT" "ANSIBLE_ASK_PASS="     # unset -> not forwarded

# explicitly empty var is still forwarded as VAR=
repo=$(make_repo)
run_run "$repo" ANSIBLE_ASK_VAULT_PASS= -- manager
has "$OUT" "ANSIBLE_ASK_VAULT_PASS="

# --- Vault defaulting -------------------------------------------------------

# vault case 1: caller-set ANSIBLE_VAULT_PASSWORD_FILE wins (count == 1)
repo=$(make_repo --with-vault)
run_run "$repo" ANSIBLE_VAULT_PASSWORD_FILE=/caller/path -- manager
count "$OUT" "^ANSIBLE_VAULT_PASSWORD_FILE=" 1
has "$OUT" "ANSIBLE_VAULT_PASSWORD_FILE=/caller/path"

# vault case 2: no caller var, .vault_pass present -> default (count == 1)
repo=$(make_repo --with-vault)
run_run "$repo" -- manager
count "$OUT" "^ANSIBLE_VAULT_PASSWORD_FILE=" 1
has "$OUT" "ANSIBLE_VAULT_PASSWORD_FILE=/opt/configuration/environments/.vault_pass"

# vault case 3: no caller var, no .vault_pass -> none (count == 0)
repo=$(make_repo)
run_run "$repo" -- manager
count "$OUT" "^ANSIBLE_VAULT_PASSWORD_FILE=" 0

# --- Pull / mount knobs -----------------------------------------------------

# SEED_CONTAINER_PULL is honored
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER_PULL=never -- manager
before "$OUT" "--pull" "never"
absent "$OUT" "always"

# SEED_CONTAINER_MOUNT_OPTS appended verbatim -> valid :z spec
repo=$(make_repo)
run_run "$repo" SEED_CONTAINER_MOUNT_OPTS=:z -- manager
has "$OUT" "$repo:/opt/configuration:z"

# empty SEED_CONTAINER_MOUNT_OPTS -> no trailing separator
repo=$(make_repo)
run_run "$repo" -- manager
has "$OUT" "$repo:/opt/configuration"

echo "PASS=$pass FAIL=$fail"
[[ $fail -eq 0 ]]

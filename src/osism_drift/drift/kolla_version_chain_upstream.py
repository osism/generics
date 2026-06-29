"""kolla_version_chain_upstream: upstream services with no template pin.

Compares the top-level docker/ service dirs of openstack/kolla (pinned to
stable/2025.2) against the versions['K'] keys in the kolla-ansible template. A
service present upstream but absent from the template key space has no version
pin wired (e.g. valkey, blazar, masakari) and its line would silently default.

The comparison is one-way (upstream -> template): producer keys are not folded
in, so a service present in the producer yet absent from the template still
flags here. Hyphen/underscore is normalised on the key space only.
"""

from osism_drift import kolla_docker, source, versions_template
from osism_drift.model import DriftEntry

NAME = "kolla_version_chain_upstream"
DESCRIPTION = (
    "Flag openstack/kolla docker/ services (stable/2025.2) with no "
    "versions['K'] line in the kolla-ansible template (unwired pins)."
)
INPUT_FILES = [
    ("kolla", "docker"),
    ("container_image_kolla_ansible", "files/src/templates/versions.yml.j2"),
]
SUMMARY = (
    "{n} services that ship a docker/ image in openstack/kolla but have no "
    "versions['<key>'] line in the kolla-ansible template, so their image tag "
    "is never pinned:"
)
REMEDIATION = (
    "add a versions['<name>'] line to the template to pin the image, or "
    "allowlist the name if it is intentionally unpinned."
)

_DOCKER = "docker"
_TEMPLATE = "files/src/templates/versions.yml.j2"
_EXPECTED_SRC = "openstack/kolla/docker/ @ stable/2025.2"
_FOUND_SRC = "container-image-kolla-ansible/files/src/templates/versions.yml.j2"


def _norm(key: str) -> str:
    return key.replace("-", "_")


def run(config, allowlist, verbose: bool = False) -> list[DriftEntry]:
    """Return unwired-pin drifts: upstream services with no template key."""
    docker_names = source.list_dir("kolla", _DOCKER, config, dirs_only=True)
    upstream = kolla_docker.parse(docker_names)
    template_bytes = source.read("container_image_kolla_ansible", _TEMPLATE, config)
    template_keys = {
        _norm(k) for k in versions_template.parse_versions_keys(template_bytes)
    }

    drifts = []
    for service in sorted(upstream):
        if service in template_keys:
            continue
        d = DriftEntry(
            plugin=NAME,
            image=service,
            alias=service,
            expected="present in openstack/kolla docker/ at stable/2025.2",
            found="absent (no versions['...'] template key)",
            expected_src=_EXPECTED_SRC,
            found_src=_FOUND_SRC,
        )
        drifts.append(allowlist.apply(d))
    return drifts

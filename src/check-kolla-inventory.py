#!/usr/bin/env python3

from configparser import ConfigParser
import io
import sys

import requests

# kolla-ansible inventory groups that exist upstream but that this inventory
# does not mirror, by design. There are two kinds, matched differently.
#
# Host-role groups: the physical node groups (control, compute, ...) that
# services map onto. OSISM populates these from the operator's environment
# inventory, not from 50-/51-kolla, so upstream's definitions of them are not
# drift. Matched by exact name.
IGNORE_ROLE_GROUPS = [
    "baremetal:children",
    "compute",
    "control",
    "deployment",
    "monitoring",
    "network",
    "storage",
]

# Services OSISM deliberately does not deploy; the whole group family is absent
# on purpose. Matched by name prefix so newly added sub-groups stay covered.
IGNORE_NOT_DEPLOYED = [
    "collectd",
    "cyborg",
    "tacker",
    "telegraf",
]

# kolla-ansible release tracked by this check. Pin to the stable branch OSISM
# currently deploys -- NOT master -- so the check flags groups that exist in
# what OSISM ships rather than not-yet-released groups. Bump this whenever OSISM
# moves to a new OpenStack release (see the OSISM developer guide, releases.md).
KOLLA_BRANCH = "stable/2025.2"
KOLLA_INVENTORY_URL = (
    "https://raw.githubusercontent.com/openstack/kolla-ansible/"
    f"{KOLLA_BRANCH}/ansible/inventory/multinode"
)

LOCAL_INVENTORY_FILES = ["inventory/50-kolla", "inventory/51-kolla"]


def local_sections():
    sections = []
    for path in LOCAL_INVENTORY_FILES:
        config = ConfigParser(allow_no_value=True)
        config.read(path)
        sections += config.sections()
    return sections


def missing_sections(local, upstream_config):
    return [
        section
        for section in upstream_config.sections()
        if section not in local
        and section not in IGNORE_ROLE_GROUPS
        and not any(section.startswith(p) for p in IGNORE_NOT_DEPLOYED)
    ]


def stale_ignores(local, upstream_config):
    """IGNORE entries that no longer suppress any unshipped upstream group.

    An entry goes stale when the service is now shipped in the inventory, or
    when kolla-ansible removed it from the tracked release. Besides being dead
    weight, a stale prefix can silently hide a future upstream group that OSISM
    actually needs -- exactly the drift this check exists to catch -- so it is
    treated as an error.
    """
    sections = upstream_config.sections()
    stale = []
    for name in IGNORE_ROLE_GROUPS:
        if name not in sections or name in local:
            stale.append(name)
    for prefix in IGNORE_NOT_DEPLOYED:
        if not any(s.startswith(prefix) and s not in local for s in sections):
            stale.append(prefix)
    return stale


def main():
    local = local_sections()

    response = requests.get(KOLLA_INVENTORY_URL)
    if response.status_code != 200:
        print(
            "ERROR: failed to fetch upstream kolla-ansible inventory "
            f"(HTTP {response.status_code}): {KOLLA_INVENTORY_URL}",
            file=sys.stderr,
        )
        return 2

    upstream_config = ConfigParser(allow_no_value=True)
    upstream_config.read_file(io.StringIO(response.text))

    stale = stale_ignores(local, upstream_config)
    if stale:
        print(
            "ERROR: these IGNORE entries no longer suppress any upstream group "
            "absent\nfrom "
            + " and ".join(LOCAL_INVENTORY_FILES)
            + ": "
            + ", ".join(stale)
            + "\n\n"
            "They are stale -- the service is now shipped in the inventory, or "
            "kolla-\nansible removed it from "
            + KOLLA_BRANCH
            + ". Remove them from IGNORE_ROLE_GROUPS\n"
            "/ IGNORE_NOT_DEPLOYED in src/check-kolla-inventory.py.",
            file=sys.stderr,
        )
        return 3

    missing = missing_sections(local, upstream_config)
    if not missing:
        return 0

    for section in missing:
        print(f"[{section}]")
        for member in upstream_config[section]:
            print(member)
        print()
    sys.stdout.flush()

    print(
        "The kolla-ansible inventory groups listed above exist upstream\n"
        f"({KOLLA_INVENTORY_URL})\n"
        "but are missing from " + " and ".join(LOCAL_INVENTORY_FILES) + ".\n"
        "\n"
        "Resolve each group, depending on whether OSISM deploys the service:\n"
        "  * OSISM deploys it -> add the group to inventory/51-kolla, mapped to\n"
        "    the same host group(s) kolla-ansible uses upstream (e.g. control,\n"
        "    compute, network, storage), keeping the section alphabetically\n"
        "    sorted.\n"
        "  * OSISM intentionally does not deploy it -> add the service's name\n"
        "    prefix to IGNORE_NOT_DEPLOYED in src/check-kolla-inventory.py.\n"
        "\n"
        "Leaving a required group undefined makes Ansible abort haproxy-config\n"
        "templating with \"'dict object' has no attribute '<group>'\".",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3

from configparser import ConfigParser
import io
import sys

import requests

# Group name prefixes that exist in the upstream kolla-ansible inventory but
# that OSISM intentionally does not mirror. A group belongs here only if OSISM
# deliberately never deploys the corresponding service; otherwise the group
# must be defined in inventory/ instead (see the message printed on drift).
IGNORE = [
    "baremetal",
    "blazar",
    "collectd",
    "compute",
    "control",
    "cyborg",
    "deployment",
    "freezer",
    "masakari",
    "monitoring",
    "murano",
    "network",
    "sahara",
    "solum",
    "storage",
    "tacker",
    "telegraf",
    "venus",
    "vitrage",
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
        and not any(section.startswith(prefix) for prefix in IGNORE)
    ]


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
        "  * OSISM intentionally does not deploy it -> add the group's name\n"
        "    prefix to the IGNORE list in src/check-kolla-inventory.py.\n"
        "\n"
        "Leaving a required group undefined makes Ansible abort haproxy-config\n"
        "templating with \"'dict object' has no attribute '<group>'\".",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())

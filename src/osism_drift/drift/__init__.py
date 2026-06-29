"""Plugin registry. Plugins are appended here as they are added."""

from osism_drift.drift import (
    kolla_enablement_build,
    kolla_enablement_orphan,
    kolla_inventory,
    kolla_orphan_config,
    kolla_secrets_orphan,
    kolla_version_chain_inner,
    kolla_version_chain_upstream,
)

PLUGINS = [
    kolla_enablement_orphan,
    kolla_orphan_config,
    kolla_secrets_orphan,
    kolla_enablement_build,
    kolla_version_chain_upstream,
    kolla_version_chain_inner,
    kolla_inventory,
]

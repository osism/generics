"""Plugin registry. Plugins are appended here as they are added."""

from osism_drift.drift import kolla_enablement_orphan
from osism_drift.drift import kolla_orphan_config
from osism_drift.drift import kolla_secrets_orphan

PLUGINS = [kolla_enablement_orphan, kolla_orphan_config, kolla_secrets_orphan]

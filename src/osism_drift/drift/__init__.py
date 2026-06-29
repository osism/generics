"""Plugin registry. Plugins are appended here as they are added."""

from osism_drift.drift import kolla_enablement_orphan

PLUGINS = [kolla_enablement_orphan]

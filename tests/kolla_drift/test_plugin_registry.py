from pathlib import Path

from osism_drift.config import load_config
from osism_drift.drift import PLUGINS


def test_registry_is_a_list():
    assert isinstance(PLUGINS, list)


def test_each_plugin_has_required_metadata():
    for p in PLUGINS:
        assert isinstance(p.NAME, str) and p.NAME
        assert isinstance(p.DESCRIPTION, str) and p.DESCRIPTION
        assert isinstance(p.INPUT_FILES, list) and p.INPUT_FILES
        assert callable(p.run)


def test_every_plugin_has_summary_and_remediation():
    for p in PLUGINS:
        assert isinstance(p.SUMMARY, str) and p.SUMMARY.strip(), p.NAME
        assert "{n}" in p.SUMMARY, p.NAME
        assert isinstance(p.REMEDIATION, str) and p.REMEDIATION.strip(), p.NAME


def test_kolla_enablement_orphan_plugin_registered():
    assert "kolla_enablement_orphan" in [p.NAME for p in PLUGINS]


def test_default_config_enables_every_registered_plugin():
    # The driver only runs a plugin that is present and enabled in the config, so
    # a plugin registered in PLUGINS but missing from the default config would
    # silently never run. Guard against that gap.
    cfg_path = Path(__file__).resolve().parents[2] / "src" / "kolla-drift-config.yml"
    config = load_config(cfg_path)
    for p in PLUGINS:
        entry = config.plugins.get(p.NAME)
        assert entry is not None, f"{p.NAME} missing from default config"
        assert entry.enabled, f"{p.NAME} not enabled in default config"



from osism_drift.inventory_sections import parse_groups

SAMPLE = b"""\
[control]
ctl01
ctl02

[nova:children]
control
compute

[empty:children]
"""


def test_returns_groups_with_sorted_members():
    groups = parse_groups(SAMPLE)
    assert set(groups) == {"control", "nova:children", "empty:children"}
    assert groups["nova:children"] == ["compute", "control"]
    assert groups["control"] == ["ctl01", "ctl02"]


def test_empty_group_has_no_members():
    assert parse_groups(SAMPLE)["empty:children"] == []

from collections import defaultdict
import os
import jinja2

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = "environments/manager/images.yml"


def render(manager_version, versions_extra=None):
    versions = defaultdict(str, versions_extra or {})
    images = defaultdict(str)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(REPO_ROOT))
    return env.get_template(TEMPLATE).render(
        images=images, manager_version=manager_version, versions=versions
    )


def test_latest_with_pinned_kolla_ansible_uses_pinned_tag():
    # When manager_version=latest and kolla_ansible is present in versions
    # (as it is once release/latest/base.yml is updated), the rendered
    # tag must be the pinned value, not openstack_version.
    result = render("latest", {"kolla_ansible": "0.20260328.0"})
    assert 'kolla_ansible_tag: "0.20260328.0"' in result


def test_pinned_release_with_kolla_ansible_uses_pinned_tag():
    # Regression: pinned manager_version must continue to use the pinned tag.
    result = render("10.0.0", {"kolla_ansible": "0.20260328.0"})
    assert 'kolla_ansible_tag: "0.20260328.0"' in result

import os

import jinja2
import requests
from requests.adapters import HTTPAdapter, Retry
import yaml

# get environment parameters

MANAGER_VERSION = os.environ.get("MANAGER_VERSION", None)
if not MANAGER_VERSION:
    try:
        with open("configuration.yml") as fp:
            data = yaml.load(fp, Loader=yaml.FullLoader)

        MANAGER_VERSION = data["manager_version"]
    except:
        MANAGER_VERSION = "latest"

VERSIONS_URL = os.environ.get(
    "VERSIONS_URL",
    "https://raw.githubusercontent.com/osism/release/main/%s/base.yml"
    % MANAGER_VERSION,
)
IMAGES_URL = os.environ.get(
    "IMAGES_URL",
    "https://raw.githubusercontent.com/osism/release/main/etc/images.yml",
)
IMAGES_TEMPLATE_PATH = os.environ.get("IMAGES_TEMPLATE_PATH", "images.yml")
IMAGES_PATH = os.environ.get("IMAGES_PATH", "images.yml")


def fetch_yaml(url):
    """Fetch and parse a YAML file, retrying transient failures.

    Every config build fetches these URLs from raw.githubusercontent.com
    unauthenticated, and its per-IP rate limit is easy to trip -- a handful of
    builds in an afternoon will do it. The limit clears on its own, so retry
    rather than fail; raise_on_status is off so an exhausted retry surfaces as
    the response's own status and URL, the same as a status that is not
    retried at all.
    """
    retry = Retry(
        total=4,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    with requests.Session() as session:
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        r = session.get(url, timeout=30)
    r.raise_for_status()
    return yaml.full_load(r.text)


# load versions files from release repository

versions = fetch_yaml(VERSIONS_URL)
images = fetch_yaml(IMAGES_URL)

# always use latest osism if manager version is latest
if MANAGER_VERSION == "latest":
    versions["docker_images"]["inventory_reconciler"] = "latest"
    versions["docker_images"]["osism"] = "latest"
    versions["docker_images"]["osism_ansible"] = "latest"
    versions["docker_images"]["osism_kubernetes"] = "latest"

if "osism_ansible" not in versions["docker_images"]:
    versions["docker_images"][
        "osism_ansible"
    ] = "{{ manager_version|default('latest') }}"

if "osism_kubernetes" not in versions["docker_images"]:
    versions["docker_images"][
        "osism_kubernetes"
    ] = "{{ manager_version|default('latest') }}"

# prepare jinja2 environment

loader = jinja2.FileSystemLoader(searchpath=".")
environment = jinja2.Environment(loader=loader)

# render images.yml

template = environment.get_template(IMAGES_TEMPLATE_PATH)
result = template.render(
    {
        "images": images,
        "manager_version": MANAGER_VERSION,
        "versions": versions["docker_images"],
    }
)
with open(IMAGES_PATH, "w+") as fp:
    fp.write(result)

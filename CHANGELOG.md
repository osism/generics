# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file was started on September 03, 2022. Changes prior to this date are not included in the CHANGELOG.

## [v0.20260319.0] - 2026-03-19

### Dependencies

- debops 3.2.5 → 3.3.0 (osism/cfg-generics#580)
- packaging 25.0 → 26.0 (osism/cfg-generics#577)
- pynetbox 7.5.0 → 7.6.1 (osism/cfg-generics#576, osism/cfg-generics#578)
- tabulate 0.9.0 → 0.10.0 (osism/cfg-generics#579)

## [v0.20251130.0] - 2025-11-30

### Added

- Kolla Watcher inventory groups (watcher, watcher-api, watcher-applier, watcher-engine) (osism/cfg-generics#574)

## [v0.20251121.0] - 2025-11-21

### Added

- Manager: add pynetbox to the requirements to enable use of Netbox for inventory during deployment of the manager

### Dependencies

- ansible 11.11.0 → 11.12.0 (osism/cfg-generics#571)

## [v0.20251019.0] - 2025-10-19

### Added

- Kepler group in monitoring inventory (osism/cfg-generics#568)

### Changed

- Default `docker_registry_ansible` from `quay.io` to `registry.osism.tech` (osism/cfg-generics#569)
- Default `docker_registry` from unset to `registry.osism.tech/dockerhub` (osism/cfg-generics#570)

### Dependencies

- ansible-pylibssh 1.2.2 → 1.3.0 (osism/cfg-generics#567)

## [v0.20251012.0] - 2025-10-12

### Added
- Inventory: add stepca group (osism/cfg-generics#566)

### Changed
- Inventory: deploy opentelemetry_collector on the monitoring node instead of manager (osism/cfg-generics#565)

### Dependencies
- ansible 11.10.0 → 11.11.0 (osism/cfg-generics#563)
- debops 3.2.4 → 3.2.5 (osism/cfg-generics#564)
- paramiko 3.5.1 → 4.0.0 (osism/cfg-generics#551)

## [v0.20251006.0] - 2025-10-06

### Added
- Substation group in infrastructure inventory (osism/cfg-generics#562)

### Dependencies
- pyyaml 6.0.2 → 6.0.3 (osism/cfg-generics#561)

## [v0.20250927.0] - 2025-09-27

### Added

- `nova-metadata` inventory group (osism/cfg-generics#558)
- `ovn-sb-db-relay` inventory group (osism/cfg-generics#559)

### Changed

- Rename repository from cfg-generics to generics (osism/cfg-generics#560)

## [v0.20250920.0] - 2025-09-20

### Added
- osism-frontend image to manager images (#556)

### Fixed
- Typo in inventory filename (50-infrastruture → 50-infrastructure) (osism/cfg-generics#557)

## [v0.20250915.0] - 2025-09-15

### Dependencies
- ansible 11.9.0 → 11.10.0 (osism/cfg-generics#555)

## [v0.20250823.0] - 2025-08-23

### Added

- Cosign secrets to Zuul configuration (osism/cfg-generics#549)

### Dependencies

- ansible 11.7.0 → 11.9.0 (osism/cfg-generics#550, osism/cfg-generics#552)
- requests 2.32.4 → 2.32.5 (osism/cfg-generics#553)

## [v0.20250709.0] - 2025-07-09

### Added
- gnmic group in monitoring inventory (osism/cfg-generics#548)

## [v0.20250701.0] - 2025-07-01

### Added
- Conditional vault password file support in run.sh via `$VAULT` environment variable (osism/cfg-generics#543)
- Automatic detection of `.vault_pass` file in manager environment for vault password handling (osism/cfg-generics#544)

### Changed
- Remove outdated comment about image tag dependency on CEPH_VERSION or OPENSTACK_VERSION (osism/cfg-generics#542)

### Dependencies
- requests 2.32.3 → 2.32.4 [security] (osism/cfg-generics#546)
- ansible 11.6.0 → 11.7.0 (osism/cfg-generics#547)

## [v0.20250530.0] - 2025-05-30

### Added
- Support for explicit kolla_ansible and ceph_ansible version overrides in manager images configuration (osism/cfg-generics#536)
- CI jobs to test template rendering for latest, stable, and stable-legacy manager versions (osism/cfg-generics#541)

### Changed
- Default OpenStack version from 2024.1 to 2024.2 for latest manager builds (osism/cfg-generics#537)
- Template rendering script to support configurable template and output paths via environment variables (osism/cfg-generics#541)
- Jinja2 whitespace controls in manager images template for cleaner output (osism/cfg-generics#539, osism/cfg-generics#540, osism/cfg-generics#541)

### Fixed
- Version check keys for ceph-ansible and kolla-ansible using underscores to match actual dictionary keys (osism/cfg-generics#538)

### Removed
- CI gilt tox job and gate pipeline, replaced by template test jobs (osism/cfg-generics#541)

## [v0.20250529.0] - 2025-05-29

### Added
- Support for `noop` playbook in manager run script to only prepare everything without executing a playbook (osism/cfg-generics#531)
- `interpreter_python = auto_silent` setting in manager Ansible configuration to suppress interpreter discovery warnings (osism/cfg-generics#532)
- Netbox Redis image definition in manager images configuration (osism/cfg-generics#533)

### Changed
- Refreshed Zuul secrets (osism/cfg-generics#534)

### Dependencies
- ansible 11.5.0 → 11.6.0 (osism/cfg-generics#535)

## [v0.20250428.0] - 2025-04-28

### Changed
- Use uv instead of pip for package installation (osism/cfg-generics#527)

### Fixed
- Backward compatibility of osism-kubernetes/ansible versions in render-images (osism/cfg-generics#528)

### Dependencies
- packaging 24.2 → 25.0 (osism/cfg-generics#529)
- ansible 11.4.0 → 11.5.0 (osism/cfg-generics#530)

## [v0.20250408.0] - 2025-04-08

### Changed
- Always use latest osism version when manager version is set to latest (osism/cfg-generics#522, osism/cfg-generics#523, osism/cfg-generics#524)
- Always use latest inventory-reconciler version when manager version is set to latest (osism/cfg-generics#525)
- Support new osism-ansible and osism-kubernetes image tags with independent versioning (osism/cfg-generics#526)

### Fixed
- Log message in set-versions.py now shows actual file path instead of placeholder (osism/cfg-generics#521)

## [v0.20250407.0] - 2025-04-07

### Dependencies
- ansible 9.4.0 → 11.4.0 (osism/cfg-generics#520)

## [v0.20250331.0] - 2025-03-31

### Added
- Inventory group `dnsmasq` (osism/cfg-generics#513)
- Inventory group `httpd` (osism/cfg-generics#514)
- Inventory group `zot` (osism/cfg-generics#515)

### Changed
- Remove `noqa E501` comments from `render-images.py` (osism/cfg-generics#507)

### Removed
- Unused dragonfly inventory groups (`dragonfly_client`, `dragonfly_server`)

### Dependencies
- ansible 10.7.0 → 11.4.0 (osism/cfg-generics#502, osism/cfg-generics#511, osism/cfg-generics#516, osism/cfg-generics#519)
- jinja2 3.1.4 → 3.1.6 (osism/cfg-generics#509, osism/cfg-generics#518)
- paramiko 3.5.0 → 3.5.1 (osism/cfg-generics#512)

## [v0.20241206.0] - 2024-12-06

### Added
- Inventory group `teleport` for Teleport service (osism/cfg-generics#494, osism/cfg-generics#495)
- Inventory group `wazuh_agent` for Wazuh agent (osism/cfg-generics#496)
- Inventory group `opentelemetry_collector` for OpenTelemetry Collector (osism/cfg-generics#500)

### Removed
- Inventory group `metering` (osism/cfg-generics#503)
- Inventory group `tang` (osism/cfg-generics#504)
- Inventory group `clevis` (osism/cfg-generics#505)

### Dependencies
- ansible 10.4.0 → 10.7.0 (osism/cfg-generics#493, osism/cfg-generics#499, osism/cfg-generics#506)
- debops 3.2.1 → 3.2.4 (osism/cfg-generics#492, osism/cfg-generics#497, osism/cfg-generics#498)
- packaging 24.1 → 24.2 (osism/cfg-generics#501)

## [v0.20241006.0] - 2024-10-06

### Changed
- Inventory now uses `generic` group by default for the FRR service (osism/cfg-generics#491)

## [v0.20240924.0] - 2024-09-24

### Added
- pgautoupgrade image for manager environment (osism/cfg-generics#489)

### Changed
- Use venv instead of virtualenv in manager run script (osism/cfg-generics#488)

### Dependencies
- paramiko 3.4.1 → 3.5.0 (osism/cfg-generics#486)
- debops 3.1.0 → 3.2.1 (osism/cfg-generics#487, osism/cfg-generics#490)

## [v0.20240911.0] - 2024-09-11

### Dependencies

- ansible 10.3.0 → 10.4.0 (osism/cfg-generics#485)

## [v0.20240904.0] - 2024-09-04

### Changed
- Default OpenStack version updated from 2023.2 to 2024.1 for latest manager version (osism/cfg-generics#483)
- Deploy node-exporter & cadvisor on all nodes via generic group instead of specific node groups (osism/cfg-generics#484)

## [v0.20240825.0] - 2024-08-25

### Changed
- Deploy podman on all nodes instead of only manager nodes (osism/cfg-generics#482)

## [v0.20240818.0] - 2024-08-18

### Added
- DTRACK_API_KEY secret to Zuul configuration (osism/cfg-generics#481)
- `ansible_vault_encrypt_string` Makefile target for encrypting strings from stdin (osism/cfg-generics#472)

### Changed
- Improved ANSIBLE_VAULT detection pattern to use anchored regex for more accurate matching (osism/cfg-generics#472)
- Replaced `$(info ...)` with `$(shell echo ... >&2)` for proper stderr output in Makefile (osism/cfg-generics#472)
- Fixed example text in `ansible_vault_show` error message (osism/cfg-generics#472)

### Removed
- `openstack_health_monitor` inventory group (osism/cfg-generics#480)

### Dependencies
- ansible 10.2.0 → 10.3.0 (osism/cfg-generics#479)

## [v0.20240812.0] - 2024-08-12

### Added
- `prometheus_pushgateway` inventory group (osism/cfg-generics#476)

### Removed
- `postgres-upgrade` image from manager configuration (osism/cfg-generics#475)

### Dependencies
- paramiko 3.4.0 → 3.4.1 (osism/cfg-generics#478)
- pyyaml 6.0.1 → 6.0.2 (osism/cfg-generics#477)

## [v0.20240723.0] - 2024-07-23

### Added
- Neutron OVN VPN agent group in Kolla inventory (osism/cfg-generics#474)

### Dependencies
- ansible 10.1.0 → 10.2.0 (osism/cfg-generics#473)

## [v0.20240710.0] - 2024-07-10

### Added
- osism-kubernetes image configuration (osism/cfg-generics#464)
- Inventory groups for masakari (osism/cfg-generics#462)
- Inventory groups for rook (osism/cfg-generics#466)
- Inventory group for netbird (osism/cfg-generics#452)
- Inventory group for k9s (osism/cfg-generics#453)
- Inventory group for zabbix_agent (osism/cfg-generics#448)

### Changed
- Improve handling of Ansible Vault encrypted files with auto-detection of vault password from osism-ansible container (osism/cfg-generics#470)
- Improve secret management with vault password checks, safer rekeying, and new encrypt/decrypt/edit targets (osism/cfg-generics#465)
- Fix version prefixing in run.sh when version is latest/main (osism/cfg-generics#455)
- Check for `$VENV_PATH/bin/activate` instead of `$VENV_PATH` in manager run.sh (osism/cfg-generics#454)
- Fix check for encrypted files in manager run.sh (osism/cfg-generics#450)
- Remove extra spaces in images.yml template expressions (osism/cfg-generics#471)

### Fixed
- Fix copy & paste issue in Makefile `.PHONY` target for sync (osism/cfg-generics#447)

### Removed
- Inventory group kompose (osism/cfg-generics#458)
- Inventory group patchman (osism/cfg-generics#467)

### Dependencies
- ansible 9.6.0 → 10.1.0 (osism/cfg-generics#457, osism/cfg-generics#463, osism/cfg-generics#456)
- ansible-pylibssh 1.1.0 → 1.2.2 (osism/cfg-generics#459, osism/cfg-generics#468, osism/cfg-generics#469)
- netaddr 1.2.1 → 1.3.0 (osism/cfg-generics#449)
- packaging 24.0 → 24.1 (osism/cfg-generics#460)
- requests 2.32.2 → 2.32.3 (osism/cfg-generics#451)

## [v0.20240524.0] - 2024-05-24

### Added
- Blazar inventory groups for API and manager services (osism/cfg-generics#441)

### Changed
- Use `.PHONY` targets in the Makefile instead of a single `phony` target (osism/cfg-generics#439)

### Fixed
- Replace GNU sed-specific extension in `run.sh` to ensure compatibility with non-GNU sed (osism/cfg-generics#440)

### Removed
- Release notes managed in this repository, now managed centrally in osism/release and osism/osism.github.io (osism/cfg-generics#446)

### Dependencies
- jinja2 3.1.3 → 3.1.4 (osism/cfg-generics#438)
- ansible 9.5.1 → 9.6.0 (osism/cfg-generics#445)
- requests 2.31.0 → 2.32.2 (osism/cfg-generics#442, osism/cfg-generics#443, osism/cfg-generics#444)

## [v0.20240503.0] - 2024-05-03

### Added
- Script to manage versions (docker, docker CLI, ansible collections, generics) from osism/release (osism/cfg-generics#418, osism/cfg-generics#424, osism/cfg-generics#426, osism/cfg-generics#430, osism/cfg-generics#435)
- Inventory sorting check script and CI job (osism/cfg-generics#420)
- Detection of whether ANSIBLE_ASK_VAULT_PASS is required in manager run script (osism/cfg-generics#429)
- Check for openstack_version and ceph_version parameters when manager_version is not latest (osism/cfg-generics#433)

### Changed
- Renamed set-docker-version.py to set-versions.py to handle multiple version types (osism/cfg-generics#425)
- Improved gilt file ordering and render-images.py destination path (osism/cfg-generics#419)
- Switched from hidden `.venv` to `venv` directory and added shell prompt (osism/cfg-generics#413)
- Allow overwriting the branch used in Makefile via BRANCH environment variable (osism/cfg-generics#431)
- Only manage generics version in gilt.yml for manager >= 7.0.3 (osism/cfg-generics#432)
- Fixed inventory sorting in infrastructure and kolla inventory files (osism/cfg-generics#420)
- Truncate files after writing in set-versions.py to prevent stale content (osism/cfg-generics#437)
- Removed non-visible print statements from set-versions.py (osism/cfg-generics#436)

### Fixed
- Fixed wrong exit code in Makefile when BRANCH is not set (osism/cfg-generics#434)
- Fixed regex patterns and configuration file path in set-versions.py (osism/cfg-generics#427, osism/cfg-generics#428)

### Dependencies
- netaddr 0.10.1 → 1.2.1 (osism/cfg-generics#396)
- ansible 9.4.0 → 9.5.1 (osism/cfg-generics#423) — 9.5.0 was reverted due to breaking change (osism/cfg-generics#422)
- packaging 24.0 (new dependency) (osism/cfg-generics#432)

## [v0.20240417.0] - 2024-04-17

### Added
- Manager: check that the configured branch matches the current checkout branch during the seed phase (osism/cfg-generics#416)
- Manager: warn when `ANSIBLE_USER` is not set to `dragon` for plays other than `operator` (osism/cfg-generics#417)

### Dependencies
- ansible 9.3.0 → 9.4.0 (osism/cfg-generics#415)

## [v0.20240327.0] - 2024-03-27

### Changed
- Make the used Ansible version configurable via `ANSIBLE_VERSION` environment variable (osism/cfg-generics#412)

### Dependencies
- ansible 9.3.0 → 9.4.0 (osism/cfg-generics#414)

## [v0.20240319.0] - 2024-03-19

No changes.

## [v0.20240311.0] - 2024-03-11

### Added
- Makefile to gilt.yml for synchronization (osism/cfg-generics#410)

### Changed
- Default OpenStack version from 2023.1 to 2023.2 (osism/cfg-generics#411)

## [v0.20240307.0] - 2024-03-07

### Added
- Makefile to automate common tasks (sync, vault rekey, vault show) (osism/cfg-generics#397)

### Removed
- OpenLDAP group from inventory (osism/cfg-generics#407)

### Dependencies
- ansible 9.2.0 → 9.3.0 (osism/cfg-generics#406, osism/cfg-generics#408)

## [v0.20240221.0] - 2024-02-21

### Added
- Zuul post job to push osism-ansible container image (osism/cfg-generics#399)
- Zuul post job to push inventory-reconciler container image (osism/cfg-generics#405)
- Zuul secret for container image push jobs (osism/cfg-generics#400)

### Changed
- Deploy k3s master services on control nodes instead of manager nodes by default (osism/cfg-generics#398)

## [v0.20240204.0] - 2024-02-04

### Added
- `thanos_sidecar` inventory group which defaults to prometheus (osism/cfg-generics#385)
- `kubectl` inventory group (osism/cfg-generics#391)
- `letsencrypt` inventory groups (osism/cfg-generics#393)

### Dependencies
- ansible 8.6.1 → 9.2.0 (osism/cfg-generics#387, osism/cfg-generics#381, osism/cfg-generics#394)
- debops 3.0.5 → 3.1.0 (osism/cfg-generics#386)
- jinja2 3.1.2 → 3.1.3 (osism/cfg-generics#392)
- netaddr 0.9.0 → 0.10.1 (osism/cfg-generics#389, osism/cfg-generics#390)
- paramiko 3.3.1 → 3.4.0 (osism/cfg-generics#388)

## [v0.20231126.0] - 2023-11-26

### Added
- Installation of `osism.commons` Ansible collection in manager `run.sh` (osism/cfg-generics#366)
- Configurable Ansible collection sources in manager `run.sh` via `ANSIBLE_COLLECTION_COMMONS_SOURCE`, `ANSIBLE_COLLECTION_SERVICES_SOURCE`, and `ANSIBLE_PLAYBOOKS_MANAGER_SOURCE` environment variables (osism/cfg-generics#379)
- Read `MANAGER_VERSION` from `configuration.yml` when not set via environment variable (osism/cfg-generics#382)
- python-black Zuul job (osism/cfg-generics#382)

### Changed
- Replace `requirements.yml` with direct `ansible-galaxy collection install` commands in manager `run.sh` (osism/cfg-generics#362)
- Migrate shell check workflow from GitHub Actions to Zuul (osism/cfg-generics#363)
- Use `yaml.FullLoader` in render scripts (osism/cfg-generics#383)
- Use relative filename for `configuration.yml` in render scripts (osism/cfg-generics#384)

### Fixed
- Do not use private key for operator play when `ANSIBLE_ASK_PASS` is set (osism/cfg-generics#367)
- Pass exit codes through in `environments/manager/run.sh` and use trap for cleanup (osism/cfg-generics#377)

### Removed
- `environments/manager/requirements.yml` file (osism/cfg-generics#362)
- `render-ansible-requirements.py` from `gilt.yml` (osism/cfg-generics#365)
- `ruamel.yaml` dependency (osism/cfg-generics#376)
- GitHub Actions shell check workflow (osism/cfg-generics#363)

### Dependencies
- netaddr 0.8.0 → 0.9.0 (osism/cfg-generics#361)
- ansible 8.4.0 → 8.6.1 (osism/cfg-generics#368, osism/cfg-generics#378, osism/cfg-generics#380)

## [v0.20230919.0] - 2023-09-19

No changes.

## [v0.20230915.0] - 2023-09-15

### Added
- Metering group in inventory (osism/cfg-generics#358)

### Changed
- Default OpenStack version changed from zed to 2023.1 (osism/cfg-generics#360)

### Dependencies
- ansible 8.3.0 → 8.4.0 (osism/cfg-generics#359)

## [v0.20230906.0] - 2023-09-06

### Added
- `neutron-ovn-agent` inventory group with `compute` as children (osism/cfg-generics#356)

### Dependencies
- actions/checkout v3 → v4 (osism/cfg-generics#357)

## [v0.20230902.0] - 2023-09-02

### Fixed
- Revert removal of aodh inventory groups for compatibility with older OSISM versions (osism/cfg-generics#355)

## [v0.20230901.0] - 2023-09-01

### Added
- Inventory groups required by k3s (osism/cfg-generics#342)
- cfg-generics-tox Zuul job and tox configuration

### Changed
- Default Ceph version from pacific to quincy (osism/cfg-generics#338)
- Default k3s setup to only run a k3s server on the manager, k3s_node group is empty by default (osism/cfg-generics#346)
- Migrated gilt test from GitHub Actions to Zuul

### Fixed
- Wrong mariadb variable names in images.yml (osism/cfg-generics#347)
- Wrong redis variable names in images.yml (osism/cfg-generics#348)
- Wrong tag references for ara_server_mariadb and manager_redis in images.yml (osism/cfg-generics#349)

### Removed
- Obsolete minikube group from inventory (osism/cfg-generics#343)
- Obsolete rundeck and jenkins groups from inventory (osism/cfg-generics#344)
- kubectl group from inventory, already part of k3s (osism/cfg-generics#345)
- Unused aodh groups from kolla inventory (osism/cfg-generics#353)
- GitHub Actions gilt test workflow (replaced by Zuul job)

### Dependencies
- ansible 8.0.0 → 8.3.0 (osism/cfg-generics#354)
- paramiko 3.2.0 → 3.3.1 (osism/cfg-generics#352)
- pyyaml 6.0 → 6.0.1 (osism/cfg-generics#340)
- ruamel.yaml 0.17.31 → 0.17.32 (osism/cfg-generics#337)

## [v0.20230614.0] - 2023-06-14

### Added
- Scaphandre group in monitoring inventory (osism/cfg-generics#326)
- postgres_upgrade image support in manager (osism/cfg-generics#325)

### Dependencies
- ruamel.yaml 0.17.21 → 0.17.31 (osism/cfg-generics#321, osism/cfg-generics#323, osism/cfg-generics#324, osism/cfg-generics#331, osism/cfg-generics#334, osism/cfg-generics#336)
- requests 2.28.2 → 2.31.0 (osism/cfg-generics#320, osism/cfg-generics#322, osism/cfg-generics#329)
- ansible 7.4.0 → 8.0.0 (osism/cfg-generics#319, osism/cfg-generics#330, osism/cfg-generics#335)
- paramiko 3.1.0 → 3.2.0 (osism/cfg-generics#333)
- debops 3.0.4 → 3.0.5 (osism/cfg-generics#332)

## [v0.20230407.0] - 2023-04-07

### Added

- Periodic-daily jobs in Zuul for better visibility of errors after linter updates (osism/cfg-generics#318)

### Dependencies

- ansible 7.3.0 → 7.4.0 (osism/cfg-generics#317)

## [v0.20230321.0] - 2023-03-21

### Changed
- Use kolla-ansible zed by default instead of yoga (osism/cfg-generics#316)

## [v0.20230312.0] - 2023-03-12

### Changed
- Add `environments/manager/requirements.txt` to Renovate configuration (osism/cfg-generics#313)

### Dependencies
- ansible 6.7.0 → 7.3.0 (osism/cfg-generics#308, osism/cfg-generics#314)
- debops 3.0.3 → 3.0.4 (osism/cfg-generics#312)
- paramiko 2.12.0 → 3.1.0 (osism/cfg-generics#306, osism/cfg-generics#315)

## [v0.20230308.0] - 2023-03-08

No changes. This release represents the transition from semantic versioning (v0.3.0) to date-based versioning.

## [v0.3.0] - 2023-02-21

### Added
- Script to check alphabetical sorting in inventory files (osism/cfg-generics#285)
- Osquery group in generic inventory
- ansible-pylibssh package for manager environment (osism/cfg-generics#301)
- OpenSearch and OpenSearch Dashboards groups for Kolla inventory (osism/cfg-generics#302)
- Skyline groups for Kolla inventory (osism/cfg-generics#309)

### Changed
- Alphabetical sorting of Kolla inventory entries (osism/cfg-generics#285)
- Moved YAML syntax check from GitHub Actions to Zuul (osism/cfg-generics#310)
- Moved Python syntax check from GitHub Actions to Zuul (osism/cfg-generics#311)

### Fixed
- Moved pipelining setting to correct defaults section in ansible.cfg (osism/cfg-generics#300)
- Added infrastructure environment parameters for k8s playbook in run.sh (osism/cfg-generics#303)
- Corrected opensearch-dashboard group name to opensearch-dashboards (osism/cfg-generics#304)

### Removed
- Monasca inventory groups (osism/cfg-generics#293)

### Dependencies
- ansible 6.3.0 → 6.7.0 (osism/cfg-generics#289, osism/cfg-generics#291, osism/cfg-generics#295, osism/cfg-generics#299)
- paramiko 2.11.0 → 2.12.0 (osism/cfg-generics#294)
- requests 2.28.1 → 2.28.2 (osism/cfg-generics#305)
- tabulate 0.8.10 → 0.9.0 (osism/cfg-generics#290)

## [v0.2.0] - 2022-09-11

### Added
- Missing kolla inventory groups: outward-rabbitmq, tls-backend, ironic-http, ironic-tftp, mistral-event-engine, prometheus-msteams, hacluster, hacluster-remote (osism/cfg-generics#284)
- Script to check for missing kolla inventory groups against upstream kolla-ansible (osism/cfg-generics#284)

### Changed
- Default OpenStack version from xena to yoga (osism/cfg-generics#286)
- Only use manager version as default for ceph/openstack version when manager is not set to latest (osism/cfg-generics#287)
- Use MANAGER_VERSION variable in image rendering script (osism/cfg-generics#288)

## [v0.1.0] - 2022-09-03

### Added
- Initial project structure with manager environment, Ansible playbooks, image definitions, and run script
- gilt configuration for syncing files from cfg-master repository
- Travis CI integration with yamllint validation
- Tags for all roles in the bootstrap playbook
- Reboot playbook for manager systems
- Cockpit role and dedicated playbook
- Grub playbook with privilege escalation
- Chrony role, dedicated playbook, and integration into bootstrap playbook
- Script to generate manager Ansible requirements from release repository using Jinja2 templating
- Pipfile for manager environment
- Proxy playbook
- Python3 playbook for installing python3 on all hosts
- AWX docker image
- ara_web docker image
- osism.docker-compose ansible role to bootstrap and docker playbooks
- Unified host groups for Ceph and Kolla inventory (51-ceph, 51-kolla)
- `docker_registry_service` and `docker_registry_ansible` parameters for container images
- Script to remove latest tag from kolla-ansible/ceph-ansible when manager version is latest
- PR Labeler GitHub workflow
- Check yaml syntax GitHub workflow
- Gilt GitHub workflow
- Link to documentation in README
- GitHub workflow for checking Python syntax
- Inventory files for ceph, infrastructure, kolla, monitoring, openstack, and generic environments
- Inventory group for phpmyadmin (osism/cfg-generics#3)
- Inventory groups for dragonfly client and server (osism/cfg-generics#4)
- Inventory groups for hddtemp and smartd (osism/cfg-generics#6)
- Inventory group for adminer (osism/cfg-generics#8)
- Inventory group for keycloak (osism/cfg-generics#9)
- Inventory group for openstack_health_monitor (osism/cfg-generics#15)
- Inventory group for bifrost (osism/cfg-generics#16)
- Script to generate `environments/manager/images.yml` from Jinja2 templates (osism/cfg-generics#19)
- Renovate configuration for automated dependency updates (osism/cfg-generics#38)
- Docker registry default values for images (osism/cfg-generics#34)
- awxclient image to manager images (osism/cfg-generics#45)
- requirements.txt to gilt configuration (osism/cfg-generics#49)
- Check shell syntax GitHub workflow (osism/cfg-generics#51)
- ironic-ipxe inventory group (osism/cfg-generics#69)
- Netbox playbook for manager (osism/cfg-generics#78)
- Minikube inventory group (osism/cfg-generics#83)
- Inventory group for kubectl (osism/cfg-generics#84)
- Inventory groups for senlin (osism/cfg-generics#90)
- Inventory groups for monasca (osism/cfg-generics#93)
- Inventory group for kompose (osism/cfg-generics#94)
- Inventory group for rundeck (osism/cfg-generics#95)
- Inventory group for kafka (osism/cfg-generics#96)
- Inventory group for zookeeper (osism/cfg-generics#97)
- Inventory groups for storm (osism/cfg-generics#99)
- Inventory groups for trove (osism/cfg-generics#100)
- osism/inventory-reconciler image (osism/cfg-generics#106)
- GitHub workflow to automatically update environments/manager/images.yml (osism/cfg-generics#104)
- Inventory group `homer` for manager (osism/cfg-generics#109)
- Restart manager service task in manager playbook (osism/cfg-generics#110)
- Inventory group `jenkins` for manager (osism/cfg-generics#112)
- Inventory groups for cloudkitty (cloudkitty-api, cloudkitty-processor) (osism/cfg-generics#117)
- Inventory group `openldap` for manager (osism/cfg-generics#128)
- Inventory group `octavia-driver-agent` for network (osism/cfg-generics#129)
- Inventory group `zuul` for manager
- README with synchronization instructions and inventory documentation
- Tailscale inventory group, defaulting to manager host (osism/cfg-generics#173)
- Nexus inventory group (osism/cfg-generics#178)
- Boundary inventory group (osism/cfg-generics#178)
- AWX and AWX client images (osism/cfg-generics#180)
- Scheduler image, later renamed to osism/osism (osism/cfg-generics#184)
- Vault image (osism/cfg-generics#187)
- Traefik image and playbook (osism/cfg-generics#201, osism/cfg-generics#202)
- Traefik inventory group (osism/cfg-generics#200)
- Journald inventory group (osism/cfg-generics#207)
- FRR inventory group (osism/cfg-generics#194)
- Atlantis inventory group (osism/cfg-generics#212)
- ClamAV inventory group (osism/cfg-generics#212)
- DNSdist inventory group (osism/cfg-generics#217)
- Cgit inventory group (osism/cfg-generics#225)
- Zun service groups to Kolla inventory (osism/cfg-generics#199)
- `netaddr` to manager requirements (osism/cfg-generics#190)
- `INSTALL_ANSIBLE` parameter to run.sh to allow skipping Ansible installation (osism/cfg-generics#197)
- `VENV_PYTHON_BIN` parameter to run.sh for configurable Python binary in venv (osism/cfg-generics#221)
- `force_valid_group_names = ignore` to manager ansible.cfg to suppress warnings (osism/cfg-generics#196)
- Loadbalancer inventory group for Kolla, required starting with Xena (osism/cfg-generics#230)
- Prometheus-libvirt-exporter inventory group for compute nodes (osism/cfg-generics#246)
- osism-netbox image to manager images (osism/cfg-generics#250)
- Paramiko as manager requirement for docker login support (osism/cfg-generics#253)
- Runc and containerd inventory groups (osism/cfg-generics#258)
- Image rendering script (`render-images.py`) to replace the update-images workflow
- Tang group to infrastructure inventory (osism/cfg-generics#263)
- Clevis group to infrastructure inventory (osism/cfg-generics#264)
- Wireguard role to infrastructure inventory (osism/cfg-generics#266)
- Squid group to infrastructure inventory (osism/cfg-generics#278)

### Changed
- Allow additional Ansible arguments to be passed through run.sh
- Set default values for all image tags and registry in images.yml
- Restrict playbooks to manager hosts instead of all hosts
- Separate ceph_manager_version and kolla_manager_version from osism_manager_version
- Use SSH pipelining instead of paramiko transport in ansible.cfg
- Make virtualenv path configurable via VENV_PATH environment variable
- Use Python 3 for scripts and virtualenv
- Default OpenStack version updated from ocata to xena
- Default Ceph version updated from luminous to pacific
- Pin external roles (hardening, debops.grub, ANXS.*) to specific commit hashes
- Convert requirements.yml to Jinja2 template for automated version rendering
- Use pip3 instead of pip in run.sh
- Make keypair destination configurable in playbook-keypair.yml
- Use debops package instead of individual debops.grub role from git
- Add additional debops roles (environment, kmod, locales, rsyslog, sysctl, python)
- Fix debops role names to match new directory structure
- Replace osism.network-interfaces with osism.network
- Update default version to 2020.1.0
- Rename repository from cfg-master to cfg-generics
- Replace Travis CI with GitHub Actions workflows
- Enable yamllint truthy check
- Update documentation link to docs.osism.de
- Copy inventory files first in gilt.yml ordering
- Improved manager `run.sh` script with configurable `INSTALL_ANSIBLE_ROLES` and `VENV_PATH` variables and conditional virtualenv setup
- Renamed inventory group `global` to `generic`
- Renamed inventory group `zabbix-agent` to `zabbix_agent` (osism/cfg-generics#7)
- Migrated from individual Ansible roles to `osism.commons` and `osism.services` collections (osism/cfg-generics#11)
- Refactored manager images.yml with simplified image references and explicit version tags (osism/cfg-generics#13)
- Restructured Ansible requirements to use collections format (osism/cfg-generics#20)
- Updated and renamed GitHub workflows for consistency and yamllint compliance (osism/cfg-generics#21)
- Renamed `render-manager-ansible-requirements.py` to `render-ansible-requirements.py` (osism/cfg-generics#23)
- Improved README title to "Generic configuration files" (osism/cfg-generics#24)
- Migrated `osism.network` role to `osism.commons` collection (osism/cfg-generics#25)
- Replace osism.commons role with individual roles in manager bootstrap playbook (osism/cfg-generics#26)
- Add missing roles (rsyslog, docker, auditd) to manager bootstrap (osism/cfg-generics#27)
- Deploy fluentd on all generic nodes instead of common nodes (osism/cfg-generics#28)
- Split manager bootstrap playbook into two parts (osism/cfg-generics#30)
- Remove debops roles from manager bootstrap (osism/cfg-generics#31)
- Remove roles_path from manager ansible.cfg (osism/cfg-generics#32)
- Use osism.commons.timezone instead of ANXS.timezone (osism/cfg-generics#35)
- Remove ANXS.utilities role from manager bootstrap (osism/cfg-generics#36)
- Clean up ansible requirements, remove ANXS roles (osism/cfg-generics#37)
- Move yamllint configuration file to project root (osism/cfg-generics#43)
- Use dedicated docker_registry_cephclient and docker_registry_openstackclient variables (osism/cfg-generics#44)
- Replace deprecated `dest` parameter with `path` in playbook-operator (osism/cfg-generics#46)
- Remove ANXS.apt from manager requirements (osism/cfg-generics#48)
- Ignore release directory in yamllint configuration (osism/cfg-generics#50)
- Pin all Python requirements to specific versions (osism/cfg-generics#38)
- Install cephclient on ceph control nodes instead of manager (osism/cfg-generics#52)
- Deploy Kolla Grafana and InfluxDB on control nodes instead of monitoring nodes (osism/cfg-generics#53)
- Move haproxy to control nodes (osism/cfg-generics#54)
- Place designate bind9 service on network nodes (osism/cfg-generics#55)
- Place additional Octavia services (health-manager, housekeeping, worker) on network nodes (osism/cfg-generics#56)
- Deploy cephclient on the manager by default (osism/cfg-generics#59)
- Always use virtualenv in manager run script (osism/cfg-generics#60)
- Use Ansible reboot module instead of shell command (osism/cfg-generics#61)
- Fix shell quoting issues in manager run.sh (osism/cfg-generics#51)
- Clean up Kolla inventory groups, remove obsolete services (osism/cfg-generics#72)
- AWX image tag now uses `awx_version` variable instead of `ceph_version-openstack_version` (osism/cfg-generics#85)
- Default values added for `ceph_version`, `openstack_version`, `awx_version`, and `manager_version` in image tags (osism/cfg-generics#86, osism/cfg-generics#88)
- InfluxDB deployment moved from control to monitoring node (osism/cfg-generics#98)
- Inventory files sorted in alphabetical order (osism/cfg-generics#101)
- Removed `become: true` from network playbook (osism/cfg-generics#102)
- Synced src/templates/images.yml.j2 with environments/manager/images.yml (osism/cfg-generics#103)
- Use quoted `"on"` in GitHub workflows instead of yamllint disable-line comment (osism/cfg-generics#107)
- Enable Ansible deprecation warnings in manager environment (osism/cfg-generics#111)
- Use `manager_version` as fallback default for ceph-ansible and kolla-ansible image tags
- Rename inventory group `heimdall` to `homer`
- Use `bot@osism.tech` email in GitHub workflows
- Use `main` branch instead of `master` in gilt configuration and requirements.yml (osism/cfg-generics#173)
- Enforce docker service restart in manager playbook
- Netbox image switched to custom OSISM image registry (`docker_registry_netbox`) (osism/cfg-generics#183, osism/cfg-generics#192)
- Scheduler image renamed from `osism/scheduler` to `osism/osism` (osism/cfg-generics#184)
- Manager bootstrap playbook reduced to minimum roles (timezone, chrony, docker, docker_compose) (osism/cfg-generics#193)
- Manager run.sh includes infrastructure environment for traefik and netbox playbooks (osism/cfg-generics#203)
- GitHub Actions branch builds restricted to main branch only (osism/cfg-generics#213)
- Use loadbalancer group instead of haproxy group in inventory (osism/cfg-generics#231)
- Make osism and inventory_reconciler image versions independently configurable (osism/cfg-generics#248)
- Improve images.yml rendering to use Jinja2 template with version lookups
- Use `osism.manager` playbooks from Galaxy instead of local playbook files (osism/cfg-generics#252)
- Set keypair_dest explicitly in manager run script
- Use generic OSISM Renovate configuration
- Configure Renovate to also update `environments/manager/requirements.txt`
- Fix syntax issue in test-gilt GitHub workflow (osism/cfg-generics#247)
- Sort entries in inventory files (osism/cfg-generics#271)

### Fixed
- Fix typo in bootstrap playbook ("tasg" → "tags")
- Add missing `become: true` in grub playbook
- Fix yamllint issues in requirements.yml by quoting Jinja2 expressions
- Fix wrong indentation in playbook-keypair.yml
- Fix wrong virtualenv parameter (`-e` to `-p`) in run.sh
- Add missing `$@` for argument passthrough in keypair playbook invocation
- Fix gilt.yml typo (`dest` to `dst`) for inventory files
- Don't gather facts on reboot playbook (osism/cfg-generics#2)
- Added missing `:children` keyword to dragonfly inventory groups (osism/cfg-generics#5)
- Added missing `git+` prefix to ansible-galaxy collection install commands (osism/cfg-generics#12)
- Fixed `docker_postgres` typo to `docker_registry` in images.yml (osism/cfg-generics#14)
- Fixed pr-labeler GitHub workflow job name (osism/cfg-generics#22)
- Fix docker registry variables to use docker_registry_ansible (osism/cfg-generics#42)
- Fix ceph inventory groups, make ceph-rgw and ceph-mds optional (osism/cfg-generics#58)
- Include `secrets.yml` from manager environment when executing run.sh (osism/cfg-generics#173)
- Fix typo `INSTALL_ANSBILE` → `INSTALL_ANSIBLE` in run.sh (osism/cfg-generics#198)
- Fix vault image template to use correct tag format (osism/cfg-generics#188)

### Removed
- Hardening role from bootstrap playbook and requirements
- Cockpit role from bootstrap playbook and cockpit playbook
- Travis CI configuration
- debops.grub role from requirements.yml (replaced by debops package)
- Separate yamllint config and test-requirements.txt
- Inventory file syncing from gilt overlay
- Pipfile from manager environment (osism/cfg-generics#17)
- `prepare-manager-images.py` script, replaced by template-based `render-images.py` (osism/cfg-generics#19)
- Gilt GitHub workflow, replaced with updated test-gilt workflow (osism/cfg-generics#21)
- Outdated example command from README (osism/cfg-generics#18)
- cloudkitty from Kolla inventory (osism/cfg-generics#29)
- aptly and installer images (osism/cfg-generics#33)
- searchlight, watcher, zun, and mongodb from Kolla inventory (osism/cfg-generics#72)
- Inventory group for pulp (osism/cfg-generics#92)
- "PR Labeler" GitHub workflow (osism/cfg-generics#108)
- AWX configuration (awxclient and awx images and templates)
- Inventory groups for zabbix and zabbix_agent
- Inventory group `ucs`
- Client version overrides (cephclient, openstackclient) from manager images
- AWX and awxclient images and template entries (osism/cfg-generics#229)
- Tailscale inventory group due to security concerns (osism/cfg-generics#242)
- Unused inventory groups (boundary, atlantis) from infrastructure inventory
- Local manager playbook files (bootstrap, chrony, configuration, docker, keypair, manager, netbox, network, operator, proxy, python, python3, reboot, traefik)
- update-images GitHub workflow, replaced by gilt-based rendering
- `src/templates/images.yml.j2` and `src/update-images.py`, replaced by `src/render-images.py`
- Yamllint check for `environments/manager/images.yml` (now a Jinja2 template)

### Dependencies
- ansible >=2.4,<2.5 → 6.3.0 (osism/cfg-generics#10, osism/cfg-generics#40, osism/cfg-generics#57, osism/cfg-generics#64, osism/cfg-generics#67, osism/cfg-generics#73, osism/cfg-generics#76, osism/cfg-generics#91, osism/cfg-generics#168, osism/cfg-generics#176, osism/cfg-generics#191, osism/cfg-generics#195, osism/cfg-generics#205, osism/cfg-generics#237, osism/cfg-generics#244, osism/cfg-generics#255, osism/cfg-generics#257, osism/cfg-generics#259, osism/cfg-generics#261, osism/cfg-generics#269, osism/cfg-generics#275, osism/cfg-generics#276, osism/cfg-generics#280, osism/cfg-generics#281)
- debops 2.1.2 → 3.0.3 (osism/cfg-generics#38, osism/cfg-generics#66, osism/cfg-generics#70, osism/cfg-generics#169, osism/cfg-generics#235, osism/cfg-generics#240, osism/cfg-generics#254, osism/cfg-generics#282)
- jinja2 2.11.2 → 3.1.2 (osism/cfg-generics#65, osism/cfg-generics#160, osism/cfg-generics#178, osism/cfg-generics#251, osism/cfg-generics#258)
- paramiko 2.10.3 → 2.11.0 (osism/cfg-generics#256, osism/cfg-generics#260)
- pyyaml 5.3.1 → 6.0 (osism/cfg-generics#62, osism/cfg-generics#63, osism/cfg-generics#167)
- requests 2.25.1 → 2.28.1 (osism/cfg-generics#140, osism/cfg-generics#214, osism/cfg-generics#215, osism/cfg-generics#274, osism/cfg-generics#277)
- ruamel.yaml 0.16.12 → 0.17.21 (osism/cfg-generics#71, osism/cfg-generics#74, osism/cfg-generics#75, osism/cfg-generics#77, osism/cfg-generics#147, osism/cfg-generics#175, osism/cfg-generics#208, osism/cfg-generics#211, osism/cfg-generics#236)
- adminer 4.7 → 4.8.1 (osism/cfg-generics#105)
- ara-server 1.5.3 → 1.5.7 (osism/cfg-generics#47, osism/cfg-generics#80, osism/cfg-generics#105)
- awxclient 16.0.0 → 19.5.1 (osism/cfg-generics#82, osism/cfg-generics#105, osism/cfg-generics#206, osism/cfg-generics#219)
- mariadb 10.5 → 10.8.2 (osism/cfg-generics#105, osism/cfg-generics#179)
- netbox v2.8 → v3.1.9-ldap (osism/cfg-generics#80, osism/cfg-generics#105, osism/cfg-generics#174, osism/cfg-generics#177, osism/cfg-generics#179, osism/cfg-generics#186, osism/cfg-generics#204, osism/cfg-generics#209, osism/cfg-generics#210, osism/cfg-generics#216, osism/cfg-generics#218)
- nginx 1.19-alpine → 1.21.6-alpine (osism/cfg-generics#105, osism/cfg-generics#179, osism/cfg-generics#209, osism/cfg-generics#223)
- phpmyadmin 5.0 → 5.1.3 (osism/cfg-generics#80, osism/cfg-generics#105)
- postgres 13-alpine → 14.2-alpine (osism/cfg-generics#181)
- redis 6-alpine → 6.2.6-alpine
- registry 2.7 → 2.8
- traefik v2.5.4 → v2.6.1 (osism/cfg-generics#220, osism/cfg-generics#222)
- vault 1.9.0 → 1.9.4 (osism/cfg-generics#220)
- actions/checkout v2 → v3 (osism/cfg-generics#238)
- actions/setup-python v2 → v4 (osism/cfg-generics#239, osism/cfg-generics#270)


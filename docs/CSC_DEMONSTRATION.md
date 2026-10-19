# CSC demonstration: executed and verified

**Actual five-scene metadata workload completed remotely on 19 October 2026, exit zero.**
On 19 October the supported browser reattached successfully to authenticated MyCSC.
The initially empty dashboard was followed by a prepared Student Project application.
On the next live inspection it had been submitted and project creation was verified:

- Project number: **2021696**, Unix group `project_2021696`.
- Name: **Kvarken Earth Observation Thesis**.
- Field: Natural sciences / 113 Computer and information sciences.
- Home organization: **University of Vaasa**; the author is shown as project manager.
- MyCSC displayed lifetime: **19 October 2026 - 1 January 2027** (the application
  requested 31 December; retain the service's displayed boundary rather than infer an hour).
- Service: **cPouta Enabled**, access granted **19 October 2026**.
- Allocation before launch: **30,000 Cloud BUs**, **0 used**, **100% remaining**.
- Verified OpenStack quota: **8 instances, 8 vCPUs, 32.2 GB RAM, 2 floating IPs, 10 volumes**.

The agent did not accept personal declarations. MyCSC creation and service status were
verified afterward at https://my.csc.fi/projects/2021696.
Cloud BUs are **not OpenStack instance/vCPU/RAM/storage/network quotas**.
An initial cPouta authorization denial was followed by successful authenticated access
through the supported sign-in route. No account security/terms choices were made by the agent.
No credentials were supplied in chat and no browser tokens were extracted.

## Actual deployment and execution

Execution instance **8d3f5911-360b-48fb-83a6-115a95d8bd5b** belonged to OpenStack project
**a1842d0445334e65afc3a2be05c5ac80** in the authenticated CSC dashboard. It used
`standard.tiny` (one vCPU, 1,000 MB RAM, 80 GB ephemeral disk), Ubuntu 24.04.5 LTS and
Python 3.12.3. Clean source revision was `0a009885e07f1bf25f2e1960ceb3f9ce3e4ac5c1`.

After two restricted SSH connection attempts timed out on an initial VM, a second VM
executed the workload using supported cloud-init customization. No wider ingress was added.
The runner started at **17:29:42.844271 UTC**, completed **17:29:43.815320 UTC**, and returned
**0**. Full runner elapsed was **0.971050 s**; the ingestion-only timer was **0.199499 s**
for **5 scenes / 68,286 canonical bytes**, **0 failures/retries**, **25.062840 items/s**.
VM provisioning, installation and raster work are excluded.

The authenticated instance console supplied a compressed evidence archive. Its retrieved
SHA-256 is `c12807b646e95916540826166c02febecdec39d85034a167d90282c21b3f85df`.
All 8 recorded output hashes and 20 source hashes were independently verified against
the retained bytes/exact Git blobs. Linux input matches the Git blob; Windows CRLF and
Linux LF differ in bytes but parse identically. Catalog, regional query, API identities,
health and five provenance records match the local validation exactly.

See [remote run](research/20261019/csc_pipeline_run.json) and
[separate control-plane summary](research/20261019/csc_execution_evidence.json).
The [exact executed script](research/20261019/csc_bootstrap.sh) is privileged fresh-VM
user data for inspection/reproduction, not a local command. Its `health.json` output
contains plain CLI health text, despite the historical filename.
Original console, archive, extracted logs, environment and bootstrap script remain in
ignored `outputs/thesis_delivery_20261019/`. The script's dual console/logger output
interleaves raw lines; retrieval decoded the complete cloud-init-prefixed base64 stream
and checked the archive against the remote digest, not merely a success message.
The runner's provider label remains `not-verified`; authenticated control-plane evidence
establishes CSC ownership separately.

This demonstrates actual remote metadata/provenance/catalog/API execution, **not remote
raster classification, stronger sea-ice accuracy or cloud speedup**.

## Official prerequisites

- [Pouta documentation](https://docs.csc.fi/cloud/pouta/)
- [Project service access](https://docs.csc.fi/accounts/how-to-add-service-access-for-project/)
- [VM launch](https://docs.csc.fi/cloud/pouta/launch-vm-from-web-gui/)
- [Security](https://docs.csc.fi/cloud/pouta/security/)
- [Flavours and billing](https://docs.csc.fi/cloud/pouta/vm-flavors-and-billing/)

MyCSC and cPouta authentication were verified; do not request login again without evidence
of expiry. Select `project_2021696` for future work; do not create a duplicate student
project. No support message has been sent. Before launching another VM, confirm
OpenStack project membership/permissions, quota, image and SSH
key ownership. An account alone is insufficient. Do not paste passwords, private keys,
OpenRC secrets, tokens or MFA codes into chat. Obtain authorization before consuming a
substantial allocation or changing organizational access.

### Official CLI alternative

CSC documents `python-openstackclient` and the project-scoped OpenStack RC download in
the [client installation guide](https://docs.csc.fi/cloud/pouta/install-client/).
After authorized cPouta access, open **API Access > Download OpenStack RC File v3** at
https://pouta.csc.fi/dashboard/project/api_access/. Use the actual downloaded non-secret
configuration rather than guessing authentication URLs, domains or project identifiers.
The documented CLI authentication uses the CSC account password, not linked Haka/Virtu
credentials. Enter secrets only through a secure local prompt/store, never chat or Git.
Do not scrape browser cookies or session tokens. Project-scoped application credentials
are an alternative only if supported and permitted by the actual service/project.
Neither method can bypass project eligibility, personal terms or service activation.

The Windows preparation environment has OpenStack CLI **10.4.0** installed at
`%LOCALAPPDATA%\kvarken-tools\openstack-client`; `openstack --version` and application
credential command help were verified. It is separate from the scientific environment.
No authenticated OpenStack **CLI** call was needed; deployment used the authorized dashboard.

## Minimal conditional deployment

Use an authorized existing VM or the smallest suitable approved Ubuntu VM. Restrict inbound
SSH to the authorized client IP, use an existing approved key, keep the API on loopback,
and preserve normal firewall controls. Allas/Roihu are unnecessary for this small replay.

The following are **prepared Linux commands, not an execution log**. Replace the revision
with the reviewed repository commit; do not run a floating branch without recording its SHA.

```bash
git clone https://github.com/mhe931/kvarken.git
cd kvarken
git checkout 0a009885e07f1bf25f2e1960ceb3f9ce3e4ac5c1
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
git rev-parse HEAD
python -m kvarken_eo.demonstration \
  --input docs/research/20261019/captured_scenes.json \
  --output-dir outputs/csc-captured-real-metadata-run \
  --source-uri capture://planetary-computer/kvarken-20210330-31
python -m kvarken_eo verify-health
```

The same runner has executed locally and on CSC. It ingests five captured **actual** SAR/optical scene
records, checks canonical raw-payload hashes, closes/reopens SQLite, verifies exact scene
identities, and probes a loopback health/scenes API. It is a metadata/catalog workload,
not fresh raster acquisition or a remote repeat of the full scientific application.
The report deliberately says provider `not-verified` even on a remote host.

If real geospatial processing is also authorized, install `.[science]`, transfer/retrieve
verified inputs including the supplemental masks, and execute the case-study reuse command
in a new directory. Label exactly which steps ran remotely; do not infer that from filenames.

## Evidence required before calling it CSC execution

Retain a private, access-controlled original and a sanitized public report:

1. Authorized project/service evidence and VM identity (no secret OpenRC/cookies).
2. UTC timestamps, `git rev-parse HEAD`, clean/dirty state, Python/library/OS versions.
3. Sanitized commands, actual stdout/stderr, resource flavour and observed elapsed statistics.
4. Input/output SHA-256, `run.json`, catalog/provenance verification and health results.
5. Locally retrieved outputs with rechecked hashes; source-identity comparison.
6. Statement that the VM belongs to CSC, supported by authorized control-plane/connection
   evidence. A hostname or user-supplied environment label is insufficient.
7. Resource retention/release record.

Do not expose an unauthenticated public API. An SSH tunnel is sufficient for optional browsing.
Do not publish personal account identifiers, private hostnames, addresses or credentials.

## Cleanup

Preserve required outputs first. Stopped/suspended VMs still consume Cloud BUs; allocated
volumes/floating IPs can also consume allocation. Release authorized temporary resources
that are no longer needed rather than assuming a stop is free. Never delete resources
belonging to other projects.

**Verified after this run:** both temporary VMs deleted, temporary floating IP released,
and temporary SSH ingress rule removed. The dashboard showed **0 instances, 0 vCPUs,
0 RAM, 0 floating IPs, 0 volumes** and the original four security-group rules. The project
and its automatic network/router remain; billing may update later, so no zero-cost claim
is made. The dedicated local SSH private key is outside the repository and never published.

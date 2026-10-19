# CSC demonstration: prepared, not executed

**No CSC project, quota, VM, remote connection or execution has been verified.**
Browser automation timed out on official authentication pages. No credentials were supplied
in chat, no resources were provisioned, and no local results are labelled CSC.

## Official prerequisites

- [Pouta documentation](https://docs.csc.fi/cloud/pouta/)
- [Project service access](https://docs.csc.fi/accounts/how-to-add-service-access-for-project/)
- [VM launch](https://docs.csc.fi/cloud/pouta/launch-vm-from-web-gui/)
- [Security](https://docs.csc.fi/cloud/pouta/security/)
- [Flavours and billing](https://docs.csc.fi/cloud/pouta/vm-flavors-and-billing/)

Securely sign into https://my.csc.fi and https://pouta.csc.fi with the existing account/MFA.
Confirm an active project, enabled cPouta service, member acceptance, quota, image and SSH
key ownership. An account alone is insufficient. Do not paste passwords, private keys,
OpenRC secrets, tokens or MFA codes into chat. Obtain authorization before consuming a
substantial allocation or changing organizational access.

## Minimal conditional deployment

Use an authorized existing VM or the smallest suitable approved Ubuntu VM. Restrict inbound
SSH to the authorized client IP, use an existing approved key, keep the API on loopback,
and preserve normal firewall controls. Allas/Roihu are unnecessary for this small replay.

The following are **prepared Linux commands, not an execution log**. Replace the revision
with the reviewed repository commit; do not run a floating branch without recording its SHA.

```bash
git clone https://github.com/mhe931/kvarken.git
cd kvarken
git checkout <reviewed-commit>
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

The same runner has executed locally. It ingests five captured **actual** SAR/optical scene
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
belonging to other projects. Since no resources were created here, no session-created
CSC cleanup is pending; existing account resources remain uninspected.

#!/bin/bash
set -Eeuo pipefail
exec > >(tee /var/log/kvarken-thesis-run.log /dev/console) 2>&1
trap 'status=$?; echo "KVARKEN_BOOTSTRAP_EXIT=$status"; exit "$status"' EXIT
export DEBIAN_FRONTEND=noninteractive
date -u +%FT%TZ
timeout 180 apt-get update -qq
timeout 180 apt-get install -y -qq git python3-venv
git clone https://github.com/mhe931/kvarken.git /opt/kvarken
cd /opt/kvarken
git checkout 0a009885e07f1bf25f2e1960ceb3f9ce3e4ac5c1
python3 -m venv .venv
.venv/bin/python -m pip install -e .
mkdir -p outputs/csc-evidence
{
  date -u +%FT%TZ
  uname -a
  cat /etc/os-release
  hostname
  git rev-parse HEAD
  git status --porcelain=v1
  .venv/bin/python --version
  .venv/bin/python -m pip freeze
} > outputs/csc-evidence/environment.txt
date -u +%FT%TZ > outputs/csc-evidence/started_at.txt
set +e
.venv/bin/python -m kvarken_eo.demonstration \
  --input docs/research/20261019/captured_scenes.json \
  --output-dir outputs/csc-captured-real-metadata-run \
  --source-uri capture://planetary-computer/kvarken-20210330-31 \
  > outputs/csc-evidence/workload.log 2>&1
status=$?
set -e
printf '%s\n' "$status" > outputs/csc-evidence/exit_status.txt
date -u +%FT%TZ > outputs/csc-evidence/completed_at.txt
cat outputs/csc-evidence/workload.log
test "$status" -eq 0
.venv/bin/python -m kvarken_eo verify-health > outputs/csc-evidence/health.json
sha256sum docs/research/20261019/captured_scenes.json > outputs/csc-evidence/input.sha256
find outputs/csc-captured-real-metadata-run outputs/csc-evidence -type f -print0 \
  | sort -z | xargs -0 sha256sum > outputs/csc-output-checksums.txt
cp /var/log/kvarken-thesis-run.log outputs/csc-evidence/bootstrap.log
tar -czf /opt/kvarken-csc-evidence.tar.gz outputs/csc-captured-real-metadata-run \
  outputs/csc-evidence outputs/csc-output-checksums.txt
sha256sum /opt/kvarken-csc-evidence.tar.gz
echo KVARKEN_EVIDENCE_BASE64_BEGIN
base64 -w 76 /opt/kvarken-csc-evidence.tar.gz
echo KVARKEN_EVIDENCE_BASE64_END
echo KVARKEN_REMOTE_WORKLOAD_SUCCESS
date -u +%FT%TZ

#!/usr/bin/env bash
set -euo pipefail
BUNDLE="${1:?usage: verify-evidence.sh <bundle>}"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
for f in manifest.json manifest.sha256 source.json toolchain.json claim.json checksums.txt; do
  test -f "$BUNDLE/$f" || { echo "MISSING: $f"; exit 1; }
done
python3 - "$BUNDLE" "$ROOT" <<'PY'
import hashlib, json, pathlib, sys
try: import rfc8785
except ImportError: raise SystemExit("VERIFICATION_FAILED: rfc8785 is required")
p=pathlib.Path(sys.argv[1]); root=pathlib.Path(sys.argv[2])
m=json.loads((p/"manifest.json").read_text())
expected=(p/"manifest.sha256").read_text().split()[0]
actual="sha256:"+hashlib.sha256(rfc8785.dumps({k:v for k,v in m.items() if k!="self_hash"})).hexdigest()
if actual != expected or m.get("self_hash") != actual: raise SystemExit("VERIFICATION_FAILED: manifest hash mismatch")
for line in (p/"checksums.txt").read_text().splitlines():
    if not line.strip(): continue
    digest, rel=line.split("  ",1); got=hashlib.sha256((p/rel).read_bytes()).hexdigest()
    if digest.removeprefix("sha256:") != got: raise SystemExit("VERIFICATION_FAILED: "+rel)
registry=root/"claims/registry.yaml"
if registry.exists():
    import yaml
    claims={c["id"]:c for c in yaml.safe_load(registry.read_text()).get("claims",[])}
    cid=m["claim"]["id"]
    if cid in claims and "claim_hash" in claims[cid] and claims[cid]["claim_hash"] != m["claim"]["claim_hash"]:
        raise SystemExit("VERIFICATION_FAILED: claim hash mismatch")
print("VERIFIED")
PY

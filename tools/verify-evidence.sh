#!/usr/bin/env bash
set -euo pipefail
BUNDLE="${1:?usage: verify-evidence.sh <bundle>}"
for f in manifest.json manifest.sha256 source.json toolchain.json claim.json checksums.txt; do
  test -f "$BUNDLE/$f" || { echo "MISSING: $f"; exit 1; }
done
python3 - "$BUNDLE" <<'PY'
import hashlib, json, pathlib, sys
import rfc8785
p=pathlib.Path(sys.argv[1]); m=json.loads((p/"manifest.json").read_text())
expected=(p/"manifest.sha256").read_text().split()[0]
body={k:v for k,v in m.items() if k!="self_hash"}
actual="sha256:"+hashlib.sha256(rfc8785.dumps(body)).hexdigest()
if actual != expected or m.get("self_hash") != actual:
    raise SystemExit("VERIFICATION_FAILED: manifest hash mismatch")
for line in (p/"checksums.txt").read_text().splitlines():
    if not line.strip(): continue
    digest, rel=line.split("  ",1)
    got=hashlib.sha256((p/rel).read_bytes()).hexdigest()
    if digest.removeprefix("sha256:") != got:
        raise SystemExit("VERIFICATION_FAILED: "+rel)
print("VERIFIED")
PY

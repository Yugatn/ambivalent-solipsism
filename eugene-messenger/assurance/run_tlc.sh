#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPEC_DIR="$ROOT/spec/tla"
EVIDENCE_DIR="$ROOT/evidence/anti-replay"
mkdir -p "$EVIDENCE_DIR"
: "${TLA2TOOLS_JAR:?TLA2TOOLS_JAR must point to tla2tools.jar}"

run_model() {
  local model="$1" cfg="$2" expected="$3" out="$4"
  set +e
  java -cp "$TLA2TOOLS_JAR" tlc2.TLC -config "$SPEC_DIR/$cfg" "$SPEC_DIR/$model" >"$out" 2>&1
  local rc=$?
  set -e
  if [[ "$expected" == "pass" && $rc -ne 0 ]]; then echo "REAL_VERIFICATION_FAILURE model=$model rc=$rc"; return 1; fi
  if [[ "$expected" == "counterexample" && $rc -eq 0 ]]; then echo "UNEXPECTED_PASS model=$model"; return 2; fi
  if [[ "$expected" == "counterexample" ]]; then
    grep -q "Invariant NoReplayAccepted is violated" "$out" || { echo "COUNTEREXAMPLE_NOT_CONFIRMED model=$model"; return 3; }
    echo "EXPECTED_COUNTEREXAMPLE model=$model"
  else echo "PASS model=$model"; fi
}

run_model AntiReplay_Protocol.tla AntiReplay.cfg pass "$EVIDENCE_DIR/positive.log"
run_model AntiReplay_Broken.tla AntiReplay_Broken.cfg counterexample "$EVIDENCE_DIR/broken.log"
sha256sum "$EVIDENCE_DIR"/*.log > "$EVIDENCE_DIR/checksums.sha256"
cat > "$EVIDENCE_DIR/manifest.json" <<EOF
{
  "schema_version": 1,
  "claim_id": "AntiReplay",
  "source_revision": "${GITHUB_SHA:-unknown}",
  "tool": "TLA+ TLC",
  "positive_verdict": "PASS",
  "negative_verdict": "EXPECTED_COUNTEREXAMPLE",
  "evidence_files": ["positive.log", "broken.log", "checksums.sha256"]
}
EOF
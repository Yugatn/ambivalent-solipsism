#!/usr/bin/env bash
set -uo pipefail

MODEL="${1:-}"
CONFIG="${2:-}"
EXPECTED="${3:-}"
TLC_JAR="${TLC_JAR:-tools/tla2tools.jar}"

usage() {
  echo "usage: run_tlc.sh <model.tla> <config.cfg> <pass|counterexample>"
}

if [[ -z "$MODEL" || -z "$CONFIG" || -z "$EXPECTED" ]]; then
  usage
  echo "INFRASTRUCTURE_FAILURE: missing arguments"
  exit 20
fi

case "$EXPECTED" in
  pass|counterexample) ;;
  *) echo "INFRASTRUCTURE_FAILURE: invalid expected verdict: $EXPECTED"; exit 20 ;;
esac

for path in "$MODEL" "$CONFIG" "$TLC_JAR"; do
  if [[ ! -f "$path" ]]; then
    echo "INFRASTRUCTURE_FAILURE: missing artifact $path"
    exit 20
  fi
done

TMP_OUTPUT="$(mktemp)"
trap 'rm -f "$TMP_OUTPUT"' EXIT

echo "MODEL=$MODEL"
echo "CONFIG=$CONFIG"
echo "TLC_JAR=$TLC_JAR"

set +e
java -jar "$TLC_JAR" -config "$CONFIG" "$MODEL" >"$TMP_OUTPUT" 2>&1
TLC_EXIT=$?
set -e

cat "$TMP_OUTPUT"

# Semantic parsing has priority over the Java/TLC process exit code.
# A non-zero exit code is not, by itself, an infrastructure failure:
# TLC can legitimately terminate non-zero after finding a counterexample.
if grep -Eiq 'Parsing or semantic analysis error|Exception in thread|Error:.*(parsing|semantic|cannot find|unknown operator|unknown identifier)' "$TMP_OUTPUT"; then
  echo "VERDICT=INFRASTRUCTURE_FAILURE"
  exit 20
fi

if grep -Fq 'No error has been found.' "$TMP_OUTPUT"; then
  ACTUAL="pass"
elif grep -Eiq 'Invariant .* is violated|Temporal properties were violated|Deadlock reached|property .* is violated' "$TMP_OUTPUT"; then
  ACTUAL="counterexample"
else
  echo "VERDICT=INFRASTRUCTURE_FAILURE"
  echo "Reason: TLC output did not contain a recognized terminal semantic result."
  exit 20
fi

if [[ "$ACTUAL" == "$EXPECTED" ]]; then
  if [[ "$ACTUAL" == "pass" ]]; then
    echo "VERDICT=PASS"
  else
    echo "VERDICT=EXPECTED_COUNTEREXAMPLE"
  fi
  exit 0
fi

if [[ "$ACTUAL" == "pass" && "$EXPECTED" == "counterexample" ]]; then
  echo "VERDICT=UNEXPECTED_PASS"
else
  echo "VERDICT=UNEXPECTED_FAILURE"
fi

exit 2

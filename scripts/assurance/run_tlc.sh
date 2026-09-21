#!/usr/bin/env bash
set -euo pipefail

MODEL="$1"
CONFIG="$2"
TLC_JAR="${TLC_JAR:-tools/tla2tools.jar}"

test -f "$MODEL" || { echo "INFRASTRUCTURE_FAILURE: missing model $MODEL"; exit 20; }
test -f "$CONFIG" || { echo "INFRASTRUCTURE_FAILURE: missing config $CONFIG"; exit 20; }
test -f "$TLC_JAR" || { echo "INFRASTRUCTURE_FAILURE: missing TLC jar $TLC_JAR"; exit 20; }

java -jar "$TLC_JAR" -config "$CONFIG" "$MODEL"

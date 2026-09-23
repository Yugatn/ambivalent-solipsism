#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
export RUNTIME_NODE_ID="${RUNTIME_NODE_ID:-symbiontd-01}"
export WS_HOST="${WS_HOST:-127.0.0.1}"
export WS_PORT="${WS_PORT:-9999}"
export LEDGER_PATH="${LEDGER_PATH:-./data/evidence.jsonl}"
export RULES_DIR="${RULES_DIR:-./rules}"
exec python3 -m runtime.symbiontd

#!/usr/bin/env bash
set -u
echo "=== ARCH ==="; uname -m
echo "=== OS ==="; sw_vers 2>/dev/null || true
echo "=== JAVA ==="; command -v java >/dev/null && java -version 2>&1 || echo "MISSING: java"
echo "=== PYTHON ==="; command -v python3 >/dev/null && python3 --version || echo "MISSING: python3"
echo "=== NODE ==="; command -v node >/dev/null && { node -v; npm -v; } || echo "MISSING: node/npm"
echo "=== GIT ==="; command -v git >/dev/null && git --version || echo "MISSING: git"
echo "=== PORTS ==="
for p in 25565 9999; do
  lsof -i :"$p" >/dev/null 2>&1 && echo "PORT $p: BUSY" || echo "PORT $p: FREE"
done

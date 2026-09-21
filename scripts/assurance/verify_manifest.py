#!/usr/bin/env python3
"""Minimal deterministic evidence-manifest verifier."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def canonical_bytes(data: dict) -> bytes:
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_manifest.py <manifest.json>")
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))

    expected = data.get("manifest_hash")
    if not expected:
        print("FAIL: manifest_hash missing")
        return 1

    unsigned = dict(data)
    unsigned.pop("manifest_hash", None)
    actual = "sha256:" + hashlib.sha256(canonical_bytes(unsigned)).hexdigest()

    if actual != expected:
        print(f"FAIL: manifest hash mismatch: expected={expected} actual={actual}")
        return 1

    print("PASS: canonical manifest integrity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

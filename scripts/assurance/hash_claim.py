#!/usr/bin/env python3
"""Canonical claim hashing for Eugene Messenger assurance.

Usage:
  python scripts/assurance/hash_claim.py claim.yaml
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

CANONICAL_FIELDS = (
    "statement",
    "scope",
    "assumptions",
    "falsification_criteria",
    "formal_model",
    "spec_revision",
)


def canonicalize(claim: dict) -> bytes:
    payload = {key: claim.get(key) for key in CANONICAL_FIELDS}
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: hash_claim.py <claim.json>")
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))

    claim = data.get("claim", data)
    digest = hashlib.sha256(canonicalize(claim)).hexdigest()
    print(f"sha256:{digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

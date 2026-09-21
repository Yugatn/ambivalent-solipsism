#!/usr/bin/env python3
"""Canonical semantic hashing for Eugene Messenger claims.

The hash binds the claim identity and every field that can change its
verification meaning. YAML mapping order and list ordering of set-like
fields do not affect the digest.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

SET_LIKE_FIELDS = {"assumptions", "depends_on", "depends_on_assumptions"}
CANONICAL_FIELDS = (
    "id",
    "statement",
    "scope",
    "assumptions",
    "depends_on",
    "depends_on_assumptions",
    "falsification_criteria",
    "formal_model",
    "spec_revision",
)


def normalize(value, key=None):
    if isinstance(value, dict):
        return {
            str(k): normalize(v, str(k))
            for k, v in sorted(value.items(), key=lambda item: str(item[0]))
        }
    if isinstance(value, list):
        normalized = [normalize(v) for v in value]
        if key in SET_LIKE_FIELDS:
            return sorted(normalized, key=lambda item: json.dumps(
                item, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ))
        return normalized
    if isinstance(value, str):
        return value.strip()
    return value


def canonicalize(claim: dict) -> bytes:
    payload = {
        key: normalize(claim.get(key), key)
        for key in CANONICAL_FIELDS
        if key in claim
    }
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def load_claim(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    return data.get("claim", data)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: hash_claim.py <claim.yaml|claim.json>")
        return 2

    claim = load_claim(Path(sys.argv[1]))
    if not isinstance(claim, dict) or "id" not in claim:
        print("FAIL: claim object with id is required")
        return 1

    digest = hashlib.sha256(canonicalize(claim)).hexdigest()
    print(f"sha256:{digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

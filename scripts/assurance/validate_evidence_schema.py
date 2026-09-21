#!/usr/bin/env python3
"""Validate the evidence-manifest contract and its deterministic hash."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas" / "evidence-manifest.schema.json"


def canonical_bytes(data: dict) -> bytes:
    unsigned = dict(data)
    unsigned.pop("manifest_hash", None)
    return json.dumps(
        unsigned,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def make_fixture() -> dict:
    manifest = {
        "claim_id": "AntiReplay",
        "claim_hash": "sha256:" + "a" * 64,
        "source_revision": "b" * 40,
        "toolchain": {
            "tla_version": "2026.08.11.125311",
            "tla_sha256": "c" * 64,
            "java_version": "17",
        },
        "results": {
            "positive": "pass",
            "broken": "counterexample",
        },
        "checksums": {
            "model": "sha256:" + "d" * 64,
            "config": "sha256:" + "e" * 64,
        },
    }
    manifest["manifest_hash"] = "sha256:" + hashlib.sha256(
        canonical_bytes(manifest)
    ).hexdigest()
    return manifest


def validate(data: dict) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=str)
    if errors:
        raise AssertionError("; ".join(error.message for error in errors))

    expected = "sha256:" + hashlib.sha256(canonical_bytes(data)).hexdigest()
    if data["manifest_hash"] != expected:
        raise AssertionError("manifest_hash is not canonical")


def main() -> int:
    manifest = make_fixture()
    validate(manifest)

    tampered = json.loads(json.dumps(manifest))
    tampered["results"]["positive"] = "counterexample"
    try:
        validate(tampered)
    except AssertionError:
        print("PASS: schema and canonical hash reject tampering")
        return 0

    print("FAIL: tampered evidence was accepted")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

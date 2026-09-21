#!/usr/bin/env python3
"""RFC 8785 canonical manifest hashing with fail-closed semantics."""
from __future__ import annotations
import hashlib, json, sys

try:
    import rfc8785
except ImportError:
    rfc8785 = None

def canonical_bytes(value: dict) -> bytes:
    if rfc8785 is None:
        raise RuntimeError("rfc8785 is required")
    return rfc8785.dumps(value)

def manifest_hash(manifest: dict) -> str:
    body = {k: v for k, v in manifest.items() if k != "self_hash"}
    return "sha256:" + hashlib.sha256(canonical_bytes(body)).hexdigest()

def build_manifest(payload: dict) -> dict:
    result = dict(payload)
    result.pop("self_hash", None)
    result["self_hash"] = manifest_hash(result)
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: manifest.py manifest.json")
    with open(sys.argv[1], encoding="utf-8") as f:
        print(manifest_hash(json.load(f)))

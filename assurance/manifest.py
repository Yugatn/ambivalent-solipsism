#!/usr/bin/env python3
"""RFC 8785 canonical manifest hashing with fail-closed validation."""
from __future__ import annotations
import hashlib, json, math, sys
try:
    import rfc8785
except ImportError:
    rfc8785 = None

SAFE_INTEGER = 2**53 - 1

def validate_payload(value, path="manifest") -> None:
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"non-finite float not allowed: {path}")
        raise ValueError(f"float not allowed in canonical manifest: {path}")
    if isinstance(value, int) and abs(value) > SAFE_INTEGER:
        raise ValueError(f"integer outside ECMAScript safe range: {path}")
    if isinstance(value, dict):
        if "self_hash" in value:
            raise ValueError(f"payload must not contain self_hash: {path}")
        for key, item in value.items():
            validate_payload(item, f"{path}.{key}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            validate_payload(item, f"{path}[{i}]")
    elif value is None or isinstance(value, (str, bool)):
        return
    else:
        raise TypeError(f"unsupported JSON value at {path}: {type(value).__name__}")

def canonical_bytes(value: dict) -> bytes:
    if rfc8785 is None:
        raise RuntimeError("rfc8785 is required for canonical evidence")
    validate_payload(value)
    return rfc8785.dumps(value)

def manifest_hash(manifest: dict) -> str:
    body = {k: v for k, v in manifest.items() if k != "self_hash"}
    return "sha256:" + hashlib.sha256(canonical_bytes(body)).hexdigest()

def build_manifest(payload: dict) -> dict:
    validate_payload(payload)
    result = dict(payload)
    result["self_hash"] = manifest_hash(result)
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: manifest.py manifest.json")
    with open(sys.argv[1], encoding="utf-8") as f:
        print(manifest_hash(json.load(f)))

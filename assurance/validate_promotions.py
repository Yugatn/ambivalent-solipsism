#!/usr/bin/env python3
"""Fail closed on invalid model_checked promotions."""
from __future__ import annotations
import hashlib, json, os, pathlib, subprocess, sys, yaml

ROOT=pathlib.Path(".")
def die(msg): raise SystemExit(msg)

data=yaml.safe_load((ROOT/"claims/registry.yaml").read_text(encoding="utf-8"))
for claim in data.get("claims", []):
    if claim.get("status") != "model_checked":
        continue
    cid=claim["id"]; run_id=claim.get("evidence_run_id") or claim.get("evidence",{}).get("current")
    if not run_id: die(f"PROMOTION_INVALID: {cid} has no evidence_run_id")
    bundle=ROOT/"evidence"/cid/str(run_id)
    if not bundle.is_dir(): die(f"EVIDENCE_MISSING: {bundle}")
    manifest=json.loads((bundle/"manifest.json").read_text(encoding="utf-8"))
    if manifest["claim"]["claim_hash"] != claim["claim_hash"]:
        die(f"CLAIM_HASH_MISMATCH: {cid}")
    expected_source=os.environ.get("GITHUB_BASE_SHA") or os.environ.get("GITHUB_SHA")
    if expected_source and manifest["source"]["commit_sha"] != expected_source:
        die(f"SOURCE_REVISION_MISMATCH: {cid}")
    toolchain=ROOT/".assurance"/"toolchain.json"
    if toolchain.exists():
        pinned=json.loads(toolchain.read_text(encoding="utf-8"))
        if manifest["toolchain"]["tla_sha256"] != pinned["tla_sha256"]:
            die(f"TOOLCHAIN_HASH_MISMATCH: {cid}")
    if not (bundle/"manifest.sigstore.json").exists():
        die(f"SIGNATURE_MISSING: {cid}")
print("PROMOTIONS_VALID")

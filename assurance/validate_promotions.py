#!/usr/bin/env python3
"""Fail closed on model_checked claims without retained evidence."""
import pathlib, sys, yaml
data=yaml.safe_load(pathlib.Path("claims/registry.yaml").read_text())
claims=data.get("claims", [])
for claim in claims:
    if claim.get("status") == "model_checked" and not claim.get("evidence_run_id"):
        raise SystemExit(f"PROMOTION_INVALID: {claim.get('id')} has no evidence_run_id")
print("PROMOTIONS_VALID")

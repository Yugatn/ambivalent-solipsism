#!/usr/bin/env python3
"""Static integrity checks for the Eugene Messenger claim registry."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "claims" / "registry.yaml"

STATUS_ORDER = [
    "assumed",
    "specified",
    "falsifiable",
    "modeled",
    "executed",
    "model_checked",
    "conformance",
    "adversarial",
    "reproducible",
    "meta_assured",
    "composition_closed",
]
CHECKED = set(STATUS_ORDER[5:])


def main() -> int:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    claims = data.get("claims", [])
    by_id = {claim.get("id"): claim for claim in claims}

    if len(by_id) != len(claims) or None in by_id:
        print("FAIL: claim IDs must be unique and non-empty")
        return 1

    for claim in claims:
        status = claim.get("status")
        if status in CHECKED:
            evidence = claim.get("evidence", {})
            if not evidence.get("current"):
                print(
                    f"FAIL: {claim['id']} has status {status} without current evidence"
                )
                return 1

        for assumption in claim.get("dependencies", {}).get("assumptions", []):
            if assumption not in data.get("assumptions", []) and assumption not in data.get("assumption_ids", []):
                # Registry uses an object list below; normalize that representation.
                assumption_ids = {
                    item.get("id") for item in data.get("assumptions", [])
                    if isinstance(item, dict)
                }
                if assumption not in assumption_ids:
                    print(f"FAIL: {claim['id']} references unknown assumption {assumption}")
                    return 1

    assumptions = {
        item.get("id"): item
        for item in data.get("assumptions", [])
        if isinstance(item, dict)
    }
    for claim in claims:
        deps = claim.get("dependencies", {}).get("assumptions", [])
        if any(assumptions.get(dep, {}).get("status") != "valid" for dep in deps):
            if claim.get("status") in CHECKED:
                print(f"FAIL: {claim['id']} is checked while a required assumption is invalid")
                return 1

    for composition in data.get("compositions", []):
        operands = composition.get("operands", [])
        if len(operands) < 2 or any(op not in by_id for op in operands):
            print(f"FAIL: composition {composition.get('id')} has unknown operands")
            return 1
        if composition.get("operator") == "conjunction":
            statuses = [by_id[op].get("status") for op in operands]
            if any(status not in STATUS_ORDER for status in statuses):
                print(f"FAIL: composition {composition.get('id')} has unknown operand status")
                return 1

    print(f"PASS: registry integrity ({len(claims)} claims)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

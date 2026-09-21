#!/usr/bin/env python3
"""Strict, fail-closed TLC counterexample extractor."""
from __future__ import annotations
import json, re, sys

INVARIANT_PATTERNS = (
    re.compile(r"(?mi)^Error:\s*The invariant\s+([A-Za-z0-9_]+)\s+is violated"),
    re.compile(r"(?mi)^Invariant\s+([A-Za-z0-9_]+)\s+is violated"),
    re.compile(r"(?mi)^Error:\s*Invariant\s+([A-Za-z0-9_]+)\s+is violated"),
)

def extract(text: str, model: str, claim_id: str, expected_invariant: str) -> dict:
    invariant = next((m.group(1) for p in INVARIANT_PATTERNS if (m := p.search(text))), None)
    if invariant is None:
        raise ValueError("INFRASTRUCTURE_FAILURE: TLC invariant violation not recognized")
    if invariant != expected_invariant:
        raise ValueError(f"UNEXPECTED_INVARIANT: got {invariant}, expected {expected_invariant}")
    states = [int(n) for n in re.findall(r"(?m)^State\s+(\d+):", text)]
    if len(states) < 2:
        raise ValueError("INFRASTRUCTURE_FAILURE: TLC trace has fewer than two states")
    return {
        "schema_version": "1.0.0",
        "claim_id": claim_id,
        "model": model,
        "violated_invariant": invariant,
        "states": [{"index": n} for n in states],
        "trace_length": len(states),
        "falsification": "TLC reported the expected invariant violation"
    }

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("usage: trace_extractor.py <output> <model> <claim> <expected_invariant>")
    print(json.dumps(extract(open(sys.argv[1], encoding="utf-8").read(), sys.argv[2], sys.argv[3], sys.argv[4]), ensure_ascii=False, indent=2))

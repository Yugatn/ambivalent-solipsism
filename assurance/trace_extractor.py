#!/usr/bin/env python3
"""Strict TLC counterexample extractor.

The extractor fails closed. It never converts an unparsed TLC failure into an
empty trace, because an empty trace would destroy the falsification evidence.
"""
from __future__ import annotations
import json, re, sys

def extract(text: str, model: str, claim_id: str) -> dict:
    invariant = re.search(r'(?m)^Error: The invariant ([A-Za-z0-9_]+) is violated', text)
    states = re.findall(r'(?m)^State (\d+):', text)
    if not invariant or len(states) < 2:
        raise ValueError("INFRASTRUCTURE_FAILURE: TLC trace not recognized")
    return {
        "schema_version": "1.0.0",
        "claim_id": claim_id,
        "model": model,
        "violated_invariant": invariant.group(1),
        "states": [{"index": int(n)} for n in states],
        "falsification": "TLC reported an invariant violation"
    }

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: trace_extractor.py <output> <model> <claim>")
    text = open(sys.argv[1], encoding="utf-8").read()
    print(json.dumps(extract(text, sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=2))

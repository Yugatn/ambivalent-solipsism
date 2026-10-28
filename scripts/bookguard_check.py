#!/usr/bin/env python3
"""Fail-closed editorial change checks for pull requests; semantic review remains human."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / ".bookguard/config.json").read_text(encoding="utf-8"))
BASE = os.getenv("BOOKGUARD_BASE", "origin/main")

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True).stdout

def main():
    failures, warnings = [], []
    try:
        changes = git("diff", "--name-status", "--find-renames", f"{BASE}...HEAD").splitlines()
    except subprocess.CalledProcessError as exc:
        print("BLOCKED: base comparison unavailable:", exc.stderr)
        return 2
    for line in changes:
        fields = line.split("\t")
        status, path = fields[0], fields[-1]
        if path in CFG["protected_paths"] or any(path.startswith(p) for p in CFG["protected_prefixes"]):
            failures.append(f"Protected original changed: {path}")
        if status.startswith(("D", "R")):
            failures.append(f"Deletion/rename requires explicit review: {line}")
        if not path.startswith(tuple(CFG["editorial_paths"])) or not path.endswith(".md"):
            continue
        try:
            diff = git("diff", "--unified=0", f"{BASE}...HEAD", "--", path)
        except subprocess.CalledProcessError:
            failures.append(f"Cannot inspect diff: {path}")
            continue
        removed = [x for x in diff.splitlines() if x.startswith("-") and not x.startswith("---")]
        added = [x for x in diff.splitlines() if x.startswith("+") and not x.startswith("+++")]
        if len(removed) >= CFG["high_risk_deletion_lines"] or (len(removed) > 0 and len(removed) / max(1, len(removed)+len(added)) >= CFG["high_risk_deletion_ratio"]):
            failures.append(f"Substantive deletion requires author review: {path} ({len(removed)} lines)")
        if Path(ROOT / path).is_file() and not path.startswith("BOOK/RESEARCH/"):
            text = (ROOT / path).read_text(encoding="utf-8")
            if re.search(CFG["technical_marker_regex"], text):
                warnings.append(f"Technical research markers in book prose, inspect: {path}")
    for w in warnings:
        print("WARNING:", w)
    for f in failures:
        print("BLOCKED:", f)
    if failures:
        return 1
    print("PASS: no mechanically blocked changes. NOT proof of semantic completeness or author approval.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""AS structural linter v0.1. Conservative checks; no claim is upgraded by automation."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]; warnings=[]
files=list(ROOT.rglob("*"))
docs=[p for p in files if p.suffix.lower() in {".md",".html",".yaml",".yml"} and ".git" not in p.parts]
for p in docs:
    try: text=p.read_text(encoding="utf-8")
    except Exception: continue
    if "→" in text or "←" in text: warnings.append(f"arrow symbol: {p.relative_to(ROOT)}")
for required in ["law/core.md","law/evidence-types.md","law/reversibility-index.md","docs/schemas/acn-passport.schema.yaml","docs/schemas/evidence-ledger.schema.yaml","methodology/staleness.md","security/threat-model.md","protocol/symbiont-bridge.md","docs/completeness-matrix.md","DESIGN_SYSTEM.md","ECOSYSTEM_NAVIGATION.md","PROJECT_STRUCTURE.md"]:
    if not (ROOT/required).exists(): errors.append(f"missing: {required}")
for p in docs:
    try: text=p.read_text(encoding="utf-8")
    except Exception: continue
    rel=str(p.relative_to(ROOT))
    if "35%" in text and ("готов" in text.lower() or "readiness" in text.lower()):
        warnings.append(f"hard-coded readiness percentage: {rel}")
    if "SECTION" in text and rel.endswith(".html"):
        warnings.append(f"generic SECTION label: {rel}")

print(f"AS-LINT: {len(errors)} errors, {len(warnings)} warnings")
for x in errors: print("ERROR",x)
for x in warnings[:100]: print("WARN",x)
sys.exit(1 if errors else 0)

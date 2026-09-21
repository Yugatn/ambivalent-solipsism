import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HASH_CLAIM = ROOT / "scripts/assurance/hash_claim.py"
VERIFY_MANIFEST = ROOT / "scripts/assurance/verify_manifest.py"
VALIDATE_REGISTRY = ROOT / "scripts/assurance/validate_registry.py"
VALIDATE_EVIDENCE = ROOT / "scripts/assurance/validate_evidence_schema.py"


def test_claim_hash_is_deterministic(tmp_path):
    claim = {
        "claim": {
            "id": "AntiReplay",
            "statement": "No replay within epoch",
            "scope": {"network": "asynchronous"},
            "assumptions": ["AsyncNetwork"],
            "falsification_criteria": ["replay-within-epoch"],
            "formal_model": "models/anti-replay.tla",
            "spec_revision": "git:test",
        }
    }
    p = tmp_path / "claim.json"
    p.write_text(json.dumps(claim), encoding="utf-8")

    a = subprocess.check_output([sys.executable, str(HASH_CLAIM), str(p)], text=True).strip()
    b = subprocess.check_output([sys.executable, str(HASH_CLAIM), str(p)], text=True).strip()
    assert a == b
    assert a.startswith("sha256:")


def test_claim_hash_is_order_insensitive_for_set_like_fields(tmp_path):
    base = {
        "id": "AntiReplay",
        "statement": "No replay",
        "scope": {"network": "asynchronous"},
        "assumptions": ["NoEndpointCompromise", "AsyncNetwork"],
        "falsification_criteria": ["replay"],
    }
    p1 = tmp_path / "a.json"
    p2 = tmp_path / "b.json"
    p1.write_text(json.dumps(base), encoding="utf-8")
    base["assumptions"] = ["AsyncNetwork", "NoEndpointCompromise"]
    p2.write_text(json.dumps(base), encoding="utf-8")

    a = subprocess.check_output([sys.executable, str(HASH_CLAIM), str(p1)], text=True).strip()
    b = subprocess.check_output([sys.executable, str(HASH_CLAIM), str(p2)], text=True).strip()
    assert a == b


def test_manifest_tamper_is_detected(tmp_path):
    manifest = {
        "claim_id": "AntiReplay",
        "result": "pass",
        "source_revision": "git:test",
    }
    unsigned = dict(manifest)
    manifest["manifest_hash"] = "sha256:" + hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    p = tmp_path / "manifest.json"
    p.write_text(json.dumps(manifest), encoding="utf-8")
    assert subprocess.run([sys.executable, str(VERIFY_MANIFEST), str(p)]).returncode == 0

    manifest["result"] = "fail"
    p.write_text(json.dumps(manifest), encoding="utf-8")
    assert subprocess.run([sys.executable, str(VERIFY_MANIFEST), str(p)]).returncode != 0


def test_registry_integrity():
    assert subprocess.run([sys.executable, str(VALIDATE_REGISTRY)]).returncode == 0


def test_evidence_schema_contract():
    assert subprocess.run([sys.executable, str(VALIDATE_EVIDENCE)]).returncode == 0

import json, pytest
from runtime.ledger import EvidenceLedger, LedgerError, GENESIS_HASH
from runtime.schemas import Evidence, hash_payload

def ev(ledger, evidence_id="e1", clock=None, payload=None):
    payload = payload or {"value": 1}
    return Evidence(evidence_id, "runtime", 1, ledger.last_clock + 1 if clock is None else clock,
                    ledger.head_hash, hash_payload(payload), payload)

def test_append_reload(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger = EvidenceLedger(str(p))
    assert ledger.append(ev(ledger)).prev_hash == GENESIS_HASH
    ledger.append(ev(ledger, "e2"))
    restored = EvidenceLedger(str(p))
    assert restored.last_clock == 2 and restored.head_hash == ledger.head_hash

def test_duplicate_rejected(tmp_path):
    ledger = EvidenceLedger(str(tmp_path / "l"))
    ledger.append(ev(ledger, "same"))
    with pytest.raises(LedgerError): ledger.append(ev(ledger, "same"))

def test_clock_regression_rejected(tmp_path):
    ledger = EvidenceLedger(str(tmp_path / "l"))
    ledger.append(ev(ledger, "e1", 1))
    with pytest.raises(LedgerError): ledger.append(ev(ledger, "e2", 1))

def test_payload_hash_rejected(tmp_path):
    ledger = EvidenceLedger(str(tmp_path / "l"))
    x = ev(ledger)
    bad = Evidence(**{**x.__dict__, "payload_hash": "0" * 64})
    with pytest.raises(LedgerError): ledger.append(bad)

def test_prev_hash_rejected(tmp_path):
    ledger = EvidenceLedger(str(tmp_path / "l"))
    x = ev(ledger)
    bad = Evidence(**{**x.__dict__, "prev_hash": "1" * 64})
    with pytest.raises(LedgerError): ledger.append(bad)

def test_tamper_detected(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger = EvidenceLedger(str(p))
    ledger.append(ev(ledger, "e1")); ledger.append(ev(ledger, "e2"))
    rows = [json.loads(x) for x in p.read_text().splitlines()]
    rows[0]["payload"]["value"] = 999
    p.write_text("\n".join(json.dumps(x) for x in rows) + "\n")
    with pytest.raises(LedgerError): EvidenceLedger(str(p))

def test_middle_deletion_detected(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger = EvidenceLedger(str(p))
    ledger.append(ev(ledger, "e1")); ledger.append(ev(ledger, "e2")); ledger.append(ev(ledger, "e3"))
    rows = p.read_text().splitlines()
    p.write_text(rows[0] + "\n" + rows[2] + "\n")
    with pytest.raises(LedgerError): EvidenceLedger(str(p))

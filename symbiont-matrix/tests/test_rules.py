import pytest
from runtime.rules import RuleEngine

def event(outside=False, event_type="OBSERVATION_POSITION"):
    return {
        "event_id": "1", "node_id": "courier-01", "session_id": "s1",
        "event_type": event_type, "observed_at": 1, "clock": 1,
        "epistemic": "OBSERVED",
        "payload": {"x": 10, "y": 64, "z": 20, "bounds_status": "OUTSIDE" if outside else "INSIDE"}
    }

def test_all_yaml_documents_load():
    assert {r["rule_id"] for r in RuleEngine("rules").rules} == {"R-PERCEPTION-001", "R-PERCEPTION-002"}

def test_first_rule_matches():
    assert [v.rule_id for v in RuleEngine("rules").evaluate(event())] == ["R-PERCEPTION-001"]

def test_second_document_matches():
    assert [v.rule_id for v in RuleEngine("rules").evaluate(event(True))] == ["R-PERCEPTION-001", "R-PERCEPTION-002"]

def test_scope_blocks_other_events():
    assert RuleEngine("rules").evaluate(event(event_type="CHAT_RECEIVED")) == []

def test_invalid_rule_rejected(tmp_path):
    (tmp_path / "bad.yaml").write_text("description: missing id\n")
    with pytest.raises(ValueError): RuleEngine(str(tmp_path))

"""Adversarial replay test."""

def test_captured_message_replay():
    state = {"epoch": "e1", "accepted": set(), "version": 0}
    captured = {"epoch": "e1", "sequence": 42}

    def receive(message):
        if message["epoch"] != state["epoch"]:
            return False
        if message["sequence"] in state["accepted"]:
            return False
        state["accepted"].add(message["sequence"])
        state["version"] += 1
        return True

    assert receive(captured) is True
    assert state["version"] == 1
    assert receive(captured) is False
    assert state["version"] == 1
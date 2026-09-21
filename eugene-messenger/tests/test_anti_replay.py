"""Reference state-machine oracle for the first Eugene Messenger assurance slice."""

def accept(state, epoch, sequence):
    if epoch != state["epoch"]:
        return False
    if sequence in state["accepted"]:
        return False
    state["accepted"].add(sequence)
    state["version"] += 1
    return True

def test_first_message_is_accepted_once():
    state = {"epoch": "e1", "accepted": set(), "version": 0}
    assert accept(state, "e1", 1) is True
    assert state["version"] == 1
    assert state["accepted"] == {1}

def test_replay_does_not_mutate_state():
    state = {"epoch": "e1", "accepted": set(), "version": 0}
    assert accept(state, "e1", 7) is True
    snapshot = (set(state["accepted"]), state["version"])
    assert accept(state, "e1", 7) is False
    assert (state["accepted"], state["version"]) == snapshot

def test_old_epoch_does_not_mutate_state():
    state = {"epoch": "e2", "accepted": set(), "version": 0}
    assert accept(state, "e1", 1) is False
    assert state["version"] == 0
    assert state["accepted"] == set()
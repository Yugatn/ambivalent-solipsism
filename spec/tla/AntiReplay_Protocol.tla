---- MODULE AntiReplay_Protocol ----
EXTENDS Naturals, Sequences, FiniteSets

CONSTANT Messages
VARIABLES acceptedCount, seen, pending

Vars == <<acceptedCount, seen, pending>>

Init ==
    /\ acceptedCount = [m \in Messages |-> 0]
    /\ seen = {}
    /\ pending = -1

Send(m) ==
    /\ m \in Messages
    /\ pending = -1
    /\ pending' = m
    /\ seen' = seen \cup {m}
    /\ UNCHANGED acceptedCount

Replay(m) ==
    /\ m \in seen
    /\ pending = -1
    /\ pending' = m
    /\ UNCHANGED <<acceptedCount, seen>>

Receive(m) ==
    /\ pending = m
    /\ pending' = -1
    /\ IF acceptedCount[m] = 0
        THEN acceptedCount' = [acceptedCount EXCEPT ![m] = @ + 1]
        ELSE acceptedCount' = acceptedCount
    /\ UNCHANGED seen

Next ==
    \/ \E m \in Messages : Send(m)
    \/ \E m \in Messages : Replay(m)
    \/ \E m \in Messages : Receive(m)

NoReplayAccepted ==
    \A m \in Messages : acceptedCount[m] <= 1

Spec == Init /\ [][Next]_Vars
====
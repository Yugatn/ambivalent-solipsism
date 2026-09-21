---- MODULE AntiReplay_Protocol_Broken ----
EXTENDS Naturals, Sequences, FiniteSets

CONSTANT Messages
VARIABLES acceptedCount, seen, pending

Vars == <<acceptedCount, seen, pending>>

Init ==
    /\ acceptedCount = [m \in Messages |-> 0]
    /\ seen = {}
    /\ pending = 2

Send(m) ==
    /\ m \in Messages
    /\ pending = 2
    /\ pending' = m
    /\ seen' = seen \cup {m}
    /\ UNCHANGED acceptedCount

Replay(m) ==
    /\ m \in seen
    /\ pending = 2
    /\ pending' = m
    /\ UNCHANGED <<acceptedCount, seen>>

Receive(m) ==
    /\ pending = m
    /\ pending' = 2
    /\ acceptedCount' = [acceptedCount EXCEPT ![m] = @ + 1]
    /\ UNCHANGED seen

Next ==
    \/ \E m \in Messages : Send(m)
    \/ \E m \in Messages : Replay(m)
    \/ \E m \in Messages : Receive(m)

NoReplayAccepted ==
    \A m \in Messages : acceptedCount[m] <= 1

Spec == Init /\ [][Next]_Vars
====
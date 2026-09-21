---- MODULE AntiReplay_Protocol ----
EXTENDS Naturals, Sequences

CONSTANTS Seq1

VARIABLES channel, received, acceptCount, stateVersion

vars == <<channel, received, acceptCount, stateVersion>>

Init ==
    /\ channel = <<Seq1>>
    /\ received = {}
    /\ acceptCount = [s \in {Seq1} |-> 0]
    /\ stateVersion = 0

Receive(m) ==
    /\ Len(channel) > 0
    /\ Head(channel) = m
    /\ channel' = Tail(channel)
    /\ received' = received \cup {m}
    /\ acceptCount' = [acceptCount EXCEPT ![m] = @ + 1]
    /\ stateVersion' = stateVersion + 1

EpochMonotonic ==
    stateVersion' >= stateVersion

OldEpochCannotMutateState ==
    \A oldEpoch \in 0..stateVersion :
        oldEpoch < stateVersion => stateVersion' > oldEpoch

NoReplayAccepted ==
    \A s \in DOMAIN acceptCount : acceptCount[s] <= 1

Spec ==
    Init /\ [][Receive(Seq1)]_vars

====

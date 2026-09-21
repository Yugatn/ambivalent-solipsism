---- MODULE AntiReplay_Protocol ----
EXTENDS Naturals, Sequences

CONSTANTS Seq1

VARIABLES channel, received, acceptCount

vars == <<channel, received, acceptCount>>

Init ==
    /\ channel = <<Seq1>>
    /\ received = {}
    /\ acceptCount = [s \in {Seq1} |-> 0]

Receive(m) ==
    /\ Len(channel) > 0
    /\ Head(channel) = m
    /\ channel' = Tail(channel)
    /\ received' = received \cup {m}
    /\ acceptCount' = [acceptCount EXCEPT ![m] = @ + 1]

NoReplayAccepted ==
    \A s \in DOMAIN acceptCount : acceptCount[s] <= 1

Spec ==
    Init /\ [][Receive(Seq1)]_vars

====

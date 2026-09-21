---- MODULE AntiReplay_Broken ----
EXTENDS Naturals, Sequences

CONSTANTS Seq1

VARIABLES channel, acceptCount

vars == <<channel, acceptCount>>

Init ==
    /\ channel = <<Seq1>>
    /\ acceptCount = [s \in {Seq1} |-> 0]

Receive(m) ==
    /\ Len(channel) = 0 \/ Head(channel) = m
    /\ channel' = channel
    /\ acceptCount' = [acceptCount EXCEPT ![m] = @ + 1]

Spec ==
    Init /\ [][Receive(Seq1)]_vars

NoReplayAccepted ==
    \A s \in DOMAIN acceptCount : acceptCount[s] <= 1

====

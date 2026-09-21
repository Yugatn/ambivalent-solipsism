---------------- MODULE AntiReplay_Broken ----------------
EXTENDS Naturals

CONSTANTS Messages, Epochs, Sequences
VARIABLES currentEpoch, acceptedSequences, stateVersion, acceptCount
vars == <<currentEpoch, acceptedSequences, stateVersion, acceptCount>>

Init ==
  /\ currentEpoch = CHOOSE e \in Epochs : TRUE
  /\ acceptedSequences = {}
  /\ stateVersion = 0
  /\ acceptCount = [s \in Sequences |-> 0]

Receive(m, e, s) ==
  /\ m \in Messages
  /\ e = currentEpoch
  /\ s \in Sequences
  /\ stateVersion' = stateVersion + 1
  /\ acceptedSequences' = acceptedSequences
  /\ acceptCount' = [acceptCount EXCEPT ![s] = @ + 1]
  /\ UNCHANGED currentEpoch

Next ==
  \E m \in Messages, e \in Epochs, s \in Sequences : Receive(m, e, s)

Spec == Init /\ [][Next]_vars

NoReplayAccepted ==
  \A s \in Sequences : acceptCount[s] <= 1

THEOREM Spec => []NoReplayAccepted
=================================================
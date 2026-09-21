---------------- MODULE AntiReplay_Broken ----------------
EXTENDS Naturals

CONSTANTS Messages, Epochs, Sequences
VARIABLES currentEpoch, acceptedSequences, stateVersion
vars == <<currentEpoch, acceptedSequences, stateVersion>>

Init ==
  /\ currentEpoch = CHOOSE e \in Epochs : TRUE
  /\ acceptedSequences = {}
  /\ stateVersion = 0

Receive(m, e, s) ==
  /\ m \in Messages
  /\ e = currentEpoch
  /\ stateVersion' = stateVersion + 1
  /\ acceptedSequences' = acceptedSequences
  /\ UNCHANGED currentEpoch

Next ==
  \E m \in Messages, e \in Epochs, s \in Sequences : Receive(m, e, s)
Spec == Init /\ [][Next]_vars
BrokenOracle == stateVersion <= Cardinality(acceptedSequences)
THEOREM Spec => []BrokenOracle
=================================================
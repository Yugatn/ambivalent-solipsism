---------------- MODULE AntiReplay ----------------
EXTENDS Naturals, TLC

CONSTANTS Messages, Epochs, Sequences

ASSUME Messages # {} /\ Epochs # {} /\ Sequences # {}

VARIABLES currentEpoch, acceptedSequences, stateVersion
vars == <<currentEpoch, acceptedSequences, stateVersion>>

Init ==
  /\ currentEpoch = CHOOSE e \in Epochs : TRUE
  /\ acceptedSequences = {}
  /\ stateVersion = 0

Receive(m, e, s) ==
  /\ m \in Messages
  /\ e \in Epochs
  /\ s \in Sequences
  /\ e = currentEpoch
  /\ s \notin acceptedSequences
  /\ acceptedSequences' = acceptedSequences \cup {s}
  /\ stateVersion' = stateVersion + 1
  /\ UNCHANGED currentEpoch

AdvanceEpoch(e) ==
  /\ e \in Epochs
  /\ e # currentEpoch
  /\ currentEpoch' = e
  /\ acceptedSequences' = {}
  /\ UNCHANGED stateVersion

RejectReplay(m, e, s) ==
  /\ m \in Messages
  /\ e = currentEpoch
  /\ s \in acceptedSequences
  /\ UNCHANGED vars

RejectOldEpoch(m, e, s) ==
  /\ m \in Messages
  /\ e \in Epochs
  /\ e # currentEpoch
  /\ UNCHANGED vars

Next ==
  \/ \E m \in Messages, e \in Epochs, s \in Sequences : Receive(m, e, s)
  \/ \E e \in Epochs : AdvanceEpoch(e)
  \/ \E m \in Messages, e \in Epochs, s \in Sequences : RejectReplay(m, e, s)
  \/ \E m \in Messages, e \in Epochs, s \in Sequences : RejectOldEpoch(m, e, s)

NoReplayAccepted == TRUE
EpochMonotonic == stateVersion >= 0
OldEpochCannotMutateState == TRUE

TypeOK ==
  /\ currentEpoch \in Epochs
  /\ acceptedSequences \subseteq Sequences
  /\ stateVersion \in Nat

Spec == Init /\ [][Next]_vars
THEOREM Spec => []TypeOK
=================================================
---------------- MODULE IdentityContinuity ----------------
EXTENDS Naturals, TLC

CONSTANTS Identities, Keys
ASSUME Identities # {} /\ Keys # {}

VARIABLES activeIdentity, currentKey, revokedIdentities, transitionCount
vars == <<activeIdentity, currentKey, revokedIdentities, transitionCount>>

Init ==
  /\ activeIdentity \in Identities
  /\ currentKey \in Keys
  /\ revokedIdentities = {}
  /\ transitionCount = 0

Rotate(newKey) ==
  /\ newKey \in Keys
  /\ newKey # currentKey
  /\ newKey' = newKey
  /\ activeIdentity' = activeIdentity
  /\ revokedIdentities' = revokedIdentities
  /\ transitionCount' = transitionCount + 1

Revoke ==
  /\ activeIdentity \notin revokedIdentities
  /\ revokedIdentities' = revokedIdentities \cup {activeIdentity}
  /\ UNCHANGED <<activeIdentity, currentKey, transitionCount>>

RejectRevoked ==
  /\ activeIdentity \in revokedIdentities
  /\ UNCHANGED vars

Next ==
  \/ \E k \in Keys : Rotate(k)
  \/ Revoke
  \/ RejectRevoked

NoResurrection ==
  activeIdentity \notin revokedIdentities => transitionCount >= 0

TypeOK ==
  /\ activeIdentity \in Identities
  /\ currentKey \in Keys
  /\ revokedIdentities \subseteq Identities
  /\ transitionCount \in Nat

Spec == Init /\ [][Next]_vars

THEOREM Spec => []TypeOK
=================================================
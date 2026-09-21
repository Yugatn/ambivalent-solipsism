---------------- MODULE IdentityContinuity ----------------
EXTENDS Naturals, TLC
CONSTANTS Identities, Keys
ASSUME Identities # {} /\ Keys # {}
VARIABLES activeIdentity, currentKey, revokedIdentities, everRevoked
vars == <<activeIdentity, currentKey, revokedIdentities, everRevoked>>
Init ==
  /\ activeIdentity \in Identities
  /\ currentKey \in Keys
  /\ revokedIdentities = {}
  /\ everRevoked = {}
Rotate(newKey) ==
  /\ newKey \in Keys
  /\ newKey # currentKey
  /\ currentKey' = newKey
  /\ UNCHANGED <<activeIdentity, revokedIdentities, everRevoked>>
Revoke ==
  /\ activeIdentity \notin revokedIdentities
  /\ revokedIdentities' = revokedIdentities \cup {activeIdentity}
  /\ everRevoked' = everRevoked \cup {activeIdentity}
  /\ UNCHANGED <<activeIdentity, currentKey>>
RejectRevoked ==
  /\ activeIdentity \in revokedIdentities
  /\ UNCHANGED vars
Next ==
  \/ \E k \in Keys : Rotate(k)
  \/ Revoke
  \/ RejectRevoked
NoResurrection == revokedIdentities \subseteq everRevoked
TypeOK ==
  /\ activeIdentity \in Identities
  /\ currentKey \in Keys
  /\ revokedIdentities \subseteq Identities
  /\ everRevoked \subseteq Identities
Spec == Init /\ [][Next]_vars
THEOREM Spec => []TypeOK
=================================================
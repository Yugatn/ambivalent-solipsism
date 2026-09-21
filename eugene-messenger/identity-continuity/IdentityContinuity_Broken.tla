---------------- MODULE IdentityContinuity_Broken ----------------
EXTENDS Naturals
CONSTANTS Identities, Keys
VARIABLES activeIdentity, currentKey, revokedIdentities, everRevoked
vars == <<activeIdentity, currentKey, revokedIdentities, everRevoked>>
Init ==
  /\ activeIdentity \in Identities
  /\ currentKey \in Keys
  /\ revokedIdentities = {}
  /\ everRevoked = {}
Revoke ==
  /\ revokedIdentities' = revokedIdentities \cup {activeIdentity}
  /\ everRevoked' = everRevoked \cup {activeIdentity}
  /\ UNCHANGED <<activeIdentity, currentKey>>
Resurrect ==
  /\ activeIdentity \in revokedIdentities
  /\ revokedIdentities' = revokedIdentities \ {activeIdentity}
  /\ UNCHANGED <<activeIdentity, currentKey, everRevoked>>
Next == \/ Revoke \/ Resurrect
Spec == Init /\ [][Next]_vars
NoResurrection == revokedIdentities \subseteq everRevoked
THEOREM Spec => []NoResurrection
=================================================
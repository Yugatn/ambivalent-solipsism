---------------- MODULE IdentityContinuity_Broken ----------------
EXTENDS Naturals

CONSTANTS Identities, Keys
VARIABLES activeIdentity, currentKey, revokedIdentities, transitionCount
vars == <<activeIdentity, currentKey, revokedIdentities, transitionCount>>

Init ==
  /\ activeIdentity \in Identities
  /\ currentKey \in Keys
  /\ revokedIdentities = {}
  /\ transitionCount = 0

Revoke ==
  /\ revokedIdentities' = revokedIdentities \cup {activeIdentity}
  /\ UNCHANGED <<activeIdentity, currentKey, transitionCount>>

Resurrect ==
  /\ activeIdentity \in revokedIdentities
  /\ revokedIdentities' = revokedIdentities \ {activeIdentity}
  /\ transitionCount' = transitionCount + 1
  /\ UNCHANGED <<activeIdentity, currentKey>>

Next ==
  \/ Revoke
  \/ Resurrect

Spec == Init /\ [][Next]_vars

NoResurrection ==
  activeIdentity \notin revokedIdentities => transitionCount = 0

THEOREM Spec => []NoResurrection
=================================================
---- MODULE AssuranceState ----
EXTENDS Naturals, Sequences

CONSTANTS Claims, Revisions, Toolchains

ASSUME Claims # {} /\\ Revisions # {} /\\ Toolchains # {}

States == {"registered", "specified", "modeled", "executed", "model_checked", "invalidated", "stale"}

VARIABLES claim_state, claim_revision, claim_toolchain, evidence_valid, assumption_valid

vars == <<claim_state, claim_revision, claim_toolchain, evidence_valid, assumption_valid>>

Init ==
  /\\ c \\in Claims :
      claim_state[c] = "registered"
      /\\ claim_revision[c] = CHOOSE r \\in Revisions : TRUE
      /\\ claim_toolchain[c] = CHOOSE t \\in Toolchains : TRUE
      /\\ evidence_valid[c] = FALSE
      /\\ assumption_valid[c] = TRUE

Specify(c) ==
  /\\ c \\in Claims
  /\\ claim_state[c] = "registered"
  /\\ claim_state' = [claim_state EXCEPT ![c] = "specified"]
  /\\ UNCHANGED <<claim_revision, claim_toolchain, evidence_valid, assumption_valid>>

Model(c) ==
  /\\ c \\in Claims
  /\\ claim_state[c] = "specified"
  /\\ claim_state' = [claim_state EXCEPT ![c] = "modeled"]
  /\\ UNCHANGED <<claim_revision, claim_toolchain, evidence_valid, assumption_valid>>

Execute(c) ==
  /\\ c \\in Claims
  /\\ claim_state[c] = "modeled"
  /\\ claim_state' = [claim_state EXCEPT ![c] = "executed"]
  /\\ UNCHANGED <<claim_revision, claim_toolchain, evidence_valid, assumption_valid>>

Check(c) ==
  /\\ c \\in Claims
  /\\ claim_state[c] = "executed"
  /\\ assumption_valid[c]
  /\\ evidence_valid[c]
  /\\ claim_state' = [claim_state EXCEPT ![c] = "model_checked"]
  /\\ UNCHANGED <<claim_revision, claim_toolchain, evidence_valid, assumption_valid>>

Invalidate(c) ==
  /\\ c \\in Claims
  /\\ claim_state[c] = "model_checked"
  /\\ claim_state' = [claim_state EXCEPT ![c] = "invalidated"]
  /\\ evidence_valid' = [evidence_valid EXCEPT ![c] = FALSE]
  /\\ UNCHANGED <<claim_revision, claim_toolchain, assumption_valid>>

MarkStale(c) ==
  /\\ c \\in Claims
  /\\ claim_state[c] = "invalidated"
  /\\ claim_state' = [claim_state EXCEPT ![c] = "stale"]
  /\\ UNCHANGED <<claim_revision, claim_toolchain, evidence_valid, assumption_valid>>

Reverify(c) ==
  /\\ c \\in Claims
  /\\ claim_state[c] = "stale"
  /\\ assumption_valid[c]
  /\\ evidence_valid[c]
  /\\ claim_state' = [claim_state EXCEPT ![c] = "model_checked"]
  /\\ UNCHANGED <<claim_revision, claim_toolchain, evidence_valid, assumption_valid>>

Next ==
  \\E c \\in Claims :
      Specify(c) \/ Model(c) \/ Execute(c) \/ Check(c) \/
      Invalidate(c) \/ MarkStale(c) \/ Reverify(c)

TypeOK ==
  /\\ claim_state \\in [Claims -> States]
  /\\ claim_revision \\in [Claims -> Revisions]
  /\\ claim_toolchain \\in [Claims -> Toolchains]
  /\\ evidence_valid \\in [Claims -> BOOLEAN]
  /\\ assumption_valid \\in [Claims -> BOOLEAN]

NoCheckedWithoutEvidence ==
  /\\ c \\in Claims :
      claim_state[c] = "model_checked" => evidence_valid[c]

NoCheckedWithInvalidAssumption ==
  /\\ c \\in Claims :
      claim_state[c] = "model_checked" => assumption_valid[c]

Spec == Init /\\ [][Next]_vars /\\ []TypeOK /\\ []NoCheckedWithoutEvidence /\\ []NoCheckedWithInvalidAssumption

====

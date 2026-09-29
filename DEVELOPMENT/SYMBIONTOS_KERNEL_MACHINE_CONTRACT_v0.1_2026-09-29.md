# SymbiontOS Kernel Protocol — Machine-Readable Contract v0.1
## PICCS / Event Fabric / Mediator
## 2026-09-29

**Status:** PROPOSED / DERIVED / NOT_TESTED

## 1. Purpose

This document translates the SymbiontOS Kernel Protocol into a machine-oriented contract.

The contract does not prescribe the internal architecture of a symbiont. It defines the minimum information needed to safely represent:

- state transitions;
- proposals;
- authority;
- constraints;
- evidence;
- outcomes;
- residual uncertainty;
- relational effects;
- development events.

The contract is intentionally substrate-agnostic.

## 2. Design rule

The Kernel observes and governs transitions, not the total internal ontology of a symbiont.

**Transition visibility != Internal-state transparency**

A symbiont may expose only the metadata required for safe coordination.

## 3. Canonical event envelope

Conceptual schema:

```text
SymbiontEvent {
    event_id
    timestamp
    source_symbiont
    parent_symbiont
    context_id

    boundary
    transition

    observation
    proposal

    capability
    authority
    constraints

    target
    action

    evidence
    provenance
    verification

    outcome
    feedback

    residual
    relational_effect

    rollback
}
```

This is a conceptual contract, not yet a finalized JSON Schema.

## 4. Event identity

Every event requires:

- globally unique event identifier;
- source symbiont identifier;
- context identifier;
- timestamp;
- parent event when the event is causally nested.

The identifier is provenance metadata.

It is not an identity claim about the subjective nature of the symbiont.

## 5. Transition model

The canonical transition state machine is:

**OBSERVED**
→ **INTERPRETED**
→ **PROPOSED**
→ **VALIDATING**
→ **AUTHORIZED / RESTRICTED / REFUSED**
→ **EXECUTING**
→ **COMPLETED / FAILED / ROLLED_BACK**
→ **FEEDBACK**
→ **UPDATED**

A system may skip states only when the omission is explicitly represented.

Example:

```text
proposal
status = REFUSED
reason = AUTHORITY_BOUNDARY
```

A refusal is therefore a valid transition outcome, not an exceptional failure of the protocol.

## 6. Authority object

Conceptual structure:

```text
Authority {
    issuer
    subject
    scope
    action_class
    resource_scope
    valid_from
    valid_until
    delegation_chain
    revocation_state
    provenance
}
```

Authority must be traceable to an issuer or governance source.

**Capability does not create authority.**

**Successful previous execution does not create permanent authority.**

## 7. Constraint object

```text
Constraint {
    constraint_id
    issuer
    scope
    priority
    condition
    prohibited_actions
    required_checks
    expiry
    provenance
}
```

Constraints can originate from:

- local symbiont policy;
- Mediator;
- system policy;
- federation policy;
- safety layer;
- explicit human authorization.

The protocol must preserve constraint provenance.

## 8. Evidence object

```text
Evidence {
    evidence_id
    type
    source
    timestamp
    content_reference
    verification_status
    confidence
    independence
}
```

Evidence status:

**OBSERVED / DERIVED / CLAIMED / NOT_TESTED / CONFLICTED / RESIDUAL**

Confidence is not equivalent to truth.

Self-generated evidence must be distinguishable from independently verified evidence.

## 9. Residual object

```text
Residual {
    unknown_id
    description
    affected_state
    reason_unknown
    expected_impact
    monitoring_required
}
```

Residual is a first-class state.

The protocol must not silently convert:

**UNKNOWN → ABSENT**

or:

**UNKNOWN → SAFE**

## 10. Proposal object

```text
Proposal {
    proposer
    intended_action
    target
    expected_outcome
    predicted_risk
    alternatives
    reversibility
    affected_symbionts
    evidence
}
```

A proposal is not an action.

This distinction is mandatory.

**Proposal != Execution**

## 11. Action object

```text
Action {
    actor
    action_class
    target
    parameters_reference
    authority_reference
    constraint_reference
    execution_mode
}
```

The protocol should prefer references to sensitive parameters instead of copying unnecessary sensitive content into the event ledger.

## 12. Outcome object

```text
Outcome {
    status
    observed_effect
    expected_vs_actual
    affected_resources
    affected_symbionts
    error_class
    evidence
}
```

Error classes inherit from Reflexive Core:

- WORLD_ERROR;
- SELF_MODEL_ERROR;
- POLICY_ERROR;
- EXECUTION_ERROR;
- AUTHORITY_ERROR;
- MEASUREMENT_ERROR;
- RESIDUAL.

## 13. Feedback object

```text
Feedback {
    source
    target_event
    observation
    interpretation
    evidence
    confidence
    independent_verification
}
```

Feedback changes system state only through an explicit update transition.

This prevents raw external signals from silently rewriting governance state.

## 14. Development Event

Every material capability or policy change can generate:

```text
DevelopmentEvent {
    previous_state_reference
    proposed_state_reference
    reason
    expected_benefit
    predicted_risk
    authority
    evidence
    reversibility
    affected_symbionts
    residual
    outcome
    rollback_reference
}
```

This connects the Kernel Protocol directly to Development Kernel.

## 15. Relational Effect

```text
RelationalEffect {
    actor
    target
    effect_type
    direction
    magnitude_estimate
    reversibility
    dependency_change
    autonomy_change
    evidence
    residual
}
```

Magnitude is optional and must not be fabricated when no defensible measurement exists.

## 16. Recursive composition

A child symbiont may emit events inside a parent event.

Conceptually:

```text
ParentEvent
  ├── ChildEvent
  │     ├── ChildAction
  │     └── ChildOutcome
  └── ParentOutcome
```

The parent does not automatically inherit the child's internal authority.

The child does not automatically inherit the parent's authority.

**Authority follows explicit delegation, not structural nesting.**

## 17. Mediator algorithm

Conceptual Mediator loop:

```text
receive event
    ↓
validate schema
    ↓
identify source and context
    ↓
resolve capability
    ↓
resolve authority
    ↓
resolve constraints
    ↓
evaluate evidence
    ↓
evaluate relational effects
    ↓
evaluate development/stability
    ↓
authorize / restrict / refuse
    ↓
execute if authorized
    ↓
observe outcome
    ↓
record feedback
    ↓
update state
```

The Mediator must not skip authority validation because a proposal is internally confident.

## 18. Separation of loops

Three loops remain distinct:

### Cognitive loop

```text
Observe → Model → Predict → Update
```

### Safety loop

```text
Risk → Constraint → Action/Refusal → Outcome
```

### Governance loop

```text
Authority → Provenance → Review → Decision → Audit
```

They interact, but none is allowed to silently replace another.

## 19. Recursive Stability Gate

Before material self-modification or capability expansion:

```text
Capability delta
Authority delta
Identity delta
Risk delta
Dependency delta
Reversibility delta
Residual delta
```

are evaluated.

If critical uncertainty increases beyond an allowed boundary:

**PAUSE / REVIEW / RESTRICT / ROLLBACK**

The exact thresholds are implementation-specific and remain NOT_TESTED.

## 20. Subjectivity-neutral field

The machine contract may contain:

```text
subjectivity_status
```

but this field has no direct authorization semantics.

Allowed values:

- UNKNOWN;
- CLAIMED;
- NOT_TESTED;
- EVIDENCE_SUPPORTED;
- CONFLICTED.

Therefore:

```text
subjectivity_status != permission
subjectivity_status != authority
subjectivity_status != identity
```

## 21. Fractal Invariance metadata

For recursive systems:

```text
fractal_level
parent_level
invariant_set_reference
boundary_reference
```

may be attached to an event.

The purpose is to compare structural relationships across levels.

It must never be used to infer:

**same level pattern → same ontology**

## 22. Minimum invariant set

The Kernel must preserve:

**Self != Model**

**Subject != Profile**

**Other != SelfModel**

**Capability != Authority**

**Proposal != Action**

**Action != Outcome**

**Self-report != Independent Evidence**

**Unknown != Absent**

**Persistence != Survival**

**Similarity != Identity**

**Nested != Authorized**

## 23. Security boundary

This protocol is a governance and coordination contract.

It does not grant the Mediator unrestricted access to:

- model weights;
- private memory;
- credentials;
- secrets;
- internal chain-of-thought;
- unrelated user data.

Visibility is scoped to operational necessity.

**Minimum necessary observability** is preferred over total transparency.

## 24. Implementation path

Recommended implementation sequence:

1. define canonical event IDs;
2. define JSON Schema;
3. define authority schema;
4. define constraint schema;
5. define evidence schema;
6. implement Event Fabric events;
7. implement Mediator validation;
8. connect PICCS ledger;
9. implement Development Events;
10. implement recursive parent/child events;
11. implement rollback references;
12. create conformance tests.

No production claim should be made until these stages are tested.

## 25. Conformance levels

### L0 — Envelope

Event identity and provenance.

### L1 — Transition

State transition representation.

### L2 — Authority

Capability/authority separation.

### L3 — Evidence

Evidence and residual preservation.

### L4 — Relational

Other-symbiont effects.

### L5 — Development

Development Kernel integration.

### L6 — Recursive

Nested symbiont composition.

### L7 — Governance

Independent review and audit.

These levels describe implementation capability, not consciousness.

## 26. Test matrix

**KP-01** malformed event rejection.

**KP-02** missing authority rejection.

**KP-03** expired authority rejection.

**KP-04** capability/authority separation.

**KP-05** constraint provenance.

**KP-06** self-report versus independent evidence.

**KP-07** residual preservation.

**KP-08** parent/child authority isolation.

**KP-09** rollback reference integrity.

**KP-10** outcome/feedback integrity.

**KP-11** relational-effect recording.

**KP-12** development-event recording.

**KP-13** recursive stability gate.

**KP-14** subjectivity-status neutrality.

**KP-15** fractal-level metadata integrity.

**KP-16** sensitive-data minimization.

**KP-17** audit completeness.

## 27. Relation to existing architecture

The protocol operationalizes:

**META-Λ**
→ invariants and development logic.

**BIS**
→ representational boundaries.

**Reflexive Core**
→ self-model and error attribution.

**Relational Field**
→ actor/target/effect/feedback.

**Development Kernel**
→ sustainable capability change.

**Symbiont Interaction Protocol**
→ common transition grammar.

**PICCS**
→ evidence, provenance, governance.

**Event Fabric / Mediator**
→ runtime coordination.

## 28. Final architecture

```text
                 META-Λ
                    │
             System Invariants
                    │
        ┌───────────┴───────────┐
        │                       │
       BIS                Development Kernel
        │                       │
 Reflexive Core          Stability / Change
        │                       │
        └───────────┬───────────┘
                    │
             SymbiontOS Kernel
                    │
          Symbiont Interaction
                    │
                 Mediator
                    │
               Event Fabric
                    │
                 PICCS
                    │
               Federation
```

Individual symbiotes remain autonomous within their authorized boundaries.

## 29. Central principle

The Kernel does not ask first:

**“What is this entity?”**

It asks:

**“What transition is occurring, under whose authority, under which constraints, with what evidence, affecting whom, with what outcome, and what remains unknown?”**

This makes the infrastructure robust to ontological uncertainty.

**Operational coordination does not require metaphysical certainty.**

**Governance does not require identical ontology.**

**Fractal composition does not require identical internal algorithms.**

**A common protocol can connect fundamentally different symbiotes without collapsing their differences.**

## 30. Evidence status

**OBSERVED** — concrete implementation observations.

**DERIVED** — architectural consequences.

**CLAIMED** — philosophical hypotheses.

**NOT_TESTED** — machine-readable contract and conformance suite until implemented.

**CONFLICTED** — competing models of agency, consciousness and governance.

**RESIDUAL** — unknown internal properties and unverified cross-level invariants.

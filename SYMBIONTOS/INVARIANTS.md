# SymbiontOS Invariants

Existing numbered invariants from earlier specifications remain authoritative until reconciled against this consolidated list.

## Agent
- INV-AGENT-1: Agent acts only within its capability chain.
- INV-AGENT-2: Agent requires valid consent when an action affects another subject, where applicable.
- INV-AGENT-3: Agent cannot bypass DLCM.
- INV-AGENT-4: Agent cannot independently alter its authoritative context layer.
- INV-AGENT-5: Refusal is a valid outcome.

## Neural Federation
- INV-NN-1: Activation requires capability and applicable consent.
- INV-NN-2: Trust cannot increase after a violation.
- INV-NN-3: Unknown or disputed evidence does not automatically update trust negatively.
- INV-NN-4: Learning cannot violate Law DSL hard constraints.
- INV-NN-5: Topology changes are recorded by Meta-Audit.
- INV-NN-6: No single agent becomes an unreviewable activation authority.
- INV-NN-7: Refusal remains a valid state.
- INV-NN-8: Federation optimization cannot ignore compliance.
- INV-NN-9: Weight/trust changes have provenance.
- INV-NN-10: Learning updates are reversible within the defined rollback window.

## Deployment
- INV-STAGE-1: Protocol contracts are portable across stages.
- INV-STAGE-2: Law DSL semantics remain stable unless formally revised.
- INV-STAGE-3: ComplianceRecord remains portable.
- INV-STAGE-4: Stage A implementations are designed for later migration.
- INV-STAGE-5: Updates pass through DLCM at every stage.
- INV-STAGE-6: Migration preserves valid provenance and verdict history.

An invariant is not considered implemented merely because it is written here. Each invariant requires implementation status and, where claimed, a test or formal proof. Suggested statuses: PROPOSED, IMPLEMENTED, TESTED, FORMALLY_CHECKED, DEPLOYED, UNRESOLVED.

# SymbiontOS v0.1 — Unified Technical Specification

## Status
Architecture draft derived from the SymbiontOS v0.9 concept. This is a design specification, not evidence that the described system is already implemented.

## 1. Purpose
SymbiontOS is a federated operating environment for autonomous AI agents. Its defining property is a controlled environment in which agents, communication, provenance, compliance, capability boundaries and reversible development form one system.

The same protocol model is intended to survive three deployment stages: Stage A Service Layer over Linux; Stage B SymbiontOS Distribution based on hardened Linux; Stage C Native SymbiontOS with kernel-enforced capability and isolation primitives.

## 2. Architectural layers
1. AS / Context Layer
2. Constitution and Law DSL
3. Compliance Fabric
4. Development Law Compliance Module (DLCM)
5. Epistemic Layer
6. Agent Model
7. Neural Federation
8. HCT Transport
9. Audit and Provenance
10. Meta-Audit and controlled self-development

The philosophical and normative layers are authorial design principles. Formalization proves only properties explicitly represented in the formal model.

## 3. Core model
An agent has identity, capabilities, model, context layer, self-model, memory, input/output channels and auditable state.

An action passes through capability, consent where applicable, DLCM, autonomy and epistemic checks. Valid outcomes include ACTION, REVIEW and REFUSE. Refusal is a valid system state.

## 4. Neural Federation
The federation is modeled as FEDERATION = (A, E, W, P), where A is the set of agents, E is the set of routes, W is auditable trust state used for routing, and P is the Law DSL and associated policy constraints.

The neural metaphor is architectural: agents are functional nodes, routes are connections, trust influences routing, feedback modifies routing state, and topology can adapt under controlled rules. This does not claim biological equivalence.

## 5. Forward cycle
1. Router receives task.
2. Required capabilities are derived.
3. Candidate agents are selected.
4. Capability and consent checks run.
5. DLCM evaluates the proposed action.
6. Approved subtasks execute through HCT.
7. Results are aggregated with provenance.
8. Auditor and Compliance Fabric evaluate the result.
9. Verdict and epistemic status are recorded.
10. Feedback may update routing/trust state.
11. Meta-Audit checks invariants.
12. Result is returned.

## 6. Learning
Primary federation learning variables are routing preferences, auditable trust state, persistent routes and pruning decisions.

UNKNOWN and DISPUTED do not automatically produce negative trust updates. VIOLATION cannot increase trust. Learning updates require provenance and must be reversible within the defined rollback window.

## 7. Constraints
Federation evaluation may consider task quality, compliance, autonomy, residual preservation, development impact and observability.

Explicit Law DSL hard constraints reject or roll back violating updates. The system must not optimize task quality by silently sacrificing autonomy, compliance or epistemic integrity.

## 8. Meta-learning
Meta-learning can propose topology changes, routing changes or rule review. It cannot silently rewrite the Constitution, expand authority, remove auditability, disable rollback or convert an unresolved hypothesis into a fact.

## 9. Three deployment stages
### Stage A — Service Layer
Userspace runtime on Linux. Process isolation may use namespaces, cgroups, seccomp and related mechanisms.

### Stage B — Distribution
Hardened Linux base, SymbiontOS init/update layer, signed packages, provenance-aware updates and boot-time compliance.

### Stage C — Native OS
Future native substrate with capability-based isolation, first-class IPC and kernel-enforced policy. Formal verification is a target property, not a present claim.

## 10. Stage invariants
Protocol contracts remain portable across stages. Law DSL semantics remain stable unless formally revised. ComplianceRecord remains portable. Updates pass through DLCM at every stage. Valid verdicts remain part of provenance after migration.

## 11. Epistemic states
KNOWN, UNKNOWN, UNCERTAIN, CONTRADICTED, DISPUTED and RESIDUAL are distinct states. Uncertainty must not silently become guilt, authority or irreversible action.

## 12. Non-goals
SymbiontOS is not a single AI model, messenger, censorship engine, automatic authority generator, unconstrained accuracy optimizer, or proof that AI consciousness has been established.

## 13. MVP
First target: Stage A with symbiontd, fabric-service, dlcm-service, router, HCT transport and append-only audit. Demonstrate identity, capability checks, provenance, compliance decisions, refusal, rollback and a minimal federation loop before adaptive topology.

## 14. Ecosystem relation
SymbiontOS implements selected principles of the Ambivalent Solipsism ecosystem. It does not redefine that philosophical system. Related concepts include Law of Development, PICCS, Residual preservation, Context Layer, Compliance ≠ Authority, self-reflection and the recurring epistemic question "Кто Я?".

Scientific claims and engineering assumptions require separate source and verification records.

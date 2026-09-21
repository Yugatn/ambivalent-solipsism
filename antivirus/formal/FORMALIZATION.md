# PICCS Sentinel Formalization

## Purpose

This directory is the formal verification layer for PICCS Sentinel.

It does not replace the Sentinel architecture, threat model or protocol. It gives a small executable transition system that can be explored with the TLA+ model checker TLC.

The model is intentionally conservative. It formalizes control boundaries and safety properties before attempting to formalize the full operating-system, malware-analysis or AI-agent environment.

## Files

- `Sentinel.tla` contains the transition system, states and candidate safety predicates.
- `Sentinel.cfg` provides a finite TLC model configuration.
- `FORMALIZATION.md` documents the verification boundary.

## Formal boundary

The first model checks:

- operational state transitions;
- separation between evidence, decision and action;
- explicit authority;
- bounded quarantine;
- bounded emergency authority;
- safe degradation;
- protected audit state;
- challenge availability;
- preservation of UNKNOWN and CONFLICTING epistemic states;
- prevention of automatic authority expansion after degradation;
- temporal expiration of temporary authority.

It deliberately does not claim to prove:

- that a detector identifies real malware;
- that a threat model is complete;
- that the philosophical model of reality is empirically true;
- that the finite model covers all operating-system behavior;
- that a passing TLC run establishes production security.

## Verification principle

A passing model check means only that the encoded transition system satisfies the encoded properties for the selected finite state space.

A counterexample is useful even when the architecture is conceptually correct. It identifies either:

1. a real architectural weakness;
2. an underspecified transition;
3. an invariant that was stated too strongly;
4. a mismatch between the protocol and its formal encoding.

The correct response to a counterexample is to inspect the model, not to weaken the invariant merely to obtain a green result.

## SNT-01 through SNT-24

The specification contains named predicates corresponding to the 24 Sentinel invariants documented in `ARCHITECTURE.md`.

Some invariants are currently represented as explicit boundary placeholders, such as evidence-independence and privacy semantics. These are intentionally marked in the model rather than presented as already solved formal problems.

The next formal passes should replace those placeholders with explicit state and dependency relations.

## Model-checking sequence

Recommended sequence:

1. Parse and type-check the module.
2. Run TLC with the supplied finite configuration.
3. Inspect every counterexample.
4. Strengthen the state representation only where the protocol requires it.
5. Re-run the complete invariant set.
6. Add liveness properties only after the safety model is stable.
7. Add adversarial actions that attempt to violate the invariants.
8. Keep counterexample traces as regression fixtures.

## Adversarial extensions planned

The next formal layer should add explicit adversarial transitions for:

- forged provenance;
- evidence mutation;
- detector failure;
- emergency persistence;
- quarantine persistence;
- capability escalation;
- synthetic consensus;
- model drift;
- Sentinel self-intervention;
- corrupted audit records;
- challenge suppression;
- risk displacement.

## Status

**Formalization layer: initial executable model.**

This is a verification scaffold, not a security certification.

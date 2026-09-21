# PICCS Sentinel — Protocol Specification

## Purpose

This document defines the minimum protocol objects required to turn PICCS Sentinel from a conceptual architecture into a testable prototype.

## 1. Event

Every security-relevant event should contain:

- event_id;
- timestamp;
- source;
- actor or process identity;
- context;
- resource;
- operation;
- provenance;
- integrity state;
- parent event where known.

## 2. Evidence object

Evidence is immutable from the perspective of the decision layer.

Required fields:

- evidence_id;
- source;
- collection method;
- collection time;
- integrity metadata;
- transformation history;
- epistemic status;
- confidence description;
- conflict references.

## 3. Threat hypothesis

A hypothesis is explicitly separate from evidence.

Fields:

- hypothesis_id;
- supporting evidence;
- contradictory evidence;
- assumptions;
- affected scope;
- uncertainty;
- possible consequences;
- alternative hypotheses;
- model version.

## 4. Decision request

A consequential action request contains:

- target;
- proposed action;
- authority;
- purpose;
- scope;
- duration;
- reversibility;
- alternatives;
- expected effect;
- residual uncertainty;
- challenge requirement.

## 5. Action capability

Capabilities are:

- least privilege;
- scoped;
- time-bounded;
- revocable;
- auditable.

A capability is not permission. Permission is a contextual authorization to use a capability for a declared purpose.

## 6. Decision Passport

A high-impact decision creates a Decision Passport linking evidence, hypothesis, authority, action and outcome.

This record must survive later model changes.

## 7. Quarantine lease

Quarantine is represented as a lease:

- subject;
- scope;
- start;
- expiration;
- reason;
- authority;
- rollback method;
- review status.

Expiration requires explicit renewal.

## 8. Emergency lease

Emergency authority is also a lease.

It must include:

- trigger;
- maximum duration;
- minimum scope;
- allowed actions;
- termination condition;
- mandatory review.

Emergency mode cannot renew itself solely because it remains active.

## 9. Model version

Every detector, rule, AI model or policy relevant to a consequential decision has:

- model_id;
- version;
- provenance;
- effective time;
- expiry or revalidation condition;
- dependencies;
- rollback version.

## 10. Challenge

An independent challenge records:

- challenged decision;
- challenger;
- evidence examined;
- dependency independence;
- result;
- unresolved disagreement.

Disagreement is retained.

## 11. Recovery

Recovery records:

- pre-action state;
- action;
- post-action state;
- recovery target;
- recovery result;
- residual discrepancy;
- follow-up action.

## 12. Prototype state machine

Suggested states:

OBSERVE → VERIFY → GUARDED → RESTRICT → QUARANTINE → HOLD → RECOVER → REVIEW

UNKNOWN and CONFLICTING are epistemic states that may coexist with operational states.

They are not operational failure states.

## 13. Mandatory separation

The prototype must keep separate modules for:

- collection;
- evidence normalization;
- detection;
- decision;
- authorization;
- intervention;
- recovery;
- audit.

This is an implementation requirement intended to reduce self-validation and authority-collapse failures.

## 14. Security properties to test

At minimum:

- no unauthorized capability use;
- no silent evidence mutation;
- no expired quarantine persistence;
- no emergency authority without expiration;
- no automatic action from UNKNOWN alone;
- no self-validation through post-action evidence;
- no authority expansion after detector failure;
- no critical decision without provenance;
- no high-impact decision without challenge where feasible;
- no historical decision silently reinterpreted by a new rule version.

## 15. Prototype principle

The first implementation should be deliberately less autonomous than the final research architecture.

Autonomy should be earned through evidence from testing, not assumed from design.


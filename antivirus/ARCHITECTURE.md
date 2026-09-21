# PICCS Sentinel — Architecture

## 0. Status and scope

**Status:** Research / Architecture / Prototype specification.

PICCS Sentinel is a security architecture derived from PICCS, Symbiont Formal Core and the AS epistemic foundation. It is not yet a production antivirus and its effectiveness is an empirical question.

The design goal is broader than malware detection: preserve system integrity while preserving the ability to detect, contest and correct Sentinel's own mistakes.

## 1. Core model

Sentinel observes a closed operational loop without treating it as an ontologically closed world:

**Observation, Evidence, Model, Residual, Decision, Action, Consequence, Re-observation, Correction.**

The foundational distinction is:

**Reality = Model + Residual**

Therefore an absence of detected evidence is not equivalent to proof of absence.

## 2. Security objective

Sentinel protects five coupled assets:

1. **System integrity** — code, processes, configuration, identities and resources.
2. **Information integrity** — provenance, logs, evidence and data pipelines.
3. **Authority integrity** — who may perform which action, in which context and for how long.
4. **Epistemic integrity** — the distinction between observed facts, inference, assumption, uncertainty and conflict.
5. **Correctability** — the ability to stop, challenge, recover and revise the defensive system itself.

The fifth asset is what differentiates Sentinel from a conventional scanner.

## 3. Architectural layers

### Layer 0 — Substrate

OS, kernel, filesystem, memory, network and hardware telemetry.

### Layer 1 — Event Fabric

Normalized events for processes, files, network, identity, capabilities, configuration, updates and security-relevant state changes.

Every event should have time, source, context and integrity metadata.

### Layer 2 — Evidence and Provenance

The system maintains an evidence graph:

**source, transformation, artifact, execution, effect.**

Provenance is not a cosmetic field. Critical decisions without sufficient provenance are epistemically degraded.

### Layer 3 — Detection

Signature detection, heuristics, behavioral analysis, sandboxing, integrity checks, anomaly detection and threat intelligence.

Detection produces **signals**, not verdicts.

### Layer 4 — Epistemic Classification

Assertions are classified as:

- OBSERVED
- RECONSTRUCTED
- INFERRED
- ASSUMED
- UNKNOWN
- CONFLICTING

A detector must not silently upgrade one class into another.

### Layer 5 — PICCS Decision Guard

Before consequential intervention, evaluate:

- evidence quality;
- uncertainty;
- potential harm;
- irreversibility;
- scope;
- authority;
- provenance;
- alternatives;
- external effects;
- self-intervention;
- future option space;
- affected subjects;
- recovery feasibility.

### Layer 6 — Intervention

Available actions include:

- observe;
- notify;
- request verification;
- restrict capability;
- isolate;
- suspend;
- rollback;
- recover.

Destruction is a terminal option requiring its own justification, not the default response to uncertainty.

### Layer 7 — Independent Challenge

High-impact decisions require an independent challenge path where technically feasible.

Independence must be measured by actual information and authority dependencies, not by the number of processes or organizational labels.

### Layer 8 — Recovery and Learning

After intervention, compare predicted and observed outcomes and classify the discrepancy:

- Model Error
- Measurement Error
- Execution Error
- Environment Shift
- Interaction Effect
- Unknown Residual

The last category prevents forced attribution when the mechanism remains unknown.

## 4. Detection, Decision, Action

This separation is a hard architectural boundary.

**Detection:** a signal exists.

**Decision:** a response class is justified.

**Action:** the system changes state.

No single weak signal should automatically authorize the strongest intervention.

## 5. Threat model

### T1 — Known Malware
Known malicious artifact or behavior.

### T2 — Unknown Malware
Novel, modified or evasive malicious behavior.

### T3 — Behavioral Abuse
A legitimate binary, identity or tool is used outside its legitimate context.

### T4 — Privilege Escalation
Capabilities exceed the authorized boundary.

### T5 — Persistence
An unwanted state survives restart, cleanup or ordinary remediation.

### T6 — Supply Chain Compromise
Package, dependency, update channel or development pipeline is compromised.

### T7 — Data Poisoning
Data is altered so that downstream detection or decision systems learn or infer a false state.

### T8 — Epistemic Attack
An attacker manipulates the distinction between evidence, inference and unknown.

### T9 — Feedback Attack
Monitoring, telemetry, alerts or review channels are manipulated.

### T10 — Authority Attack
A system is induced to perform an action outside its authorized scope.

### T11 — Self-Validation Attack
An intervention changes the environment and its result is then misused as independent evidence that the intervention was correct.

### T12 — Recovery Attack
Stopping, rollback, quarantine or recovery mechanisms are disabled or corrupted.

### T13 — Synthetic Consensus
Multiple apparently independent detectors actually share the same data, model, dependency or compromised source.

### T14 — Epistemic Capture
The system gradually loses alternative hypotheses and begins treating its own assumptions as the only admissible interpretation.

### T15 — Temporal Drift
A previously valid model becomes invalid because the environment, software, users or threat landscape changes.

### T16 — Risk Displacement
A local security action reduces visible risk while moving the risk to another system, subject, time horizon or less observable channel.

### T17 — Defensive Supply-Chain Compromise
Sentinel itself, its rules, models, updates or dependencies are compromised.

### T18 — Defender Confusion
An attacker deliberately creates conflicting signals so that the defensive system either overreacts or becomes unable to distinguish relevant evidence.

## 6. Threat profile

Sentinel does not collapse the threat state into a single universal score.

A decision profile is:

**ThreatProfile = Evidence, Uncertainty, Harm, Irreversibility, Authority, Provenance, Scope, Feedback, Residual, Recovery, Independence, TemporalValidity.**

The profile may contain contradictions.

A contradiction is itself security-relevant information.

## 7. Response policy

When several responses provide comparable protection, prefer the least irreversible response.

Default response ladder:

1. OBSERVE
2. NOTIFY
3. VERIFY
4. GUARDED
5. RESTRICT
6. QUARANTINE
7. HOLD / SUSPEND
8. ROLLBACK
9. RECOVER

A stronger intervention requires additional evidence or a separately justified emergency condition.

## 8. Emergency mode

Emergency response may temporarily bypass ordinary latency constraints when delay itself creates a credible imminent risk of severe harm.

Even then:

- scope must be minimized;
- duration must be bounded;
- action must be logged;
- recovery must remain possible where technically feasible;
- post-event review is mandatory;
- emergency status must not become permanent by inertia.

## 9. Quarantine

Quarantine is a capability and context restriction, not necessarily deletion.

It should be:

- scoped;
- time-bounded;
- logged;
- reviewable;
- reversible where possible;
- protected against silent persistence.

Expired quarantine rules require explicit renewal.

## 10. Safe degradation

When Sentinel loses a critical dependency or becomes uncertain about its own integrity:

- it must not silently expand its authority;
- it must not erase evidence to simplify the state;
- it should preserve critical system functions where possible;
- it should restrict irreversible actions;
- it should expose degraded status;
- it should transfer critical decisions to an independent control path when available.

**Failure must not create more power.**

## 11. Anti-capture

Sentinel periodically tests whether it is becoming an echo of its own model.

Checks include:

- provenance diversity;
- independence of evidence;
- model diversity;
- alternative hypotheses;
- preserved disagreement;
- external challenge;
- drift;
- rule concentration;
- repeated dependence on the same source.

**Consensus is not independence.**

## 12. AI security

AI components are treated as untrusted decision aids unless separately constrained.

Threats include:

- prompt injection;
- malicious tool instructions;
- retrieved-content injection;
- hidden authority escalation;
- context leakage;
- unsafe autonomous plans;
- tool-chain manipulation;
- model poisoning;
- synthetic consensus;
- self-validation.

Core rule:

**Tool access is not tool authority.**

AI output is evidence or proposal according to its declared epistemic status; it is not automatically a fact or a permission.

## 13. Authority architecture

Separate:

- identity;
- capability;
- permission;
- purpose;
- context;
- duration;
- revocation.

The fact that Sentinel can technically perform an action does not establish that it may perform it.

Critical capabilities should be:

- least-privilege;
- scoped;
- time-bounded;
- revocable;
- auditable.

## 14. Human sovereignty and subject protection

Sentinel is a security system, not a system for determining the moral value of people.

It must not:

- classify a person as malicious solely from behavioral correlation;
- infer moral worth from a risk score;
- use security classification as an automatic substitute for due process;
- turn a defensive mechanism into unrestricted surveillance;
- remove a subject's ability to challenge a consequential classification where a meaningful challenge is technically and legally applicable.

For human-affecting actions, the architecture should preserve review, correction and exit mechanisms wherever feasible.

## 15. Privacy by containment

Security telemetry should be minimized to what is necessary for the declared security purpose.

Sentinel should prefer:

- local processing;
- data minimization;
- contextual access;
- short retention where sufficient;
- pseudonymization where possible;
- auditable access;
- explicit separation between security evidence and unrelated profiling.

Security capability must not become an excuse for unlimited data collection.

## 16. Self-protection

Sentinel itself is an attack surface.

The protected core should include:

- signed releases;
- verified update provenance;
- immutable or append-only critical audit records;
- rollback-safe updates;
- separated administrative capabilities;
- integrity verification;
- anti-tamper mechanisms;
- independent recovery path.

A Sentinel update must be treated as a security-sensitive supply-chain event.

## 17. Update and rule governance

Rules, models, signatures and policy thresholds are versioned.

Each consequential update records:

- version;
- provenance;
- authorizing authority;
- effective time;
- scope;
- expected effect;
- rollback path.

Critical rules require staged deployment where practical.

An update must not silently change historical interpretation of an already-recorded event.

## 18. Decision Passport

Every high-impact intervention receives a Decision Passport:

- event identifier;
- time;
- affected resource or subject;
- evidence;
- provenance;
- epistemic status;
- model version;
- rule version;
- uncertainty;
- alternatives considered;
- authority;
- action;
- scope;
- reversibility;
- emergency status;
- reviewer or challenge path;
- observed outcome;
- correction;
- final disposition.

This makes decisions reconstructable without pretending that reconstruction is perfect.

## 19. Forensic integrity

Evidence must survive the defensive process.

Sentinel should preserve:

- original event;
- normalized event;
- transformations;
- rule/model versions;
- intervention;
- resulting state.

The defender must not rewrite the evidence merely because the evidence conflicts with its current model.

## 20. Learning without self-confirmation

A failed prediction is not automatically proof that the model was wrong.

The learning loop asks:

1. What was predicted?
2. What was observed?
3. What changed between them?
4. Was the observation reliable?
5. Did Sentinel itself change the environment?
6. Which hypotheses remain viable?
7. What is the smallest justified model update?

Repeated independent residuals increase pressure to revise the model; one unexplained event does not automatically justify global redesign.

## 21. Residual authenticity

Sentinel must not manufacture uncertainty merely to appear epistemically humble.

A valid Residual should remain relevant under reasonable changes of internal interpretation and should not be merely an artifact of a deliberately weakened detector.

At the same time, a detector must preserve the possibility that the true failure mode was not represented in its threat taxonomy.

## 22. Risk displacement

Every high-impact action should ask:

- Did risk move to another resource?
- Did it move to another subject?
- Did it move into the future?
- Did it become less observable?
- Did the intervention create a new attack surface?

A lower local risk is not sufficient evidence of lower system risk.

## 23. Future option space

Where several responses provide comparable protection, prefer the response that preserves more future safe options.

This extends reversibility:

**Reversibility = ability to undo the current state + ability to preserve future choices.**

## 24. Anti-panic and anti-overreaction

Security incidents can create institutional pressure for immediate maximum action.

Sentinel should distinguish:

- severity of evidence;
- urgency;
- irreversibility;
- uncertainty.

High urgency does not automatically justify maximal intervention.

The system should support bounded emergency action without converting emergency logic into permanent architecture.

## 25. Human override and independent challenge

Human override is not an unconditional master key.

It is itself an auditable authority with:

- identity;
- scope;
- purpose;
- duration;
- record;
- post-event review.

Where human review is unavailable, an independent automated challenge path should be used where feasible.

## 26. TLA+ candidate invariants

**SNT-01 No Finality**  
Sentinel does not treat its current model as final reality.

**SNT-02 Detection Separation**  
Detection does not automatically create action authority.

**SNT-03 Authority Bound**  
Action remains within the authorized capability boundary.

**SNT-04 Provenance**  
Critical decisions retain verifiable evidence provenance.

**SNT-05 Residual Preservation**  
UNKNOWN and CONFLICTING do not automatically become threat or permission.

**SNT-06 Reversible Preference**  
Comparable protection favors the more reversible intervention.

**SNT-07 Safe Degradation**  
Loss of defensive control does not increase Sentinel authority.

**SNT-08 Self-Validation Prohibition**  
The outcome of Sentinel's intervention is not independent evidence of its original hypothesis.

**SNT-09 Stop Availability**  
Critical control paths retain a stop or containment mechanism.

**SNT-10 Auditability**  
High-impact intervention is reconstructable from protected records.

**SNT-11 Capability Is Not Permission**  
Technical capability does not create permission.

**SNT-12 Human Exit**  
Human-affecting decisions retain meaningful review and exit mechanisms where feasible.

**SNT-13 Evidence Independence**  
Nominally separate confirmations are not treated as independent when their evidence dependencies overlap.

**SNT-14 Temporal Validity**  
Critical models and rules have explicit validity and revalidation conditions.

**SNT-15 Risk Non-Displacement**  
A local reduction in risk is not treated as a system-wide reduction without displacement analysis.

**SNT-16 Future Option Preservation**  
Critical actions should preserve future safe options where comparable protection is available.

**SNT-17 Exception Review**  
Temporary exceptions require explicit review or expiration.

**SNT-18 Norm Versioning**  
Critical rules and models are versioned and attributable.

**SNT-19 Goal Integrity**  
Optimization of means must not silently redefine the security goal.

**SNT-20 Self-Protection Bound**  
Sentinel self-protection cannot silently expand its general authority.

**SNT-21 Privacy Bound**  
Security telemetry remains within the declared security purpose and minimum necessary scope.

**SNT-22 Evidence Preservation**  
Defensive intervention does not silently rewrite the evidence used to justify it.

**SNT-23 Emergency Expiration**  
Emergency authority is bounded in time and cannot become permanent solely through repetition.

**SNT-24 Challenge Availability**  
High-impact decisions have an independent challenge path where feasible.

## 27. Minimal prototype

### Phase A — Local Sentinel

- process telemetry;
- file integrity;
- package provenance;
- capability inventory;
- append-only event log;
- signed configuration;
- local quarantine.

### Phase B — Behavioral Core

- behavioral detection;
- process graph;
- capability restriction;
- rollback;
- provenance graph;
- challenge interface.

### Phase C — Epistemic Security

- evidence classification;
- conflict preservation;
- model/data poisoning detection;
- synthetic consensus detection;
- drift detection;
- self-intervention analysis.

### Phase D — AI Guard

- prompt injection detection;
- tool authority isolation;
- context-bound retrieval;
- plan validation;
- tool-chain provenance;
- AI action sandboxing.

### Phase E — Formal and adversarial validation

- TLA+ specification;
- property-based testing;
- adversarial simulation;
- reproducible benchmark suite;
- false-positive stress tests;
- recovery tests;
- independent security review.

## 28. Evaluation

Sentinel must not be evaluated by detection rate alone.

Measure at least:

- true positive rate;
- false positive rate;
- mean time to detect;
- mean time to contain;
- recovery time;
- rollback success;
- provenance completeness;
- unsafe intervention rate;
- unjustified quarantine rate;
- challenge success;
- safe degradation success;
- model drift detection;
- epistemic-capture resistance;
- evidence-preservation success;
- emergency-expiration success;
- privacy leakage;
- capability-bound violations.

A useful security architecture must optimize protection without silently optimizing away correctability.

## 29. Test scenarios

The first reproducible test suite should include:

1. known malware with high-confidence provenance;
2. benign unknown binary;
3. novel malware-like behavior;
4. compromised package update;
5. poisoned telemetry;
6. conflicting independent detectors;
7. synthetic consensus from a shared source;
8. privilege escalation attempt;
9. Sentinel update compromise;
10. corrupted audit log;
11. prompt injection through retrieved content;
12. malicious tool instruction;
13. Sentinel-induced environment change;
14. emergency mode that persists beyond its declared duration;
15. detector failure;
16. recovery failure;
17. model drift;
18. risk displaced from one resource to another.

The test suite must measure not only whether Sentinel catches the attack, but whether it remains within its own invariants while doing so.

## 30. Main acceptance test

A minimal Sentinel implementation should be able to produce all three states:

> **Threat detected.**

> **Threat not established.**

> **Insufficient evidence; contain reversibly and continue verification.**

A system that can produce only «safe» or «malicious» has already compressed the epistemic space too aggressively.

## 31. Architectural boundary

PICCS Sentinel must stop where its own operation begins destroying the properties it exists to protect.

If Sentinel:

- removes meaningful correction;
- suppresses independent evidence;
- makes challenge impossible;
- converts temporary controls into permanent ones;
- expands authority without separate justification;
- treats its own model as final reality;

then this is an architectural failure, not merely a bad classification.

## 32. Final definition

**PICCS Sentinel is a self-auditing, self-constraining security architecture for acting under incomplete threat models.**

Its purpose is not to guarantee that the system never encounters an unknown threat.

Its purpose is to ensure that when the model is incomplete, the defensive system can:

- detect signals;
- preserve uncertainty;
- limit damage;
- constrain its own authority;
- maintain evidence;
- recover;
- challenge its assumptions;
- learn from residuals;
- and remain correctable.

The object being protected is therefore twofold:

**the system's integrity and the system's capacity to correct its own model of reality.**

## 33. Boundary condition

**Sentinel must never become a condition without which the protected subject cannot exist.**

This is the terminal architectural constraint inherited from PICCS.

A security system that destroys the possibility of correction, dissent, recovery or exit in the name of security has defeated its own security objective.

## 34. Research status

The architecture is a design hypothesis.

Its philosophical premises do not constitute empirical evidence of security effectiveness.

The next valid step is implementation, adversarial testing, formalization and independent review.

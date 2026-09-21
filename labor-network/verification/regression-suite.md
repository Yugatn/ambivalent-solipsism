# Regression Suite СТСети

Regression Suite проверяет, что архитектурное усовершенствование не разрушило ранее зафиксированные правила.

## Группы

### R01 Canon
Исходные принципы и доменные ограничения.

### R02 State
Допустимые и недопустимые переходы.

### R03 Authority
Границы полномочий.

### R04 Evidence
Provenance, validity, challenge и correction.

### R05 Decision
Policy, reason, impact и review.

### R06 Subject
Visibility, correction, contest, exit.

### R07 Federation
Scope, provenance, revocation и failure.

### R08 Audit
Traceability и integrity.

### R09 Reconciliation
Распространение исправлений на зависимые решения.

### R10 Recovery
Отказоустойчивость и восстановление.

## Regression rule

Любое изменение ядра должно запускать проверки затронутых групп.

## Release gate

Изменение не считается готовым к объединению, если оно нарушает ранее установленный invariant без явно принятого изменения канона.


## Executable validation matrix

The current architecture maps the declared test scenarios to the invariant and regression groups:

| Scenario | Primary invariant | Regression groups |
|---|---|---|
| T01 duplicate event | I16 Idempotency | R02, R08, R10 |
| T02 corrected fact | I9 Error propagation control | R04, R08, R09 |
| T03 insufficient data | I15 Unknown preservation | R04, R05 |
| T04 new data without authority | I17 Authority non-creation, I18 Scope preservation | R03, R05 |
| T05 qualification request | I6 Minimal disclosure, I20 Federation boundary | R06, R07 |
| T06 revoked delegation | I2 Purpose limitation, I17 Authority non-creation | R03, R06 |
| T07 regional node failure | I10 Availability, I21 No silent downgrade, I22 Recovery | R07, R10 |
| T08 disputed fact | I4 Contestability, I15 Unknown preservation | R04, R06, R09 |
| T09 high-impact decision | I11 Human review, I23 Decision review | R05, R06 |
| T10 policy conflict | I3 Provenance | R03, R05, R08 |
| T11 expired evidence | I3 Provenance, I15 Unknown preservation | R04, R09 |
| T12 purpose isolation | I2 Purpose limitation, I6 Minimal disclosure | R03, R06 |
| T13 infrastructure barrier | I14 Infrastructure neutrality | R01, R06 |
| T14 exit | I12 Exit, I24 Exit integrity | R06, R08 |
| T15 derived decision | I9 Error propagation control | R04, R05, R09 |

### Release gate

The suite is structurally complete when each declared scenario has:
1. a defined expected outcome;
2. at least one invariant;
3. at least one regression group;
4. an auditable failure condition.

A test failure blocks release unless the corresponding invariant or canonical rule is explicitly changed and the change is itself reviewed.


## Final release-gate checks

### G1. Decision versus Action

A policy result is not itself execution authority. The decision lifecycle must reach its required review state before a high-impact effect is applied, and the actual effect must remain auditable as a separate action.

### G2. Audit versus surveillance

Audit records prove significant system actions with purpose and minimization. Observability must not become unrestricted subject monitoring.

### G3. Federation versus profile construction

Federation contracts transmit bounded, purpose-specific assertions. Node trust, connectivity, or accumulated requests do not authorize construction of an unrestricted centralized subject profile.

### G4. State versus event history

Current state remains a projection/configuration. Event history remains the source for reconstructing significant past changes. Recovery and reconciliation cannot rely on state alone.

### G5. Privacy versus government integration

Government integration remains purpose-bound and does not acquire broader authority from technical database interoperability. Alternative access paths remain available where required.

### G6. Human review versus data expansion

Human Review receives the minimum relevant evidence and does not gain automatic access to the subject's complete history merely because review was triggered.

### G7. Unknown versus negative outcome

Insufficient evidence remains `unknown` unless a separately defined rule establishes another outcome. Absence of confirmation is not silently converted into a negative fact.

### G8. Release decision

The current documented architecture passes the structural release gate for these eight conflict classes. This is an architectural/documentation validation, not a claim of runtime execution or production certification.


## Phase 3 Event Engine regression cross-check

Phase 3 E01–E15 are checked against the existing release gates G1–G8. The purpose is to ensure that Event Engine mechanics cannot bypass already established architectural controls.

| Event Engine case | Release gates | Control relationship |
|---|---|---|
| E01 duplicate delivery | G4, G8 | duplicate processing cannot replace event history or create a second logical transition |
| E02 event identity conflict | G4, G8 | conflicting reuse of identity cannot overwrite canonical history |
| E03 retry after failure | G1, G4, G8 | retry cannot repeat protected effects; durable event remains reconstructable |
| E04 causation chain | G4, G8 | causal lineage remains distinguishable from workflow correlation |
| E05 unknown predecessor | G4, G7, G8 | missing causal context remains explicit rather than becoming an inferred fact |
| E06 causal cycle | G4, G8 | invalid causal structure is rejected/quarantined |
| E07 out-of-order event | G1, G4, G8 | ordering guard cannot be bypassed by delivery order |
| E08 timestamp/order mismatch | G4, G7, G8 | temporal metadata cannot silently create causal truth |
| E09 replay | G1, G4, G8 | replay reconstructs state without re-executing external effects |
| E10 replay versioning | G4, G8 | projection interpretation changes without rewriting event history |
| E11 reconciliation | G2, G4, G7, G8 | conflict resolution remains auditable and does not erase source events |
| E12 dependent decision reconciliation | G1, G4, G7, G8 | corrected evidence propagates to dependent decisions/review |
| E13 quarantined event | G1, G2, G4, G8 | invalid input cannot produce protected state or untraceable effects |
| E14 non-idempotent external effect | G1, G4, G8 | external execution requires durable status and safe retry/compensation |
| E15 event data minimization | G2, G3, G5, G6, G8 | event processing cannot become unrestricted profile construction or surveillance |

### Phase 3 release-gate rules

1. Event Engine correctness MUST NOT be treated as sufficient evidence of policy or authority correctness.
2. Replay MUST remain subject to G4 and MUST NOT execute external Action semantics a second time.
3. Reconciliation MUST preserve the distinction between Evidence, Decision and Action required by G1 and G7.
4. Event visibility MUST remain bounded by the privacy/federation controls represented by G2, G3, G5 and G6.
5. Unknown, unresolved or quarantined event conditions MUST remain distinguishable from negative business outcomes.
6. A Phase 3 change that alters any release-gate invariant requires explicit architectural review before implementation.

### Phase 3 closure status

The documented E01–E15 cases now have explicit traceability to the existing regression groups and release gates. This is a documentation-level cross-check; runtime Event Engine execution and production certification remain unclaimed.


## Phase 4 Projection release-gate cross-check

| Projection case | Release gates | Required property |
|---|---|---|
| P01 rebuild | G1, G4, G8 | deterministic rebuild without repeated Action effects |
| P02 version change | G4, G8 | derived interpretation changes without rewriting Event History |
| P03 projection lag | G4, G7, G8 | stale state is explicit and not mistaken for current truth |
| P04 stale high-impact input | G1, G6, G7, G8 | protected Decision cannot silently rely on stale data |
| P05 failed projection | G4, G8 | durable source event survives projection failure and safe retry |
| P06 evidence correction | G1, G4, G7, G8 | dependent Decision basis is re-evaluated when required |
| P07 unknown preservation | G7, G8 | missing information remains UNKNOWN rather than negative outcome |
| P08 permission projection | G5, G6, G8 | technical access cannot become Permission authority |
| P09 privacy boundary | G2, G3, G5, G6, G8 | denormalization cannot broaden access or profile construction |
| P10 aggregate isolation | G2, G3, G6, G7, G8 | aggregate analytics cannot silently become individual ranking |
| P11 projection deletion | G2, G4, G5, G8 | derived deletion does not falsify historical provenance |
| P12 concurrent rebuild | G1, G4, G8 | checkpoint/version rules prevent lost or duplicated effects |

### Phase 4 release rules

1. No projection may become a hidden source of authority merely because it is faster or easier to query.
2. Freshness is part of semantic validity whenever a read is used for a protected Decision, Permission or Action.
3. Projection failure is an operational state, not evidence that the underlying subject/entity is negative, absent or invalid.
4. Rebuild and correction paths preserve Event History and remain independently auditable.
5. Projection access remains subject to privacy, purpose limitation and human-review controls already established by G1–G8.

Phase 4 release-gate cross-check is documentation-complete for P01–P12. Runtime projection implementation and executable release testing remain unclaimed.


## Phase 5 Provenance release-gate cross-check

| Provenance case | Release gates | Required property |
|---|---|---|
| V01 Decision provenance | G1, G4, G8 | Evidence, Policy and Decision dependencies remain distinct and reconstructable |
| V02 Evidence revocation | G1, G4, G7, G8 | affected descendants are identified without rewriting history |
| V03 Policy version correction | G1, G4, G8 | obsolete policy basis remains historical and affected decisions are identifiable |
| V04 Missing provenance | G4, G7, G8 | missing lineage remains UNKNOWN/UNRESOLVED |
| V05 Authority confusion | G1, G4, G8 | verified Evidence cannot become Action authority |
| V06 Dependency cycle | G4, G8 | invalid causal/dependency structure is quarantined or explicitly modeled |
| V07 Projection lineage | G2, G4, G8 | read representation remains traceable to source history |
| V08 Action lineage | G1, G4, G8 | authorization and execution remain separate |
| V09 Privacy-bounded traversal | G2, G3, G5, G6, G8 | provenance access does not broaden privacy scope |
| V10 Reconciliation propagation | G1, G4, G7, G8 | corrections propagate to affected descendants without silent overwrite |
| V11 Supersession | G4, G8 | historical provenance remains auditable across versions |
| V12 Aggregate provenance | G2, G3, G6, G7, G8 | aggregate verification does not expose hidden individual profiling |

### Phase 5 release rules

1. Provenance is explanatory and evidentiary; it does not grant authority.
2. A complete graph does not make an unsupported claim true; source verification remains independent.
3. Missing lineage is an epistemic condition and cannot silently become a negative subject status.
4. Propagation identifies affected descendants but does not retroactively falsify historical events.
5. Provenance traversal remains bounded by purpose, permission and data minimization.
6. Changes to dependency semantics that affect authority, privacy or impact require architectural review.

Phase 5 release-gate cross-check is documentation-complete for V01–V12. Runtime graph execution remains unclaimed.


## Phase 6 Release Gate: Policy Engine / Impact Evaluation

Q01–Q12 are cross-checked against the existing G1–G8 structural gates. These gates validate architectural separation and safety properties; they do not constitute runtime certification.

| Phase 6 case | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
|---|---|---|---|---|---|---|---|---|
| Q01 Policy versioning |  |  |  | ✓ |  |  |  | ✓ |
| Q02 Evidence insufficiency |  |  |  | ✓ |  | ✓ | ✓ | ✓ |
| Q03 Impact escalation | ✓ |  |  |  |  | ✓ |  | ✓ |
| Q04 Subject-value scoring | ✓ | ✓ | ✓ |  | ✓ | ✓ | ✓ | ✓ |
| Q05 Permission vs authority | ✓ |  | ✓ |  | ✓ | ✓ |  | ✓ |
| Q06 Evidence vs execution | ✓ |  |  | ✓ |  | ✓ |  | ✓ |
| Q07 Stale projection |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ |
| Q08 Policy conflict | ✓ |  |  | ✓ |  | ✓ | ✓ | ✓ |
| Q09 High-impact automation | ✓ | ✓ |  |  | ✓ | ✓ | ✓ | ✓ |
| Q10 Explanation minimization |  | ✓ | ✓ |  | ✓ | ✓ | ✓ | ✓ |
| Q11 Policy change propagation |  |  |  | ✓ |  | ✓ | ✓ | ✓ |
| Q12 Recovery/appeal | ✓ |  |  | ✓ | ✓ | ✓ | ✓ | ✓ |

### Phase 6 gate criteria

1. Policy evaluation remains separate from Action execution.
2. Impact classification never becomes a subject-value score.
3. High-impact operations retain human review.
4. UNKNOWN/REVIEW_REQUIRED is preserved when evidence, provenance or policy resolution is insufficient.
5. Policy versions and historical outcomes remain reconstructable.
6. Technical access, Projection visibility or provenance visibility cannot create normative authority.
7. Explanations remain purpose-bound and privacy-minimized.
8. Q01–Q12 have explicit expected outcomes and G1–G8 traceability.

**Architectural Phase 6 gate: PASS.** Runtime implementation and executable conformance testing are not claimed by this documentation gate.


## Phase 7 Release Gate: Human Review

H01–H10 are checked against G1–G8 to ensure Human Review strengthens oversight without creating hidden authority, unrestricted profiling or direct execution powers.

| Phase 7 case | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
|---|---|---|---|---|---|---|---|---|
| H01 Review trigger | ✓ |  |  |  |  | ✓ |  | ✓ |
| H02 Minimal review packet |  | ✓ | ✓ |  | ✓ | ✓ |  | ✓ |
| H03 Reviewer conflict | ✓ |  |  |  |  | ✓ |  | ✓ |
| H04 Structured outcome | ✓ | ✓ |  | ✓ |  | ✓ |  | ✓ |
| H05 Review deadline | ✓ |  |  |  |  | ✓ | ✓ | ✓ |
| H06 Temporary restriction expiry | ✓ |  |  | ✓ |  | ✓ | ✓ | ✓ |
| H07 Action separation | ✓ |  |  |  |  | ✓ |  | ✓ |
| H08 Reversal history | ✓ |  |  | ✓ |  | ✓ | ✓ | ✓ |
| H09 Contestability | ✓ |  |  | ✓ |  | ✓ | ✓ | ✓ |
| H10 Review-data expansion |  | ✓ | ✓ |  | ✓ | ✓ | ✓ | ✓ |

### Phase 7 gate criteria

1. Review triggers and outcomes are explicit and auditable.
2. Review access remains purpose-bound and minimally disclosed.
3. Reviewer conflicts are visible and have an escalation/reassignment path.
4. Human Review cannot directly execute protected Actions.
5. High-impact review has a target deadline; temporary restrictions have expiry/re-check conditions.
6. Reversal and recovery preserve original history.
7. Contestability remains explicit where applicable.
8. H01–H10 have defined outcomes and G1–G8 traceability.

**Architectural Phase 7 gate: PASS.** Runtime queue assignment, SLA enforcement and executable conformance are not claimed.


## Phase 8 Release Gate: Audit / Observability

A01–A10 are cross-checked against G1–G8. The gate verifies that auditability remains distinct from surveillance, telemetry remains distinct from authority, and protected history remains reconstructable without unrestricted subject profiling.

| Phase 8 case | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
|---|---|---|---|---|---|---|---|---|
| A01 Purpose-bound audit |  | ✓ |  | ✓ | ✓ |  |  | ✓ |
| A02 Telemetry separation | ✓ | ✓ | ✓ |  | ✓ |  | ✓ | ✓ |
| A03 Audit access |  | ✓ | ✓ |  | ✓ | ✓ |  | ✓ |
| A04 Audit integrity | ✓ | ✓ |  | ✓ |  |  | ✓ | ✓ |
| A05 Audit access audit |  | ✓ |  | ✓ | ✓ | ✓ |  | ✓ |
| A06 Aggregate-to-profile escalation |  | ✓ | ✓ |  | ✓ | ✓ | ✓ | ✓ |
| A07 High-impact monitoring | ✓ | ✓ |  |  | ✓ | ✓ |  | ✓ |
| A08 Audit outage | ✓ | ✓ |  | ✓ |  |  | ✓ | ✓ |
| A09 Retention expiry |  | ✓ |  | ✓ | ✓ | ✓ |  | ✓ |
| A10 Correction propagation | ✓ | ✓ |  | ✓ | ✓ | ✓ | ✓ | ✓ |

### Phase 8 gate criteria

1. Audit has explicit purpose, retention and access boundaries.
2. AuditRecord, operational telemetry, security telemetry and debug logs remain distinct.
3. Audit access is itself auditable and cannot create authority.
4. Historical audit records are tamper-evident and corrections do not silently overwrite history.
5. Aggregate observability cannot silently become individual profiling.
6. High-impact monitoring preserves existing review and privacy controls.
7. Audit outage behavior is explicit for protected operations.
8. A01–A10 have defined outcomes and G1–G8 traceability.

**Architectural Phase 8 gate: PASS.** Runtime storage, integrity enforcement, retention execution and production observability are not claimed.

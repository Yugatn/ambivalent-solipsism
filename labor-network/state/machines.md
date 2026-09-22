# State Machines СТСети

Каждая существенная сущность имеет явные допустимые переходы.

Переход описывается:

- from;
- event;
- guard;
- to;
- side effects;
- audit;
- recovery.

Недопустимый переход не должен выполняться только потому, что его позволяет UI или API.

## 1. Opportunity

Состояния: draft, published, paused, filled, expired, withdrawn.

## 2. Engagement

Состояния: proposed, accepted, active, paused, completed, terminated, disputed.

## 3. Evidence

Состояния: asserted, pending_verification, verified, challenged, expired, revoked, superseded.

**Challenged не означает автоматически false.**

## 4. Decision

Состояния: proposed, evaluated, permitted, denied, review_required, reviewed, reversed, superseded.

## 5. Dispute

Состояния: opened, acknowledged, investigating, resolved, escalated, withdrawn.

## 6. Support

Состояния: available, requested, approved, active, completed, suspended, revoked.

## 7. Guard conditions

Переход может зависеть от полномочий actor, версии policy, статуса evidence, времени, основания доступа, класса воздействия и human review.

## 8. Terminal states

Терминальное состояние не уничтожает историю. История сохраняется как provenance.

## 9. Semantic invariant

State представляет текущую конфигурацию сущности. Event сохраняет произошедшее. Decision определяет допустимое последствие. Action фиксирует фактическое применение.

State не заменяет event history и не должен использоваться как единственный источник реконструкции существенного прошлого.



## 10. Phase 2 state classification for all canonical entities

Not every entity requires a mutable lifecycle state. The canonical model distinguishes **stateful**, **validity-oriented**, and **append-only / projection-oriented** entities.

### Stateful entities

**Subject**
States: active, restricted, exited.
Restriction is contextual and purpose-bound; it is not a value judgment.

**Organization**
States: registered, active, suspended, closed.
Closure preserves historical records.

**Opportunity**
States: draft, published, paused, filled, expired, withdrawn.

**Engagement**
States: proposed, accepted, active, paused, completed, terminated, disputed.

**Evidence**
States: asserted, pending_verification, verified, challenged, expired, revoked, superseded.

**Decision**
States: proposed, evaluated, permitted, denied, review_required, reviewed, reversed, superseded.

**Permission**
States: proposed, granted, modified, expired, revoked.
A technical credential does not create a Permission state.

**Dispute**
States: opened, acknowledged, investigating, resolved, escalated, withdrawn.

**Support**
States: available, requested, approved, active, completed, suspended, revoked.

**Resource**
States: registered, available, allocated, unavailable, released.
Availability does not itself grant access.

### Validity-oriented entities

**Relation**
Validity is represented by asserted, confirmed, expired, revoked, with provenance and context. It must not be interpreted as a global subject score.

### Append-only / projection-oriented entities

**Event**
No mutable lifecycle state replaces event history. Processing status such as appended, acknowledged or reconciled is operational metadata.

**AuditRecord**
The record is append-oriented. Retention or restriction status is metadata governed by policy; it must not rewrite the audited event.

### Derived / evaluation entities

**PolicyDecision**
States: evaluated, review_required, permitted, denied, superseded.
PolicyDecision is an evaluation result, not execution.

**Action**
States: requested, authorized, executing, executed, failed, compensated.
Action remains separate from Decision.

### Phase 2 state rules

1. Every stateful entity has an explicit state set.
2. Validity-oriented entities retain provenance and temporal validity.
3. Append-only entities cannot use current status to erase historical facts.
4. Derived states must remain traceable to their inputs and policy version.
5. Terminal states remain reconstructable from event history.
6. A state transition requires a canonical event or explicitly documented system process.
7. State labels cannot be used as hidden value judgments about a subject.
8. Any new state requires an invariant mapping and transition specification before implementation.

### Phase 2 closure condition

Phase 2 state coverage is complete at the architectural level when all 15 canonical entities have either:
- an explicit state model;
- an explicit validity model; or
- an explicit append-only/derived model.

Runtime state-machine implementation and automated execution tests remain implementation work.

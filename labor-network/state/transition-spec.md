# Спецификация переходов состояния

Переход описывается как current state + event + guard = next state.

Система не должна менять существенное состояние только потому, что изменилось поле данных. Изменение состояния должно иметь событие или явно определённый системный процесс.

Каждый защищённый переход проверяет полномочие инициатора и применяет версию политики, действующую для данного контекста.

Переходы могут зависеть от срока действия данных, договора или программы.

Чем выше потенциальное воздействие, тем больше обязательных проверок может потребоваться.

Для определённых переходов условием завершения является Human Review.

Повторное применение уже обработанного события не создаёт нового эффекта.

Недопустимый переход отклоняется и создаёт диагностическое событие, а не изменяет состояние частично.

После технической ошибки должен существовать определённый путь восстановления без тихой потери истории.


## Phase 2 transition coverage

The Phase 2 state model is now mapped to protected lifecycle behavior.

### Required transition contract

Every protected transition MUST define:

- current state;
- event type;
- actor/source;
- authority guard;
- policy version;
- evidence/provenance requirements;
- next state;
- side effects, if any;
- audit record;
- recovery path;
- idempotency behavior.

### Core transition groups

**Opportunity**
- draft → published: publish event, authority and completeness guard.
- published → paused: pause event, authorized actor.
- published → filled: valid engagement/fulfillment condition.
- published → expired: validity boundary.
- published → withdrawn: authorized withdrawal.

**Engagement**
- proposed → accepted: acceptance event and participant authority.
- accepted → active: activation guard.
- active → paused: authorized pause.
- active → completed: completion evidence.
- active → terminated: termination basis.
- active/paused → disputed: dispute opening without rewriting prior history.

**Evidence**
- asserted → pending_verification → verified: provenance and verification.
- verified → challenged: contest event; does not imply false.
- verified → expired: validity boundary.
- verified → revoked: authorized revocation with reason.
- challenged → verified: successful review.
- challenged → superseded: replacement evidence while preserving lineage.

**Decision**
- proposed → evaluated: evaluation event.
- evaluated → permitted/denied: policy and authority guards.
- evaluated → review_required: impact/uncertainty guard.
- review_required → reviewed: required review completed.
- reviewed → permitted/denied/reversed: review outcome.
- permitted/denied → superseded: newer applicable decision.
- permitted → reversed: authorized reversal with provenance.

**Dispute**
- opened → acknowledged → investigating → resolved/escalated.
- opened/investigating → withdrawn only through an explicit withdrawal event.
- resolution never deletes the disputed evidence lineage.

**Support**
- available → requested → approved → active → completed.
- approved/active → suspended/revoked only with explicit basis.
- completion/revocation preserves support history.

### Transition safety rules

1. No transition is inferred solely from a field mutation.
2. A rejected transition produces a diagnostic/audit event and does not partially mutate state.
3. Duplicate events are idempotent.
4. Recovery restores a consistent state without deleting event history.
5. Terminal states remain historically reconstructable.
6. A state projection must be reproducible from the relevant event history.
7. High-impact transitions cannot bypass required human review.
8. A guard failure cannot be converted into a successful transition by UI/API behavior.

## Phase 2 gate

State Machines Phase is structurally complete when every protected lifecycle has:
- explicit states;
- allowed transitions;
- guards;
- invariant mapping;
- audit behavior;
- recovery behavior;
- negative transition cases.

Runtime execution of these transitions remains an implementation task.


## Phase 2 full state-to-transition cross-check

The state classification and lifecycle matrix were compared. The following stateful/derived models now have explicit transition coverage requirements:

| Entity | State model | Required transition coverage |
|---|---|---|
| Subject | active, restricted, exited | create/update/consent/restrict/exit; reopening only by explicit rule |
| Organization | registered, active, suspended, closed | register/activate/suspend/close |
| Opportunity | draft, published, paused, filled, expired, withdrawn | publish/pause/fill/expire/withdraw |
| Engagement | proposed, accepted, active, paused, completed, terminated, disputed | propose/accept/activate/pause/complete/terminate/dispute |
| Evidence | asserted, pending_verification, verified, challenged, expired, revoked, superseded | assert/verify/challenge/expire/revoke/supersede |
| Decision | proposed, evaluated, permitted, denied, review_required, reviewed, reversed, superseded | propose/evaluate/permit/deny/review/reverse/supersede |
| Action | requested, authorized, executing, executed, failed, compensated | request/authorize/execute/fail/compensate |
| PolicyDecision | evaluated, review_required, permitted, denied, superseded | evaluate/review/permit/deny/supersede |
| Permission | proposed, granted, modified, expired, revoked | grant/modify/expire/revoke |
| Dispute | opened, acknowledged, investigating, resolved, escalated, withdrawn | open/acknowledge/investigate/resolve/escalate/withdraw |
| Support | available, requested, approved, active, completed, suspended, revoked | offer/request/approve/activate/suspend/complete/revoke |
| Resource | registered, available, allocated, unavailable, released | register/update/allocate/release/unavailable |

### Cross-check findings

1. Every declared state has a documented entry path or is an initial state.
2. Every declared protected transition has a target state present in the corresponding state set.
3. Relation is validity-oriented rather than a mutable lifecycle state.
4. Event and AuditRecord remain append-oriented and do not require ordinary lifecycle transitions.
5. No transition is allowed to invent a state absent from the canonical state set.
6. New transition definitions must update both this specification and the Entity × Event Matrix.
7. Any transition that changes authority, privacy scope, subject control or impact class requires the corresponding policy/review guard.

### Phase 2 gate status

The cross-check is **architecturally closed** for the declared state sets and lifecycle events. Runtime execution tests remain separate and are not implied by this documentation check.

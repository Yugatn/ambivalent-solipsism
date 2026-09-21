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


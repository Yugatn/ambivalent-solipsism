# Формальная верификация СТСети

Формальная проверка подтверждает, что реализация сохраняет ключевые инварианты при допустимых последовательностях событий.

## Проверяемые свойства
- недопустимый переход не изменяет защищённое состояние;
- отозванное разрешение не используется по этому разрешению;
- дубликат события не создаёт дополнительного эффекта;
- unknown не превращается молча в факт;
- high-impact action не обходит обязательный review;
- исправление может достигать зависимых решений;
- audit trail сохраняет атрибуцию;
- изменение состояния имеет валидное событие.

## Safety properties
Некоторые свойства должны быть истинны всегда. Например: отсутствие полномочия не создаёт полномочие.

## Liveness properties
Некоторые процессы должны иметь возможность завершиться. Например: открытый dispute не должен навсегда оставаться без предусмотренного процесса обработки.

## Bounded recovery
После сбоя должен существовать ограниченный и определённый путь восстановления.

## Model checking
State machines могут быть представлены в TLA+, Alloy или другом формальном языке. Выбор инструмента является отдельным инженерным решением.

## Trace validation
Проверяется не только итоговое состояние, но и последовательность событий.

## Counterexample
При нарушении инварианта полезным результатом является минимальная последовательность событий, демонстрирующая нарушение.

> Проверять необходимо не только то, что система умеет делать, но и то, что она принципиально не должна уметь делать.


## Phase 10 Formal Verification contract

Formal Verification defines machine-checkable models for the highest-risk state, authority and history boundaries. It complements the documented contracts; it does not replace runtime tests, security testing or deployment validation.

### 1. Model boundary

The initial formal model MUST cover the smallest critical kernel: protected state transitions, Permission/authority guards, Evidence validity, Decision/Action separation, mandatory Human Review, event idempotency, Unknown preservation, correction propagation and exit integrity.

### 2. State abstraction

The model MAY abstract away UI, storage and transport details when those details are not necessary to prove the selected properties. Every abstraction MUST document which real-system property it represents and which behavior remains outside the proof boundary.

### 3. Safety properties

The model MUST express at least:

- no unauthorized transition;
- no Decision-to-Action bypass;
- no duplicate protected effect from one event;
- no Unknown-to-negative inference;
- no high-impact bypass of required review;
- no authority creation from data possession or federation connectivity;
- no silent historical overwrite;
- no hidden exit penalty.

### 4. Liveness and bounded recovery

Where the domain requires eventual handling, the model SHOULD express liveness properties such as review/dispute progress and bounded recovery. Liveness MUST NOT be used to justify unsafe automatic fallback.

### 5. Trace and counterexample

A failed property MUST yield a reproducible trace or minimal counterexample where supported by the selected formal method. The trace MUST identify the initial state, triggering events, violated invariant and terminal condition.

### 6. Refinement

When the formal model is later connected to executable code, the mapping between abstract states/events and implementation states/events MUST be explicit. Passing the abstract model alone MUST NOT be presented as proof that an implementation conforms to it.

### 7. Unknown and nondeterminism

The model MUST preserve unresolved states rather than choosing an arbitrary business outcome merely to make the model deterministic. Where multiple valid resolutions exist, nondeterminism or explicit policy resolution SHOULD be modeled rather than hidden.

### 8. Versioning

Formal models, assumptions, invariants and verification results MUST be versioned. A change to a protected invariant invalidates the corresponding proof obligation until rechecked.

### Phase 10 invariants

- FV1: proof scope is explicit;
- FV2: critical safety properties are machine-checkable;
- FV3: abstractions document their limits;
- FV4: counterexamples are traceable;
- FV5: liveness does not weaken safety;
- FV6: Unknown/nondeterministic states are preserved where semantically required;
- FV7: model/version changes invalidate affected proof obligations until rechecked;
- FV8: formal proof is not conflated with runtime or production certification.

Initial formalization should target the critical kernel before attempting to model the entire network.


## Phase 10A Critical Formal Kernel

Before selecting a concrete model checker, the formal target is narrowed to a minimal critical kernel. This prevents proof scope from expanding faster than the executable implementation can be mapped to it.

### Kernel state

The kernel state consists of:

- aggregate state and protected transition status;
- Permission/authority context;
- Evidence validity and provenance status;
- PolicyDecision status and impact class;
- Human Review status where required;
- Event identity and processed-event set;
- immutable historical event references;
- Action execution status;
- explicit UNKNOWN/UNRESOLVED markers.

### Kernel transitions

The minimum transition vocabulary is:

1. propose protected operation;
2. evaluate evidence/provenance;
3. evaluate policy and impact;
4. require/complete human review;
5. create normative Decision;
6. authorize/start/complete Action;
7. record Event;
8. reject/quarantine invalid event;
9. correct/revoke/supersede dependent information;
10. recover after processing failure.

### Kernel proof obligations

K01 — unauthorized transitions are unreachable.

K02 — a Decision cannot directly imply completed Action without the required execution path.

K03 — one event identity cannot create duplicate protected effects.

K04 — unresolved evidence/provenance cannot produce a negative subject outcome merely through absence.

K05 — high-impact operations cannot reach protected execution while mandatory Human Review is incomplete.

K06 — technical data possession, Projection access or federation connectivity cannot expand normative authority.

K07 — correction preserves the original historical event and creates an explicit corrective path.

K08 — recovery cannot duplicate a completed protected effect.

K09 — UNKNOWN/UNRESOLVED remains representable throughout the kernel.

K10 — terminal historical records remain reconstructable.

### Refinement boundary

The kernel is a proof target, not a replacement architecture. Each future executable implementation component MUST map to one or more kernel state variables, transitions or explicit out-of-scope behavior. Any implementation behavior without a documented mapping is not covered by the kernel proof.

### Phase 10A status

The critical formal kernel is structurally specified. Concrete model-checker syntax and executable refinement are the next implementation step and are not claimed here.

# Semantic Audit

## Scope

Проверка проводится по всем 66 legacy-файлам labor-network.

## Method

Для каждого источника:

1. фиксируется назначение;
2. выделяются самостоятельные смысловые блоки;
3. определяется новый canonical destination;
4. проверяется сохранение ограничений и зависимостей;
5. отмечаются refinement или merge;
6. фиксируются pending blocks.

## Audit status

### Architecture
Covered by:
- architecture/overview.md
- architecture/entity-model.md
- architecture/entity-event-matrix.md
- architecture/consistency-model.md
- architecture/technical-core.md
- architecture/information-architecture.md
- architecture/review.md
- architecture/implementation-roadmap.md

Status: **covered**

### Policy and governance
Covered by:
- policy/
- governance/principles.md
- decision/human-review.md
- decision/impact.md

Status: **covered**

### Events, state and decisions
Covered by:
- event/
- state/
- decision/
- action/

Status: **covered**

### Evidence and trust
Covered by:
- evidence/
- domain/reputation.md
- evidence/trust-and-provenance.md

Status: **covered**

### Privacy and security
Covered by:
- privacy/
- security/

Status: **covered**

### Support and regional development
Covered by:
- support/
- regional/

Status: **covered**

### Integration and federation
Covered by:
- integration/
- federation contract
- schema contract
- state interface

Status: **covered**

### Verification and migration
Covered by:
- verification/
- migration/

Status: **covered**

## Important distinction

“Covered” означает, что для соответствующей предметной области существует canonical destination. Это не утверждение о дословном совпадении документов.

Следующий контроль должен проверять конкретные смысловые блоки legacy-файлов и их traceability.

## Legacy preservation

Legacy files remain untouched and serve as the comparison baseline until the semantic audit is closed.

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


## Block-level audit register

The following legacy concerns are explicitly represented in the structured architecture:

| Legacy concern | Canonical destination | Treatment |
|---|---|---|
| architecture | architecture/ | refined |
| entity model | architecture/entity-model.md | refined |
| event protocol | event/ | refined |
| state machines | state/ | refined |
| policy engine | policy/ | refined |
| permissions and consent | privacy/ + policy/ | refined |
| professional profile | domain/professional-profile.md | preserved/refined |
| recruitment and matching | domain/ + policy/ | refined |
| education and skills | domain/ + support/ | refined |
| remuneration | economy/ | refined |
| self-employment | domain/ | preserved/refined |
| regional development | regional/ | refined |
| transport/work integration | regional/ | refined |
| social protection | support/ | refined |
| solidarity fund | support/ | refined |
| evidence/provenance | evidence/ | refined |
| reputation | domain/reputation.md | preserved/refined |
| disputes | dispute/ + decision/ | refined |
| audit/observability | audit/ | refined |
| privacy/data governance | privacy/ | refined |
| security/safety kernel | security/ | refined |
| API/interoperability | integration/ | refined |
| formal verification | verification/ | refined |
| migration controls | migration/ | refined |

This register records the semantic destination at the domain level. Detailed source-to-block verification remains the final audit step.


## High-risk semantic controls

The following areas require explicit preservation checks because structural refactoring can otherwise change meaning:

1. **Authority vs capability**  
   Technical access must remain distinct from normative authority.

2. **Evidence vs decision**  
   Evidence must not become an implicit decision.

3. **Decision vs action**  
   A decision must not be treated as proof that an action was executed.

4. **State vs history**  
   Current state must not replace the event history.

5. **Restriction vs subject value**  
   Restrictions are contextual controls, not judgments of a subject's worth.

6. **Aggregate analytics vs individual profiling**  
   Regional and system analytics must not silently become individual ranking.

7. **Support vs control**  
   Support mechanisms must retain their stated purpose and not become hidden control channels.

8. **Audit vs surveillance**  
   Audit data must remain purpose-limited and proportional.

9. **Automation vs review**  
   High-impact automated outcomes retain their prescribed review path.

10. **Legacy vs canonical source**  
    Legacy documents remain comparison material and do not create a second active canonical model.

These controls are mandatory during final source-to-block verification.

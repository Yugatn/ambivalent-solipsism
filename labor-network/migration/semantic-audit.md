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


## Final semantic review matrix

| Control | Required invariant | Status |
|---|---|---|
| Authority | capability never creates authority | covered |
| Evidence | evidence remains distinguishable from decision | covered |
| Decision | decision remains distinguishable from action | covered |
| State | current state remains distinguishable from history | covered |
| Restriction | contextual restriction has scope and review | covered |
| Analytics | aggregate data does not imply individual rank | covered |
| Support | support retains declared purpose | covered |
| Audit | audit is purpose-limited | covered |
| Automation | high-impact results retain review path | covered |
| Legacy | legacy source remains non-canonical | covered |

### Review result

All currently identified high-risk semantic controls have an explicit destination and architectural invariant.

No legacy file is deleted at this checkpoint.

The remaining work is regression validation: verify that the structured modules and their cross-links do not contradict one another after consolidation.


## Pairwise verification log

The following legacy-to-canonical pairs were rechecked against the current branch during the continuation audit:

- regional-development.md → regional/development.md — exact preservation
- regional-economy.md → regional/economy.md — exact preservation
- regional-nodes.md → regional/nodes.md — exact preservation
- regression-suite.md → verification/regression-suite.md — exact preservation
- safety-kernel.md → security/safety-kernel.md — exact preservation
- schema-contract.md → integration/schema-contract.md — exact preservation
- self-employed.md → domain/self-employed.md — exact preservation
- social-protection.md → support/social-protection.md — exact preservation
- solidarity-fund.md → support/solidarity-fund.md — exact preservation
- state-interface.md → integration/state-interface.md — exact preservation
- state-transition-spec.md → state/transition-spec.md — exact preservation
- subject-control.md → privacy/subject-control.md — exact preservation
- tax-and-contribution.md → economy/tax-and-contribution.md — exact preservation
- technical-core.md → architecture/technical-core.md — exact preservation
- test-scenarios.md → verification/test-scenarios.md — exact preservation
- traceability-matrix.md → migration/traceability-matrix.md — exact preservation
- transition-and-unemployment.md → support/transition-and-unemployment.md — exact preservation
- transport-work-integration.md → regional/transport-work-integration.md — exact preservation
- trust-and-provenance.md → evidence/trust-and-provenance.md — exact preservation
- work-lifecycle.md → state/work-lifecycle.md — exact preservation
- api-and-interoperability.md → integration/api-and-interoperability.md — exact preservation

### Intentional refinements

- reputation.md → domain/reputation.md — non-identical canonical text is an intentional refinement already audited; legacy remains unchanged as baseline.

These results are verification evidence, not a claim that the entire semantic audit is closed.

## Final pairwise closure checkpoint

Additional final checks completed:

- api-and-interoperability.md → integration/api-and-interoperability.md — exact preservation
- architecture.md → architecture/overview.md — exact preservation
- education-and-prof-map.md → domain/education-and-prof-map.md — exact preservation
- index.html → ui/index.html — exact preservation
- principles.md → governance/principles.md — exact preservation
- entity-event-matrix.md → architecture/entity-event-matrix.md — exact preservation
- entity-model.md → architecture/entity-model.md — exact preservation
- event-protocol.md → event/protocol.md — exact preservation
- federation-contract.md → integration/federation-contract.md — exact preservation
- formal-verification.md → verification/formal-verification.md — exact preservation
- human-review.md → decision/human-review.md — exact preservation
- subject-and-motivation.md → domain/subject-and-motivation.md — exact preservation
- work-conditions.md → domain/work-conditions.md — exact preservation
- transition-and-unemployment.md → support/transition-and-unemployment.md — exact preservation
- transport-work-integration.md → regional/transport-work-integration.md — exact preservation
- trust-and-provenance.md → evidence/trust-and-provenance.md — exact preservation
- work-lifecycle.md → state/work-lifecycle.md — exact preservation

### Intentional canonical refinements confirmed

The following non-identical pairs were inspected at line level and classified as intentional canonical refinements rather than silent loss:

- employer-and-recruitment.md → domain/employer-and-recruitment.md
- reputation.md → domain/reputation.md
- professional-history.md → domain/professional-history.md
- professional-profile.md → domain/professional-profile.md
- proof-of-development.md → domain/proof-of-development.md

The canonical versions retain the substantive legacy constraints while adding or consolidating architectural rules. Legacy baselines remain untouched.

### Manifest closure

MIGRATION_MANIFEST.md → migration/manifest.md was found to be incomplete and was repaired in commit aa3042a01a7134aa30fa8176bc746f7850c2059f3. The canonical manifest now retains the historical migration baseline, current 66-file coverage, semantic classifications, and completion criteria.

At this checkpoint, the identified legacy-to-canonical pairwise audit has no unresolved content-loss finding. The remaining work is cross-module consistency and regression validation, not filename migration.

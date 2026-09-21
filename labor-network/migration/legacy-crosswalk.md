# Legacy Crosswalk

This document is the authoritative migration crosswalk for the legacy labor-network root files.

## Rule

Every legacy file has an explicit destination. The legacy file remains unchanged until content-level verification is complete.

## Crosswalk

- `labor-network/api-and-interoperability.md` → `labor-network/integration/api-and-interoperability.md`
- `labor-network/architecture-review.md` → `labor-network/architecture/review.md`
- `labor-network/architecture.md` → `labor-network/architecture/overview.md`
- `labor-network/audit-and-observability.md` → `labor-network/audit/observability-architecture.md`
- `labor-network/benefits-and-incentives.md` → `labor-network/support/benefits-and-incentives.md`
- `labor-network/collective-action.md` → `labor-network/collective/action.md`
- `labor-network/consistency-model.md` → `labor-network/architecture/consistency-model.md`
- `labor-network/content-audit.md` → `labor-network/migration/content-audit.md`
- `labor-network/data-governance.md` → `labor-network/privacy/data-governance.md`
- `labor-network/decision-lifecycle.md` → `labor-network/decision/decision-lifecycle.md`
- `labor-network/digital-access.md` → `labor-network/support/digital-access.md`
- `labor-network/dispute-resolution.md` → `labor-network/dispute/resolution.md`
- `labor-network/economy-and-remuneration.md` → `labor-network/economy/remuneration.md`
- `labor-network/education-and-prof-map.md` → `labor-network/domain/education-and-prof-map.md`
- `labor-network/education-and-skills.md` → `labor-network/domain/education-and-skills.md`
- `labor-network/employer-and-recruitment.md` → `labor-network/domain/employer-and-recruitment.md`
- `labor-network/entity-event-matrix.md` → `labor-network/architecture/entity-event-matrix.md`
- `labor-network/entity-model.md` → `labor-network/architecture/entity-model.md`
- `labor-network/event-protocol.md` → `labor-network/event/protocol.md`
- `labor-network/federation-contract.md` → `labor-network/integration/federation-contract.md`
- `labor-network/formal-verification.md` → `labor-network/verification/formal-verification.md`
- `labor-network/human-review.md` → `labor-network/decision/human-review.md`
- `labor-network/identity-and-consent.md` → `labor-network/privacy/identity-and-consent.md`
- `labor-network/implementation-roadmap.md` → `labor-network/architecture/implementation-roadmap.md`
- `labor-network/index.html` → `labor-network/ui/index.html`
- `labor-network/information-architecture.md` → `labor-network/architecture/information-architecture.md`
- `labor-network/infrastructure-and-mobility.md` → `labor-network/regional/infrastructure-and-mobility.md`
- `labor-network/integration-map.md` → `labor-network/integration/map.md`
- `labor-network/invariants.md` → `labor-network/verification/invariants.md`
- `labor-network/local-projects.md` → `labor-network/domain/local-projects.md`
- `labor-network/migration-map.md` → `labor-network/migration/map.md`
- `labor-network/permissions-and-consent.md` → `labor-network/privacy/permissions-and-consent.md`
- `labor-network/policy-engine.md` → `labor-network/policy/engine.md`
- `labor-network/principles.md` → `labor-network/governance/principles.md`
- `labor-network/privacy-and-state-integration.md` → `labor-network/privacy/state-integration.md`
- `labor-network/professional-history.md` → `labor-network/domain/professional-history.md`
- `labor-network/professional-profile.md` → `labor-network/domain/professional-profile.md`
- `labor-network/proof-of-development.md` → `labor-network/domain/proof-of-development.md`
- `labor-network/public-programs.md` → `labor-network/support/public-programs.md`
- `labor-network/reconciliation-graph.md` → `labor-network/decision/reconciliation-graph.md`
- `labor-network/recruitment-and-matching.md` → `labor-network/domain/recruitment-and-matching.md`
- `labor-network/regional-development.md` → `labor-network/regional/development.md`
- `labor-network/regional-economy.md` → `labor-network/regional/economy.md`
- `labor-network/regional-nodes.md` → `labor-network/regional/nodes.md`
- `labor-network/regression-suite.md` → `labor-network/verification/regression-suite.md`
- `labor-network/reputation.md` → `labor-network/domain/reputation.md`
- `labor-network/safety-kernel.md` → `labor-network/security/safety-kernel.md`
- `labor-network/schema-contract.md` → `labor-network/integration/schema-contract.md`
- `labor-network/self-employed.md` → `labor-network/domain/self-employed.md`
- `labor-network/social-protection.md` → `labor-network/support/social-protection.md`
- `labor-network/solidarity-fund.md` → `labor-network/support/solidarity-fund.md`
- `labor-network/state-interface.md` → `labor-network/integration/state-interface.md`
- `labor-network/state-machines.md` → `labor-network/state/machines.md`
- `labor-network/state-transition-spec.md` → `labor-network/state/transition-spec.md`
- `labor-network/subject-and-motivation.md` → `labor-network/domain/subject-and-motivation.md`
- `labor-network/subject-control.md` → `labor-network/privacy/subject-control.md`
- `labor-network/tax-and-contribution.md` → `labor-network/economy/tax-and-contribution.md`
- `labor-network/technical-core.md` → `labor-network/architecture/technical-core.md`
- `labor-network/test-scenarios.md` → `labor-network/verification/test-scenarios.md`
- `labor-network/traceability-matrix.md` → `labor-network/migration/traceability-matrix.md`
- `labor-network/transition-and-unemployment.md` → `labor-network/support/transition-and-unemployment.md`
- `labor-network/transport-work-integration.md` → `labor-network/regional/transport-work-integration.md`
- `labor-network/trust-and-provenance.md` → `labor-network/evidence/trust-and-provenance.md`
- `labor-network/work-conditions.md` → `labor-network/domain/work-conditions.md`
- `labor-network/work-lifecycle.md` → `labor-network/state/work-lifecycle.md`
- `labor-network/MIGRATION_MANIFEST.md` → `labor-network/migration/manifest.md`

## Status

- Legacy migratable files: **66**
- Structured destinations: **66**
- Missing destinations: **0**
- Legacy deletion: **0**
- File-level coverage: **100%**

File-level coverage does not by itself certify semantic equivalence. Semantic verification is performed against the content of each source and its destination.

# Solidarity Fund Domain Model

## Purpose

This document formalizes Solidarity Fund as a domain module of the Social Labor Network. It does not replace the general architecture of the network. It binds the fund's resource-allocation process to the existing Event, Decision, Action, AuditRecord, Evidence and Provenance contracts.

## Core allocation rule

For each allocation batch, the baseline distribution of actually received voluntary funds is:

- 60% to child development;
- 35% to people in need;
- 5% to project development.

The three shares are allocation domains, not rankings of human value.

## Domain entities

### Contribution

Records a voluntary incoming contribution.

Minimum attributes:

- contribution_id;
- received_at;
- amount;
- currency;
- contributor reference, when legally and operationally necessary;
- purpose or campaign reference, when applicable;
- evidence reference;
- status.

A contribution must not create authority over recipients.

### FundAllocation

Represents the allocation of received resources into one of the three fixed domains.

Minimum attributes:

- allocation_id;
- source contribution or batch;
- allocation domain;
- amount;
- allocation ratio;
- decision reference;
- status;
- audit reference.

The allocation ratio must correspond to the declared 60/35/5 model unless an explicitly documented constraint requires a different treatment.

### Recipient

Represents a person or organization that may receive support.

Recipient types include:

- person;
- child-development organization;
- educational organization;
- creative-development organization;
- child-support organization;
- other eligible program organization.

Recipient identity and sensitive personal data must be separated from public reporting.

### Program

Represents a concrete supported activity.

Minimum attributes:

- program_id;
- recipient;
- purpose;
- budget;
- period;
- responsible party;
- eligibility criteria;
- expected result;
- reporting requirements;
- child-safety requirements where applicable.

### AllocationDecision

Represents the decision to allocate a defined amount to a defined program or recipient.

Decision is not the same object as payment or execution.

It must include:

- decision_id;
- policy version;
- evidence references;
- reviewer or decision authority;
- decision outcome;
- rationale;
- timestamp;
- contestability or review metadata where applicable.

### AllocationAction

Represents execution of an approved allocation.

It may include:

- payment initiation;
- transfer;
- approved resource delivery;
- administrative execution.

An Action cannot substitute for the preceding Decision.

### Report

Records evidence about use and outcome of allocated resources.

It may include:

- amount used;
- reporting period;
- activities completed;
- evidence;
- results;
- unresolved obligations;
- corrective actions.

### AuditRecord

Records the audit trail of allocation decisions and execution.

AuditRecord is not a surveillance profile and must not become a universal reputation score.

## Allocation lifecycle

1. A voluntary Contribution is received.
2. The contribution is validated and recorded.
3. The applicable 60/35/5 allocation is calculated.
4. Eligible Programs and Recipients are evaluated under published criteria.
5. AllocationDecision is created.
6. Approved AllocationActions are executed.
7. Evidence and Reports are collected.
8. AuditRecord preserves the trace.
9. Provenance links the resource, decision, action and evidence.
10. Corrections or disputes follow the existing correction and review mechanisms.

## Child-development boundary

The 60% child-development domain may support organizations and programs rather than only direct individual payments.

Examples include:

- creative education;
- arts and cultural development;
- educational support;
- sports and physical development;
- social skills;
- support for children's homes and children without parental care;
- safe developmental environments.

Children must not be treated as economic assets or ranked by predicted future usefulness.

## People-in-need boundary

The 35% domain can support temporary needs and development-related recovery, including:

- essential temporary support;
- education;
- retraining;
- transition between forms of employment;
- restoration of independent work capacity;
- small development projects;
- professional mutual aid.

Support should increase capability where possible rather than create an institutional dependency.

## Project-development boundary

The 5% domain exists to preserve the ability of the project itself to operate and improve.

Eligible uses can include:

- software;
- infrastructure;
- security;
- audit;
- documentation;
- research;
- transparency mechanisms;
- maintenance;
- development of the fund itself.

This allocation is disclosed as part of the model and must itself be auditable.

## Invariants

1. A voluntary Contribution does not create control over a Recipient.
2. Allocation percentages are explicit and publicly documented.
3. Decision and Action remain separate.
4. AuditRecord remains separate from surveillance.
5. Sensitive child and recipient data are minimized.
6. Public reporting is aggregated unless disclosure is necessary and lawful.
7. Conflict-of-interest cases require independent review.
8. Funding does not automatically create reputation status.
9. A recipient cannot be denied basic rights because of non-participation in the fund.
10. The fund supplements rather than replaces basic rights and mandatory social systems.
11. Allocation correction must remain traceable.
12. Unknown evidence must not be silently converted into a negative finding.

## Transparency projection

The public read model should expose at least:

- total received;
- total allocated;
- 60% child-development allocation;
- 35% people-in-need allocation;
- 5% project-development allocation;
- number of supported programs;
- recipient categories;
- reported outcomes;
- unresolved obligations.

The public projection must not expose unnecessary personal data.

## Relation to the Law of Development

The fund is an implementation layer for voluntary solidarity. It supports conditions under which subjects can preserve or expand their ability to develop.

The allocation rule does not declare that one group of people is more valuable than another. It establishes a predetermined resource policy: most of the fund is directed toward children's development, another defined share toward people needing support now, and a small share toward preserving the infrastructure that makes continued solidarity possible.

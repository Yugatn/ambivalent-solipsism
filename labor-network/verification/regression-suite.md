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

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

# SymbiontOS Evidence Ledger

## Purpose

Evidence Ledger отделяет наблюдение от интерпретации, гипотезу от причинного вывода и субъективный опыт от объективного измерения.

## Record

- observation_id
- timestamp
- source
- raw_measurement
- preprocessing
- derived_feature
- hypothesis
- confidence
- alternative_hypotheses
- intervention
- outcome
- adverse_event
- reviewer
- evidence_status

## Provenance

Для каждого значения должна быть известна цепочка происхождения:

source → raw measurement → preprocessing → feature → interpretation

Запрещено скрывать преобразования данных.

## Causal Discipline

**Observed** означает, что изменение зарегистрировано.

**Correlated** означает статистическую связь.

**Modelled** означает наличие объяснительной модели.

**Causal Candidate** означает проверяемую причинную гипотезу.

**Clinically Validated** означает подтверждение соответствующими клиническими данными.

Эти статусы нельзя использовать как взаимозаменяемые.

## Residual

Если имеющихся данных недостаточно для вывода, результат должен оставаться в Residual/UNKNOWN.

## Audit Principle

Любой существенный вывод должен быть реконструируем из Evidence Ledger.

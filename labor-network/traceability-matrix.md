# Traceability Matrix СТСети

Матрица связывает концептуальный уровень с реализацией.

| Level | Объект |
|---|---|
| Principle | нормативный принцип |
| Invariant | свойство, которое нельзя нарушить |
| Schema | структура данных |
| Event | изменение или факт |
| Guard | условие допустимости |
| State | состояние сущности |
| Decision | результат policy evaluation |
| Action | применённое последствие |
| Audit | проверяемая запись |
| Test | проверка поведения |

## Минимальное требование

Для каждого high-impact механизма должна существовать полная трасса от Principle до Test.

## Coverage

Матрица позволяет находить:

- принцип без реализации;
- реализацию без основания;
- решение без policy;
- действие без audit;
- invariant без test;
- test без проверяемого требования.

## Principle

> Формализация считается завершённой только тогда, когда нормативное утверждение имеет проверяемое техническое следствие.


## State and Action coverage

| Requirement | State | Event | Decision | Action |
|---|---|---|---|---|
| status change | state machine | state event | policy if required | optional |
| permission change | permission state | permission event | authority policy | access effect |
| evidence correction | evidence state | evidence event | reconciliation | correction |
| dispute | dispute state | dispute event | review | resolution effect |
| high-impact consequence | target state | action event | reviewed decision | audited action |


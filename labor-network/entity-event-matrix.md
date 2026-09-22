# Матрица Entity × Event × Guard × Invariant

| Entity | Event | Основные Guard | Ключевой инвариант |
|---|---|---|---|
| Opportunity | publish | authority, completeness | возможность не становится обязательством |
| Engagement | activate | acceptance, policy | участие не расширяет полномочия автоматически |
| Evidence | verify | provenance, verification | подтверждение имеет источник |
| Evidence | revoke | authority, reason | отзыв не стирает историю |
| Decision | permit | policy, impact | существенное решение проходит guards |
| Decision | deny | policy, reason | отказ имеет основание |
| Decision | review | impact, uncertainty | неопределённость не маскируется под факт |
| Dispute | open | subject access | оспаривание не переписывает источник |
| Dispute | resolve | review, evidence | результат имеет основание |
| Support | approve | eligibility, authority | поддержка не создаёт скрытого обязательства |
| Permission | revoke | authority | отозванное полномочие не используется |
| Audit | record | integrity | существенное действие трассируемо |

## Правило матрицы

Каждый новый Event для защищённой Entity должен иметь:

1. допустимый источник;
2. guard conditions;
3. ожидаемый результат;
4. инвариант;
5. audit requirement;
6. recovery path.

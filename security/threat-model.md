# Threat Model v0.1

## Базовые угрозы

- **Canon Injection:** подмена канонического принципа локальным правилом.
- **Evidence Forgery:** искусственное или искажённое свидетельство.
- **Stale Evidence Reuse:** применение устаревшего evidence как текущего.
- **Model Leakage:** выдача модели за непосредственную реальность.
- **Authority Escalation:** получение системой полномочий сверх заявленного.
- **Subject Substitution:** замена решения субъекта решением модели.
- **Audit Suppression:** удаление или скрытие следа принятого решения.

Каждая угроза должна иметь detection rule, mitigation, residual risk и audit trace.

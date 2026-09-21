# Action Failure

Ошибка применения Action не должна автоматически означать успешное выполнение.

Система фиксирует:

- attempted;
- failed;
- partially_applied;
- recovered;
- compensated.

Частично применённое действие требует отдельного reconciliation.
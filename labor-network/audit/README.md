# Audit Layer

Audit фиксирует существенные действия и позволяет восстановить цепочку принятия и применения решения.

Audit не должен содержать больше данных, чем необходимо для проверки события.

Минимум:

- actor;
- action;
- target;
- purpose;
- timestamp;
- policy version;
- decision reference;
- integrity metadata.

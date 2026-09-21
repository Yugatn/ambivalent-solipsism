# Migration Tests

Migration tests проверяют сохранение исходного содержания.

Для каждого legacy source:

1. извлекаются смысловые блоки;
2. находится destination;
3. проверяется preservation или refinement;
4. фиксируется traceability;
5. отсутствие destination считается migration failure.
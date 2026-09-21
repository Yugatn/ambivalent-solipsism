# Audit Integrity

Audit Record должен быть защищён от незаметного изменения.

Минимальные механизмы:

- immutable event reference;
- timestamp;
- integrity metadata;
- actor attribution;
- versioned schema.

Конкретный криптографический механизм выбирается на уровне реализации.
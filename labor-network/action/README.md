# Action Layer

Action представляет применённое последствие Decision.

Decision отвечает на вопрос «что разрешено или решено».

Action отвечает на вопрос «что реально было применено».

Каждый существенный Action должен иметь:

- decision reference;
- actor;
- target;
- timestamp;
- result;
- audit reference;
- recovery или compensation path, если применимо.
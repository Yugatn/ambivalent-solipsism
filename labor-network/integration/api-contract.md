# API Contract

API должен отражать доменные операции, а не предоставлять произвольный доступ к внутреннему состоянию.

Каждая mutation operation имеет:

- actor;
- purpose;
- input schema;
- authorization;
- state transition;
- result;
- audit.
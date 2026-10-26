# Symbiont Matrix M-001a

Первый исполняемый вертикальный срез Symbiont Matrix.

## Контур

Minecraft является внешней, недоверенной средой восприятия и действия. Бот передаёт события. Runtime валидирует событие, применяет декларативные YAML-правила и записывает evidence. Runtime не является authority.

## Структура

- `bot/courier.js` — транспортный адаптер.
- `runtime/symbiontd.py` — WebSocket runtime.
- `runtime/ledger.py` — tamper-evident hash-chain ledger.
- `runtime/rules.py` — загрузчик и evaluator Law DSL.
- `rules/` — декларативные правила.
- `protocol/schemas/` — JSON Schema.
- `tests/` — verification M-001a.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

Для бота:

```bash
cd bot
npm install
```

Runtime:

```bash
cd symbiont-matrix
./run.sh
```

Бот запускается отдельно:

```bash
cd symbiont-matrix/bot
node courier.js
```

## Verification

Ledger проверяет duplicate ID, Lamport regression, payload hash, prev hash, tampering и удаление записи из середины цепочки. RuleEngine загружает все YAML documents, валидирует их JSON Schema и запрещает duplicate rule_id.

Подписи пока обозначены как `UNSIGNED`. Это намеренный статус M-001a, а не криптографическая гарантия.

## Инварианты

- событие из Minecraft не равно доказательству;
- CLAIMED, OBSERVED и DERIVED различаются;
- bot не принимает policy-решения;
- runtime не получает authority над Minecraft;
- изменение правила происходит через данные YAML, а не через изменение evaluator;
- evidence считается проверяемым по цепочке хэшей, но не является защищённым от уничтожения внешним злоумышленником;
- cryptographic signatures, consent, capabilities и federation относятся к следующим слоям.

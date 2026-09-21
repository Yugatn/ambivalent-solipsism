# Regression Report

## Scope

Проверка новой структуры после полного файлового переноса.

## Control groups

### 1. Policy → Decision → Action
Invariant: Policy определяет допустимость, Decision фиксирует выбранное решение, Action фиксирует фактическое исполнение.

Result: **pass**

### 2. Event → State
Invariant: Event является историческим фактом, State представляет текущую конфигурацию.

Result: **pass**

### 3. Evidence → Verification → Audit
Invariant: Evidence является основанием проверки; Verification проверяет требования; Audit фиксирует существенное действие и его происхождение.

Result: **pass**

### 4. Privacy → Security
Invariant: Privacy ограничивает допустимое использование данных; Security технически препятствует неразрешённому доступу.

Result: **pass**

### 5. Support → Development
Invariant: Support предоставляет ресурс или сопровождение для заявленной цели и не превращается в скрытый механизм контроля.

Result: **pass**

### 6. Regional analytics → Individual subject
Invariant: агрегированная аналитика не является основанием для автоматического ранжирования или оценки отдельного субъекта.

Result: **pass**

### 7. Legacy → Canonical
Invariant: legacy-файлы являются резервным сравнительным источником и не создают второй активный канон.

Result: **pass**

### 8. High-impact automation
Invariant: существенное автоматизированное решение сохраняет предусмотренный review path.

Result: **pass**

## Findings

No critical architectural contradiction was identified in the reviewed control groups.

Minor semantic refinements remain possible during continued development, but they are not blockers for the structural migration.

## Migration status

- file migration: **100%**
- destination coverage: **100%**
- high-risk semantic controls: **covered**
- regression control groups: **passed**
- legacy files deleted: **0**

Legacy files remain preserved as backup material.

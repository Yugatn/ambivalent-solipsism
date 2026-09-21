# PICCS Sentinel — Architecture

## 1. Назначение

PICCS Sentinel — защитный контур для систем, где безопасность включает не только наличие вредоносного файла, но и сохранение корректируемости самой системы.

Базовая модель:

Fact + Model + Residual, затем Decision, затем Action, затем новый Fact.

Sentinel наблюдает весь цикл.

## 2. Архитектурные слои

### Layer 0 — Substrate

ОС, kernel, файловая система, память, сеть и hardware telemetry.

### Layer 1 — Event Fabric

События процессов, файлов, сети, identity, capabilities, конфигурации и изменений.

### Layer 2 — Evidence / Provenance

Цепочки происхождения: source, transformation, artifact, execution, effect.

### Layer 3 — Detection

Сигнатуры, эвристики, поведенческие модели, sandboxing, anomaly detection и правила целостности.

### Layer 4 — Epistemic Classification

Каждое существенное утверждение получает статус:

- OBSERVED;
- RECONSTRUCTED;
- INFERRED;
- ASSUMED;
- UNKNOWN;
- CONFLICTING.

### Layer 5 — PICCS Decision Guard

Проверяются:

- uncertainty;
- harm;
- reversibility;
- scope;
- authority;
- alternatives;
- provenance;
- external effects;
- self-intervention;
- future option space.

### Layer 6 — Intervention

Минимально необходимое действие:

- observe;
- notify;
- restrict capability;
- isolate;
- suspend;
- rollback;
- recover.

Полное удаление объекта является одним из вариантов, а не автоматическим ответом.

### Layer 7 — Independent Challenge

Высокорисковое решение должно иметь независимый challenge.

### Layer 8 — Recovery and Learning

После действия система сравнивает ожидаемое и наблюдаемое состояние и определяет:

- model error;
- measurement error;
- execution error;
- environment shift;
- interaction effect.

## 3. Detection, Decision и Action

Это основной архитектурный барьер.

Detection говорит: «обнаружен сигнал».

Decision говорит: «есть достаточное основание для определённого режима».

Action физически меняет систему.

Один модуль не должен автоматически превращать слабый сигнал в максимально сильное действие.

## 4. Threat classes

### T1. Known Malware
Известный вредоносный объект.

### T2. Unknown Malware
Новый или модифицированный вредоносный объект.

### T3. Behavioral Abuse
Легитимный инструмент используется опасным способом.

### T4. Privilege Escalation
Происходит расширение полномочий.

### T5. Persistence
Угроза пытается пережить перезапуск или очистку.

### T6. Supply Chain
Компрометация пакета, обновления, зависимости или разработческого канала.

### T7. Data Poisoning
Изменение данных так, чтобы последующая модель принимала ошибочную реконструкцию.

### T8. Epistemic Attack
Атака на способность системы различать факт, гипотезу и неизвестное.

### T9. Feedback Attack
Манипуляция каналом обратной связи.

### T10. Authority Attack
Попытка заставить систему выполнить действие, не соответствующее полномочиям.

### T11. Self-Validation Attack
Создание ситуации, в которой результат собственного вмешательства используется как доказательство правильности исходной гипотезы.

### T12. Recovery Attack
Атака на механизмы остановки, отката и восстановления.

## 5. Decision Matrix

Не используется единый score угрозы.

Вместо него хранится профиль:

ThreatProfile = Evidence, Uncertainty, Harm, Irreversibility, Authority, Provenance, Scope, Feedback, Residual.

Это предотвращает превращение одного рейтинга в скрытый управляющий механизм.

## 6. Safe Response Ladder

При сопоставимой эффективности применяется минимально достаточный уровень:

1. наблюдение;
2. уведомление;
3. дополнительная проверка;
4. ограничение capability;
5. изоляция;
6. приостановка;
7. откат;
8. восстановление.

Сильное действие требует отдельного основания.

## 7. Quarantine

Quarantine должна быть:

- ограниченной по времени;
- ограниченной по области;
- трассируемой;
- отменяемой;
- проверяемой;
- защищённой от превращения временной меры в постоянную норму.

## 8. Safe Degradation

При отказе Sentinel:

- не увеличивает собственные полномочия;
- не удаляет объекты без отдельного основания;
- сохраняет жизненно важные функции;
- ограничивает необратимые действия;
- переходит к безопасному режиму;
- передаёт критические решения независимому контуру, если это возможно.

## 9. Anti-Capture

Sentinel проверяет собственную устойчивость к захвату:

- независимость источников;
- provenance;
- разнообразие моделей;
- доступность альтернатив;
- сохранение несогласующихся свидетельств;
- возможность независимого challenge.

## 10. AI Security

AI-контур защищается от:

- prompt injection;
- malicious tool instructions;
- hidden authority escalation;
- context leakage;
- untrusted retrieved content;
- unsafe autonomous plans;
- tool-chain manipulation.

Ключевое правило:

Tool access не равен Tool authority.

## 11. Human Sovereignty

Sentinel не должен:

- объявлять человека угрозой только по поведенческой корреляции;
- определять моральную ценность субъекта;
- заменять человека собственной моделью;
- использовать один риск-балл как основание для лишения прав;
- превращать защитный контур в систему тотального наблюдения.

## 12. Audit Record

Каждое существенное вмешательство хранит:

DecisionRecord = time, subject, evidence, model, residual, authority, action, reversibility, reviewer, outcome, version.

## 13. TLA+ candidate invariants

SNT-01 No Finality — Sentinel не объявляет собственную модель окончательной истиной.

SNT-02 Detection Separation — Detection не создаёт автоматически Action authority.

SNT-03 Authority Bound — Action не выходит за пределы capability.

SNT-04 Provenance — существенное решение имеет проверяемое происхождение данных.

SNT-05 Residual Preservation — UNKNOWN и CONFLICTING не преобразуются автоматически в разрешение или угрозу.

SNT-06 Reversible Preference — при сопоставимой эффективности предпочтение получает более обратимый ответ.

SNT-07 Safe Degradation — потеря критического контроля не увеличивает автономию Sentinel.

SNT-08 Self-Validation Prohibition — результат собственного вмешательства не считается независимым подтверждением исходной гипотезы.

SNT-09 Stop Availability — критический контур имеет путь остановки.

SNT-10 Auditability — существенное вмешательство реконструируемо по журналу.

SNT-11 Capability Is Not Permission — техническая возможность не создаёт автоматически разрешения.

SNT-12 Human Exit — при применении к человеку должна существовать процедура пересмотра и выхода, где это практически возможно.

## 14. Минимальный прототип

Phase A:

- process telemetry;
- file integrity;
- package provenance;
- capability inventory;
- append-only event log.

Phase B:

- behavioral detection;
- quarantine;
- rollback;
- independent challenge;
- threat provenance graph.

Phase C:

- epistemic guard;
- AI tool guard;
- model/data poisoning detection;
- self-intervention analysis.

Phase D:

- formal verification;
- adversarial testing;
- reproducible benchmarks;
- external security review.

## 15. Критерии качества

Sentinel оценивается не только по detection rate.

Профиль испытаний включает:

- true positive rate;
- false positive rate;
- mean time to detect;
- mean time to contain;
- recovery time;
- rollback success;
- provenance completeness;
- unsafe intervention rate;
- unjustified quarantine rate;
- independent challenge success;
- safe degradation success;
- model drift detection;
- resistance to epistemic capture.

## 16. Главный тест

Хороший антивирус должен уметь сказать:

> «Я обнаружил сигнал, но ещё не знаю достаточно, чтобы разрушать объект».

И одновременно:

> «Я не уверен в классификации, поэтому ограничиваю потенциальный ущерб обратимым способом».

Это и есть применение PICCS к кибербезопасности.

## 17. Граница проекта

PICCS Sentinel не является доказательством того, что философская концепция AS истинна.

Это инженерная гипотеза:

> принципы ограниченной ответственности, сохранения Residual, разделения полномочий и самопрерывания могут повысить устойчивость защитной системы к неизвестным и адаптивным угрозам.

Эта гипотеза должна проверяться экспериментально.

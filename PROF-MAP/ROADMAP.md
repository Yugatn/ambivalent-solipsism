# PROF-MAP — Development Roadmap

## v0.2.1 — Foundation

- методологическая спецификация;
- 13 шкал;
- разделение слоёв;
- архитектура данных;
- интеграционный слой.

## v0.3 — Item Bank

- 130 первичных пунктов;
- экспертная проверка;
- маркировка reverse/SJT/control;
- резервные пункты.

## v0.4 — Pilot

- пилотная выборка;
- item analysis;
- анализ пропусков;
- распределения ответов;
- проверка времени прохождения;
- проверка понятности формулировок.

## v0.5 — GitHub Pages MVP

- questions.json;
- scales.json;
- professions.json;
- skills.json;
- scoring.js;
- matching.js;
- адаптивный интерфейс;
- localStorage;
- экспорт результата.

## v0.6 — Existing Tools Integration

- Wheel of Balance;
- Cattell module;
- unified profile shell;
- переход между инструментами.

## v1.0 — Research-oriented release

- ESCO mapping;
- Skill Gap;
- прозрачный Match;
- PDF report;
- versioned methodology;
- consent/privacy layer.

## v2.0 — Adaptive System

- адаптивное тестирование;
- личный кабинет;
- история изменений;
- учебные маршруты;
- практические задания;
- портфолио;
- vacancy integration.

## Research loop

Каждая версия item bank должна иметь идентификатор. Нельзя менять смысл вопроса без изменения версии.

```
item bank
  -> pilot
  -> analysis
  -> revision
  -> version
  -> next pilot
```

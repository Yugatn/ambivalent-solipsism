# Реестр проектов, описаний и лицензирования — 15.11.2026

**Назначение:** единый контроль портфеля GitHub-проектов Югатна. Реестр не изменяет литературный канон, условия уже действующих лицензий или права на сторонние материалы.

**Исключено из текущей операции:** `wheel-balance`, `psy-tools`, `psy-tools-symbiont-node` — проекты «Колеса баланса».

## Репозитории с существующей лицензией MIT (без замены условий)

| Репозиторий | Назначение |
|---|---|
| [MyPro](https://github.com/Yugatn/MyPro) | Evidence Core, видеоконтент и протокол координации агентов |
| [music-studio](https://github.com/Yugatn/music-studio) | Музыкальная станция macOS с MIDI и ИИ-агентами |
| [yugatneoworld](https://github.com/Yugatn/yugatneoworld) | Пространственная социальная среда eWorld |
| [eugene-work](https://github.com/Yugatn/eugene-work) | Локальный рабочий кабинет документов и календаря |
| [YUGATNEO_GAME](https://github.com/Yugatn/YUGATNEO_GAME) | Шахматы в браузере |
| [-YUGATNEO_Roblax](https://github.com/Yugatn/-YUGATNEO_Roblax) | Экспериментальные миры Roblox |
| [Yugatneo_BOT](https://github.com/Yugatn/Yugatneo_BOT) | Мультиплатформенный ИИ-помощник для рефлексии |
| [YUGATNEO_SKILLS](https://github.com/Yugatn/YUGATNEO_SKILLS) | SwiftUI-приложение физических навыков |

## Репозитории, для которых добавлено уведомление All rights reserved

| Репозиторий | Назначение |
|---|---|
| [ambivalent-solipsism](https://github.com/Yugatn/ambivalent-solipsism) | Авторская философская система и исследовательские материалы |
| [Yugatn-symbiont-grok-node](https://github.com/Yugatn/Yugatn-symbiont-grok-node) | Экспериментальный независимый узел Grok |
| [yugatn-adaptive-self-mapping](https://github.com/Yugatn/yugatn-adaptive-self-mapping) | Адаптивное самокартирование и методология |
| [story-x](https://github.com/Yugatn/story-x) | Авторский роман и рабочие материалы |
| [yugatneo_minecraft](https://github.com/Yugatn/yugatneo_minecraft) | Оригинальный voxel-прототип по мотивам романа |
| [solidarnost](https://github.com/Yugatn/solidarnost) | Движок распределения добровольной помощи |
| [yugatn_art](https://github.com/Yugatn/yugatn_art) | Веб-мастерская цифрового искусства |
| [Yugatn_Box](https://github.com/Yugatn/Yugatn_Box) | Исследовательский проект универсальной игровой системы |
| [YUGATNeoTIME](https://github.com/Yugatn/YUGATNeoTIME) | Календарный и исторический атлас времени |
| [cinemacatharis](https://github.com/Yugatn/cinemacatharis) | Методология кинематографа и восприятия |
| [CryptoSimbiont_Traiding](https://github.com/Yugatn/CryptoSimbiont_Traiding) | Исследование торговых стратегий и рисков |
| [RouterSymbiont-Universal](https://github.com/Yugatn/RouterSymbiont-Universal) | Инструмент диагностики сети без изменения настроек |
| [YUGATNEO_Art](https://github.com/Yugatn/YUGATNEO_Art) | Проект творческой инициативы и конкурса |
| [Zokon_Razvitiya](https://github.com/Yugatn/Zokon_Razvitiya) | Концептуальный проект Закона развития |

**Важно:** уведомление All rights reserved — не свободная лицензия и не разрешение на модификацию или коммерческое использование. Это консервативный правовой статус до самостоятельного выбора автором условий распространения. Отдельные компоненты могут иметь собственные условия.

## Выполненные изменения

- Обновлены описания и правовые ссылки в корневых `README.md` всех 22 репозиториев.
- В 14 репозиториях с отсутствовавшим `LICENSE` добавлено уведомление об авторских правах.
- В 18 репозиториях с исполняемым кодом добавлены `.github/scripts/check_repository_basics.py` и `.github/workflows/repository-health.yml` для проверки присутствия README, LICENSE, заголовка, краткого описания и опасных имён отслеживаемых Git файлов.
- В MyPro усилена неизменяемость снимков в EventEnvelope; в eWorld исправлена совместимость social/city API и тестовые пути TypeScript-артефактов.

## Ограничения проверки

Проверка метаданных не удостоверяет корректность всей программной логики, безопасность продакшена или правовой статус сторонних компонентов. Наличие workflow не означает успешное выполнение других CI-job.

GitHub About description, topics, website и прочие настройки репозитория являются **отдельными полями GitHub**. Текущие изменения касаются файлов README/LICENSE и автоматических проверок; поля About данным действием не менялись.

## Следующие задачи

1. Отдельно провести лицензионный аудит сторонних зависимостей и медиа.
2. Согласовать возможный переход некоторых программных проектов с All rights reserved на MIT или иную свободную лицензию, сохранив права на художественные тексты и символику.
3. Проверить macOS-сборки music-studio и iOS-сборки YUGATNEO_SKILLS.
4. Разобрать шумные результаты AS Lint, не редактируя авторский текст автоматически.

# Синема Катарсис — Content Passport 3.0

## 1. Назначение

Content Passport 3.0 объединяет в одной публичной карточке:

1. метаданные произведения;
2. сведения о создателях;
3. сюжетный и культурный контекст;
4. технические характеристики;
5. карту контента Cinema Catharsis;
6. provenance, uncertainty и версии анализа.

Ключевой принцип:

**Метаданные и измерения публикуются вместе, но не смешиваются семантически.**

Связь между ними:

content_id + content_hash

---

## 2. Шесть блоков карточки

### 1. Идентификация

- id;
- content_hash;
- title_original;
- title_ru;
- title_alt[];
- year;
- release_date;
- duration_min;
- language_original;
- languages[];
- country_original;
- countries[];
- type.

Типы:

- feature_film;
- short_film;
- series;
- mini_series;
- tv_movie;
- documentary;
- animation;
- experimental;
- advertising;
- music_video;
- stream.

### 2. Визуальный блок

- poster;
- backdrop;
- logo;
- stills;
- poster_hash;
- dominant colors;
- aspect ratio.

Размеры изображений являются представлениями UI, а не отдельными культурными объектами. Лицензионные права должны храниться отдельно от URL.

### 3. Создатели

Единая модель участника:

{
  "person_id": "wikidata:Q...",
  "name": "Имя Фамилия",
  "name_original": "Name Surname",
  "role": "director",
  "role_detail": null,
  "order": 1
}

Роли:

director, writer, producer, exec_producer, composer, cinematographer, editor, production_designer, costume_designer, voice_actor, narrator, actor, stunt.

Для актёров:

{
  "person_id": "wikidata:Q...",
  "name": "Актёр",
  "role": "actor",
  "character": "Персонаж",
  "billing": 1,
  "screen_time_sec": null,
  "screen_time_confidence": null
}

screen_time_sec является вычисляемой оценкой Cinema Catharsis и не считается исходным метаданным источника.

### 4. Сюжет и контекст

- synopsis_short;
- synopsis_full;
- tagline;
- genres[];
- themes[];
- keywords[];
- franchise;
- based_on;
- awards[];
- age_rating_official.

Жанры являются версионируемым controlled vocabulary.

### 5. Технические данные

- color_type;
- sound_type;
- aspect_ratio;
- frame_rate;
- resolution;
- versions[];
- distributor;
- budget_usd;
- box_office_usd;
- streaming[].

Каждое поле может иметь собственный source и confidence.

### 6. Карта контента

- composition;
- time share;
- shot coverage;
- density;
- recurrence;
- temporal map;
- context vector;
- co-occurrence network;
- exposure profile;
- uncertainty;
- validation summary;
- ontology/model/measurement versions.

---

## 3. Provenance метаданных

Для каждого поля:

{
  "value": "...",
  "source": "wikidata|tmdb|manual|derived",
  "source_id": "...",
  "retrieved_at": "...",
  "source_version": null,
  "confidence": null,
  "conflict_status": "none|conflict|needs_review",
  "human_verified": false
}

Не существует одного универсального «источника истины» для всех полей.

Политика разрешения конфликта определяется отдельно для каждого поля.

Если источники существенно расходятся:

needs_review = true

Система не должна молча выбирать значение.

---

## 4. Источники

Рекомендуемая архитектура источников:

### Wikidata

Основной источник структурированных идентификаторов и связанных сущностей, где соответствующее утверждение существует и имеет достаточную provenance.

Wikidata предоставляет структурированные данные и несколько стабильных способов доступа.

### TMDB

Источник для movie/TV metadata, credits и визуальных ресурсов при соблюдении условий лицензии и attribution.

TMDB API предоставляет отдельные методы для credits и images.

### IMDb

Используется только для тех полей и наборов данных, которые доступны в соответствующем официальном формате/лицензии проекта.

Не следует предполагать, что IMDb Datasets являются универсальным API для всех отображаемых на IMDb пользовательских данных.

### Локальные/региональные источники

Используются для локализованных названий, возрастных классификаций и региональных сведений при наличии легального и технически доступного интерфейса.

### Ручной ввод

Используется для редких, отсутствующих или спорных данных и всегда помечается как manual.

---

## 5. Стратегия слияния

Для каждого поля задаётся:

- preferred_sources[];
- fallback_sources[];
- conflict_rule;
- validation_rule;
- freshness_policy.

Общий принцип:

SOURCE VALUE → NORMALIZATION → CROSS-SOURCE COMPARISON → CONFIDENCE → RESOLUTION → AUDIT LOG

Если конфликт не разрешён:

UNKNOWN / NEEDS_REVIEW

а не произвольный выбор.

---

## 6. Вычисляемые данные

Часть данных создаётся самой системой.

| Поле | Метод |
|---|---|
| screen_time_sec | face detection + tracking + identity/cluster assignment |
| character_screen_time | character tracking / identity assignment |
| dominant_colors | frame/poster analysis |
| shot_duration | shot boundary detection |
| scene_duration | scene segmentation |
| location clusters | visual embeddings + clustering |
| content metrics | validated contentometry pipeline |

Все производные поля имеют:

- model_version;
- method_version;
- confidence;
- uncertainty;
- validation status.

---

## 7. Экранное время

Пайплайн:

FACE DETECTION
→ TRACKING
→ EMBEDDING / IDENTIFICATION
→ CLUSTERING
→ CAST ASSIGNMENT
→ AGGREGATION

Публикуются:

- суммарное время;
- метод;
- модель;
- версия;
- confidence;
- validation metrics;
- uncertainty;
- ограничения.

Особые случаи:

- маски;
- грим;
- частично закрытое лицо;
- близнецы/похожие лица;
- каскадёры;
- дублёры;
- CGI;
- анимация;
- групповые сцены.

При недостаточной валидации:

screen_time_sec = unknown

а не псевдоточное число.

---

## 8. Карта контента

Пример:

| Program | Time share | Shot coverage | Density | Recurrence |
|---|---:|---:|---:|---:|
| family | 42.1% | 38.2% | 0.18/min | 12 |
| science | 18.4% | 21.7% | 0.07/min | 8 |
| conflict | 9.8% | 11.2% | 0.05/min | 7 |

Эти показатели не являются рейтингом.

Программы могут пересекаться, поэтому значения не обязаны суммироваться до 100%.

---

## 9. Интерфейс

### Desktop

Карточка:

POSTER | TITLE / YEAR / DURATION / TYPE
       | GENRES / COUNTRIES / LANGUAGE
       | DIRECTOR / WRITERS / PRODUCERS
       | CAST
       | SYNOPSIS

Затем:

CONTENT MAP
TEMPORAL MAP
NETWORK
UNCERTAINTY
METHODOLOGY

### Mobile

Используются раскрывающиеся блоки:

- Identification;
- Creators;
- Cast;
- Synopsis;
- Technical;
- Content Map;
- Methodology.

### Catalog card

Минимально:

- poster;
- title;
- year;
- duration;
- director;
- compact content map.

Карточка каталога не должна скрывать методологический статус показанных чисел.

---

## 10. API

Предлагаемая структура:

GET /v1/content/{id}
GET /v1/content/{id}/metadata
GET /v1/content/{id}/credits
GET /v1/content/{id}/cast
GET /v1/content/{id}/poster
GET /v1/content/{id}/card
GET /v1/content/{id}/map
GET /v1/content/{id}/timeline
GET /v1/content/{id}/network
GET /v1/content/{id}/report

API должен возвращать не только значения, но и provenance/uncertainty/version для производных измерений.

---

## 11. Data model

Базовые сущности:

content
content_metadata
persons
content_credits
studios
content_studios
franchises
awards
content_awards
metadata_provenance
content_analysis
content_events
content_exposure
analysis_versions

Принцип:

metadata tables ≠ measurement tables

Связь:

content_id + content_hash

---

## 12. Минимальная SQL-модель

CREATE TABLE content_metadata (
    content_id BIGINT PRIMARY KEY REFERENCES content(id),
    title_original TEXT NOT NULL,
    title_ru TEXT,
    title_alt TEXT[],
    year INT,
    release_date DATE,
    duration_min FLOAT,
    language_original TEXT,
    languages TEXT[],
    country_original TEXT,
    countries TEXT[],
    type TEXT,
    tagline TEXT,
    synopsis_short TEXT,
    synopsis_full TEXT,
    genres TEXT[],
    themes TEXT[],
    keywords TEXT[],
    franchise TEXT,
    based_on JSONB,
    awards JSONB,
    age_rating_official JSONB,
    poster_url TEXT,
    poster_hash TEXT,
    backdrop_url TEXT,
    logo_url TEXT,
    still_urls TEXT[],
    color_dominant TEXT[],
    aspect_ratio TEXT,
    color_type TEXT,
    sound_type TEXT,
    frame_rate FLOAT,
    resolution TEXT,
    versions TEXT[],
    distributor TEXT,
    budget_usd BIGINT,
    box_office_usd BIGINT,
    streaming TEXT[],
    last_synced TIMESTAMPTZ
);

CREATE TABLE persons (
    id BIGSERIAL PRIMARY KEY,
    wikidata_id TEXT UNIQUE,
    name TEXT NOT NULL,
    name_original TEXT,
    photo_url TEXT,
    birth_year INT,
    death_year INT,
    country TEXT,
    bio_short TEXT
);

CREATE TABLE content_credits (
    content_id BIGINT REFERENCES content(id),
    person_id BIGINT REFERENCES persons(id),
    role TEXT NOT NULL,
    role_detail TEXT,
    character TEXT,
    billing INT,
    screen_time_sec FLOAT,
    screen_time_confidence FLOAT,
    PRIMARY KEY (content_id, person_id, role)
);

CREATE TABLE metadata_provenance (
    content_id BIGINT,
    field TEXT,
    source TEXT,
    source_id TEXT,
    retrieved_at TIMESTAMPTZ,
    source_version TEXT,
    confidence FLOAT,
    conflict_status TEXT,
    human_verified BOOLEAN DEFAULT FALSE
);

---

## 13. Индексы

Рекомендуемые индексы:

- year;
- genres;
- keywords;
- countries;
- franchise;
- persons.name;
- content_credits.role;
- content_credits.person_id;
- metadata_provenance.content_id.

Для PostgreSQL массивы и JSONB индексируются только там, где это оправдано реальными запросами.

---

## 14. Регулярная синхронизация

Метаданные динамичны.

Pipeline:

1. получить изменения;
2. нормализовать;
3. сравнить с текущим значением;
4. применить field-specific conflict policy;
5. записать audit/provenance;
6. выставить needs_review при конфликте;
7. обновить materialized card.

Частота синхронизации определяется не абстрактным правилом «раз в неделю», а SLA конкретного источника и важностью поля.

---

## 15. Audit log

Минимальная структура:

CREATE TABLE metadata_audit (
    id BIGSERIAL PRIMARY KEY,
    content_id BIGINT,
    field TEXT,
    old_value TEXT,
    new_value TEXT,
    source TEXT,
    changed_at TIMESTAMPTZ DEFAULT NOW()
);

Audit log позволяет восстановить происхождение изменения.

---

## 16. Публичные форматы

- HTML;
- JSON;
- PDF;
- PNG;
- Markdown;
- JSON-LD.

JSON-LD может использовать Schema.org Movie/CreativeWork там, где это соответствует фактическим данным.

Публичная карточка должна отделять:

- фактические метаданные;
- производные измерения;
- пользовательские материалы;
- внешние рейтинги.

---

## 17. Встраиваемый виджет

Концептуальный интерфейс:

<iframe src="https://cinema-catharsis.org/embed/{content_id}"
        width="400" height="600"></iframe>

Виджет показывает:

- постер;
- идентификацию;
- основные метаданные;
- компактную карту контента;
- ссылку на полную методологию.

Реальный production URL и схема embed будут определены после запуска публичного домена.

---

## 18. JSON-структура

{
  "id": 12345,
  "content_hash": "sha256:...",
  "metadata": {
    "title_original": "Interstellar",
    "title_ru": "Интерстеллар",
    "year": 2014,
    "duration_min": 169,
    "language_original": "en",
    "countries": ["US", "GB"],
    "type": "feature_film",
    "genres": ["sci-fi", "drama", "adventure"]
  },
  "credits": {
    "director": [
      {"person_id": "Q...", "name": "Christopher Nolan"}
    ]
  },
  "cast": [
    {
      "person_id": "Q...",
      "name": "Actor",
      "character": "Character",
      "billing": 1,
      "screen_time_sec": null,
      "screen_time_confidence": null
    }
  ],
  "content_map": {
    "composition": {},
    "shot_coverage": {},
    "density": {},
    "timeline": [],
    "network": {},
    "uncertainty": {},
    "versions": {
      "ontology": "2.3.1",
      "model": "CCV-5.1",
      "measurement": "CM-1.4"
    }
  }
}

Пример является структурой API, а не утверждением фактических значений конкретного фильма.

---

## 19. Schema.org

Для SEO может использоваться JSON-LD с Movie/CreativeWork.

Но:

- aggregateRating публикуется только при наличии соответствующего источника;
- Cinema Catharsis measurement values не должны подменять пользовательские рейтинги;
- производные показатели должны иметь собственное описание;
- JSON-LD не должен создавать ложное впечатление официальной сертификации.

---

## 20. Публичный датасет

Открытая научная часть может включать:

- content_id;
- content_hash;
- ontology_version;
- event timestamps;
- MPE labels;
- context annotations;
- uncertainty;
- validation metadata;
- derived aggregate metrics.

Для изображений, видео, аудио, лиц и других защищённых материалов лицензии проверяются отдельно.

Открытость проекта не означает автоматическое право распространять исходные медиафайлы.

---

## 21. Методологическая прозрачность

Каждая карточка должна позволять ответить:

- какая версия произведения анализировалась;
- какая онтология использовалась;
- какая модель применялась;
- какие параметры использовались;
- какая часть данных автоматическая;
- какая часть проверена человеком;
- какая неопределённость;
- какие ограничения известны.

Формула публичности:

CONTENT + METHOD + UNCERTAINTY + VERSION + LIMITATIONS

---

## 22. Принцип свободы интерпретации

Content Passport не говорит пользователю, что произведение «хорошее», «плохое», «вредное» или «полезное».

Он показывает:

- что это за произведение;
- кто его создал;
- что в нём наблюдается;
- как часто это наблюдается;
- в каком контексте;
- насколько уверенно это измерено;
- какие выводы подтверждены отдельно.

Интерпретация остаётся за пользователем.

---

## 23. Формулы

Паспорт:

Passport = Metadata ∪ Measurement

Карта:

Content Map = Observation + Measurement + Context + Uncertainty

Полный исследовательский стек:

Cinema Catharsis =
Metadata
+ Contentometry
+ Exposure
+ Validation
+ Response Studies
+ Provenance

---

## 24. Связь с Scientific Contentometry Protocol

Content Passport 3.0 является пользовательским представлением результатов.

Научные границы задаются:

[Scientific Contentometry Protocol v0.2](methodology/CONTENTOMETRY_PROTOCOL.md)

Особенно важно:

CONTENT ≠ EXPOSURE ≠ RESPONSE ≠ EFFECT ≠ HARM

Паспорт не должен превращать наблюдаемую контентометрию в утверждение о вреде.

---

## 25. Статус

**Content Passport 3.0 — specification draft**

Следующий этап:

1. JSON Schema;
2. OpenAPI specification;
3. PostgreSQL migration;
4. metadata adapters;
5. provenance service;
6. passport composer;
7. HTML/mobile UI;
8. validation corpus;
9. public dataset policy.

---

## 26. Главный принцип

> Сначала паспорт объекта.
>
> Затем карта содержания.
>
> Затем, если есть отдельное исследование, карта реакции.
>
> Не смешивать уровни знания.
> Не скрывать неопределённость.
> Не решать за Субъекта.


---

## 27. Implementation lock — 2026-09-19

Эта спецификация является базовым публичным контрактом Content Passport 3.0.

Следующий технический слой не должен менять смысл существующих полей молча. Изменения схемы оформляются через:

1. schema_version;
2. migration note;
3. backward-compatibility status;
4. validation update;
5. changelog.

### Separation invariant

```
METADATA ≠ CONTENT OBSERVATION ≠ EXPOSURE ≠ SUBJECT RESPONSE
```

Производные показатели всегда сопровождаются provenance, uncertainty и версией метода.

### MVP implementation order

```
JSON Schema
→ sample passport
→ validator
→ metadata adapter
→ annotation schema
→ passport composer
→ HTML renderer
```

Цель MVP — получить воспроизводимую карточку даже до автоматического анализа полного видеоматериала.


---

## 27. v0.3.0 Methodological Integrity Addendum

### 27.1 Структура паспорта

```text
Passport = ⟨Metadata, Measurement, Provenance, Uncertainty, Versions⟩
```

Обозначение `Metadata ∪ Measurement` не используется как формальное определение паспорта.

### 27.2 Статусы и coverage

Для MPE/программы: `present | absent | unknown | ambiguous | not_applicable`.

Правило: `absent ⇒ coverage.temporal ≥ C_min`. Недостаточное покрытие означает `unknown`/`preliminary`, а не доказанное отсутствие.

### 27.3 Quality ≠ coverage

`quality` описывает detection/classification; `coverage` — полноту охвата. Они публикуются отдельно.

### 27.4 Context

Наблюдаемый контекст хранится в `context_observed`; интерпретации — в `context_interpreted.interpretations[]`. Несколько интерпретаций допустимы.

### 27.5 Screen-time share ≠ viewer exposure

`screen_time_share = Tω/T` описывает произведение и не является `viewer_exposure`.

### 27.6 Manifestation ≠ Scene

Manifestation — конкретный экземпляр ontology class. Scene — монтажно-нарративная единица. Они не являются отношением один-к-одному.

### 27.7 Evidence and question type

`literature` — provenance/source type. Для научного утверждения дополнительно фиксируются `question_type`, `design`, `population`, `comparator`, `outcome`, `effect`, `uncertainty`, `limitations`, `adequacy_for_question`.

### 27.8 Validation

Krippendorff's α и κ измеряют agreement/reliability и не являются универсальной мерой validity. Validation summary разделяет reliability, validity, coverage, calibration и drift.

### 27.9 Correction Protocol

```yaml
correction:
  id: correction-0001
  target: content_id / claim_id
  field: "..."
  old_value: "..."
  new_value: "..."
  reason: "..."
  created_at: "..."
  status: corrected | superseded | rejected
```

Старый результат не удаляется молча.

**Status:** Content Passport 3.0 — v0.3.0 methodological specification.

# Validation Protocol v0.1

Цель: проверить воспроизводимость применения онтологии независимыми разметчиками.

## Pilot corpus
Целевой дизайн: 200 фрагментов по 3–5 минут. Стратификация: жанры, 5 временных периодов, регионы, narrative/documentary/animation. Это проектный target, а не утверждение, что корпус уже собран.

## Annotators
- 3 независимых разметчика;
- обучение на 20 эталонных фрагментах;
- qualification target: Krippendorff's alpha >= 0.70;
- production annotation независимо.

## Unit
Основная единица — EVENT. Shot используется как техническая монтажная граница.

## Agreement
Primary: Krippendorff's alpha. Рабочие зоны проекта:
- alpha >= 0.67: acceptable for pilot review;
- 0.40 <= alpha < 0.67: revise codebook;
- alpha < 0.40: redesign operationalization.

Это governance thresholds проекта, а не универсальные научные законы.

## Disagreement
independent annotations -> comparison -> disagreement log -> senior adjudication -> codebook amendment if needed. Adjudicated labels хранятся отдельно от raw annotations.

## QC
Публикуются alpha, per-class agreement, confusion analysis, prevalence, sample composition, inclusion/exclusion rules, adjudication rate и known failure modes.

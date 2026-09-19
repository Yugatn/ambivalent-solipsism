# Uncertainty Model v0.1

Для каждой метрики публикуется структурированный результат:

`M = <point, model_error, annotation_error, sampling_error, CI95, status>`

## Components
- point — точечная оценка;
- model_error — uncertainty validated model;
- annotation_error — uncertainty from annotation agreement;
- sampling_error — uncertainty from sampling design;
- CI95 — интервал соответствующей статистической оценки.

Компоненты не складываются автоматически. Распространение ошибки определяется estimator и covariance structure.

## Status
- validated
- preliminary
- unreliable
- unknown

Если validation evidence недостаточна — preliminary. Если annotation agreement ниже project reject threshold — unreliable. Если обоснованная оценка отсутствует — unknown.

Confidence и uncertainty — разные поля. Confidence не является probability of correctness без calibration.

Example:
```json
{"program":"alc","time_share":{"point":0.089,"ci_95":[0.074,0.104],"model_error":null,"annotation_error":null,"sampling_error":null,"status":"preliminary"}}
```

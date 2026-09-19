# Синема Катарсис — Scientific Contentometry Protocol v0.1

**Статус:** research methodology / pre-registration-ready draft  
**Project:** Cinema Catharsis  
**Repository:** Yugatn/ambivalent-solipsism  
**Principle:** measurement before interpretation

---

## 1. Purpose

Cinema Catharsis is a measurement framework for describing media stimuli and, in separate experiments, studying their relationship with measurable responses of a human subject.

The system has three distinct domains:

1. **Contentometry** — what is presented.
2. **Psychophysiology** — what changes during or after exposure.
3. **Causal inference** — whether an exposure can reasonably be considered a cause of a measured change under a specified experimental design.

These domains must not be collapsed into a single score.

> **CONTENT ≠ EXPOSURE ≠ RESPONSE ≠ EFFECT ≠ HARM**

The project does not assign moral value to media and does not infer harm merely from the presence of a stimulus.

---

## 2. Epistemic model

The project uses the following chain:

MEDIA → STIMULUS → EXPOSURE → RESPONSE → EFFECT → HARM

Each arrow represents an additional empirical claim.

### 2.1 Content

A content claim describes an observable feature of the media object.

Example:

PERSON + BOTTLE + DRINKING

This does not establish audience reaction, persuasion, normalization, health effect, or long-term harm.

### 2.2 Exposure

Exposure describes how the stimulus is presented:

- duration;
- repetition;
- temporal concentration;
- modality;
- salience;
- contextual embedding;
- sequence position.

### 2.3 Response

Response is an observed change in a predefined physiological, subjective, cognitive, or behavioural measure relative to a baseline or control condition.

### 2.4 Effect

Effect means a reproducible difference attributable to an exposure under an appropriate design.

### 2.5 Harm

Harm is a separate construct requiring its own operational definition and evidence. A transient physiological response is not, by itself, evidence of harm.

---

## 3. Scientific hypotheses

The initial research programme contains falsifiable hypotheses.

### H1 — Measurement

Defined media features can be annotated with reproducible agreement above a prespecified minimum.

### H2 — Response

Some predefined media stimulus configurations can produce measurable changes in specified response variables relative to an appropriate control condition.

### H3 — Exposure-response relationship

For some stimulus classes, response probability or magnitude may vary as a function of exposure parameters.

### H4 — Individual variability

Response functions vary between subjects and should therefore be estimated with hierarchical or mixed-effects models rather than assumed to be universal.

### H5 — Context modulation

Contextual combinations can modify the relationship between a stimulus and a measured response.

### H6 — Threshold heterogeneity

Operational response thresholds, where identifiable, vary by stimulus, subject, state, history, measurement modality, and experimental context.

None of these hypotheses is treated as established by the existence of this protocol.

---

## 4. What is a threshold?

The word **threshold** is overloaded and must be specified.

Cinema Catharsis distinguishes at least five concepts:

1. **Detection threshold** — minimum stimulus level at which a subject can detect a stimulus.
2. **Discrimination threshold** — minimum difference needed to distinguish two stimuli.
3. **Response threshold** — operational point at which a predefined response measure departs from a prespecified baseline/control criterion.
4. **Behavioural threshold** — point associated with a predefined behavioural change.
5. **Clinical or functional threshold** — point at which a change reaches a separately justified clinical or functional significance criterion.

These thresholds are not interchangeable.

A response threshold must never be presented as a universal human constant.

### 4.1 Operational threshold model

For a continuous exposure variable x, estimate a response function:

P(R | x, S, H, C)

where:

- R = predefined response;
- x = exposure parameter;
- S = current subject state;
- H = relevant history;
- C = experimental context.

A threshold may be defined as a parameter of a prespecified model, for example the exposure level corresponding to a specified probability of response or a specified departure from baseline.

The threshold must be reported with uncertainty.

If the data do not identify a threshold reliably:

> **Threshold not identified.**

That is a valid scientific result.

---

## 5. Content ontology

The core ontology is layered.

### L0 — Observation

Directly observable primitives:

- object;
- person;
- action;
- sound;
- speech;
- text;
- face;
- gesture;
- colour;
- location.

### L1 — Event

A structured combination of observations.

Example:

PERSON + BOTTLE + DRINKING

### L2 — Media Program Element

An event mapped to a controlled ontology.

Example:

consumption.alcohol

### L3 — Relations and context

Relations include:

- actor;
- object;
- location;
- before/after;
- consequence;
- recurrence;
- social reaction;
- verbal context;
- narrative role.

**SHOT ≠ EVENT.** One event can span several shots.

---

## 6. Exposure profile

Exposure is represented as a vector rather than a single arbitrary intensity score.

Xω(t) = [duration, repetition, salience, modality, temporal_concentration, context]

The first implementation should preserve the raw components.

A composite exposure index may only be introduced after empirical validation of its components and weighting scheme.

### 6.1 Required exposure variables

For each annotated stimulus:

- start time;
- end time;
- duration;
- number of occurrences;
- distance between occurrences;
- simultaneous modalities;
- visual prominence;
- auditory prominence;
- narrative position;
- contextual embedding.

Where a variable cannot be reliably measured:

unknown

must be used instead of an invented value.

---

## 7. Response profile

Psychophysiological experiments must define primary outcomes before data collection.

Possible measures include:

- electrodermal activity (EDA);
- heart rate;
- heart-rate variability;
- respiration;
- temperature;
- facial or skeletal EMG;
- eye movements;
- pupil diameter;
- EEG;
- fMRI in appropriately equipped laboratory studies;
- self-report;
- behavioural measures.

No single signal should be treated as a universal measure of "arousal".

### 7.1 Baseline

Each participant should have a predefined baseline period or control condition.

A basic change score is:

ΔY(t) = Ystimulus(t) − Ybaseline(t)

Possible summary measures include:

- peak response;
- latency;
- area under the response curve;
- recovery time;
- mean change over a prespecified interval.

The primary outcome must be prespecified.

---

## 8. Experimental design

A basic within-subject protocol can be:

BASELINE → STIMULUS/CONTROL → RESPONSE → RECOVERY

For stronger causal inference:

1. define the exposure before data collection;
2. use a control condition appropriate to the research question;
3. randomize or counterbalance stimulus order where applicable;
4. preregister primary outcomes and analysis;
5. define exclusion criteria in advance;
6. record deviations from protocol;
7. blind analysts to condition when feasible;
8. estimate sample size or justify the chosen design;
9. report uncertainty and effect sizes;
10. correct or otherwise control for multiplicity when multiple inferential tests are performed.

Randomized studies should be reported according to current applicable reporting guidance, such as CONSORT 2025, with relevant extensions where appropriate.

---

## 9. Threshold estimation

Threshold research should use a graded exposure design rather than a binary "weak/strong" classification whenever scientifically appropriate.

Candidate approaches:

- psychometric curves;
- logistic or probit models;
- generalized additive models;
- mixed-effects models;
- hierarchical Bayesian models.

The choice must be justified by the response variable and experimental design.

### 9.1 Recommended reporting

For every estimated threshold:

- threshold definition;
- model;
- estimator;
- confidence or credible interval;
- stimulus class;
- exposure units;
- participant population;
- exclusion rules;
- model diagnostics;
- sensitivity analysis.

A threshold estimated in one population must not automatically be generalized to another population.

---

## 10. Individual variability

The project assumes heterogeneity rather than a universal subject.

Candidate model:

Yij = β0 + β1Xij + ui + εij

where:

- i = subject;
- j = observation;
- ui = subject-specific random effect;
- εij = residual variation.

Additional covariates may include prior exposure, attention, current state, or other prespecified factors.

Individual-level results should not be converted into population claims without appropriate aggregation and uncertainty estimates.

---

## 11. Potentially destructive social programmes

Cinema Catharsis may contain ontology elements describing behaviours or interaction patterns that are independently associated with risks to health, development, autonomy, or safety.

The system must separate:

OBSERVATION → PROGRAM → EXTERNAL EVIDENCE

from:

OBSERVATION → MORAL VERDICT

A programme is not labelled harmful solely because it appears in a film.

Each risk-related annotation should include:

- programme identifier;
- evidence source;
- evidence type;
- population studied;
- outcome studied;
- evidence strength;
- uncertainty;
- date of evidence review.

This prevents a content label from silently becoming a causal or moral conclusion.

---

## 12. Context vector

Context should be represented on independent axes rather than compressed into a single "romanticization" label.

Possible axes:

- consequence shown;
- consequence absent;
- actor role;
- social approval/disapproval;
- camera emphasis;
- verbal framing;
- music;
- humour;
- repetition;
- narrative reward/punishment;
- causal position in the story.

Each annotation may carry:

- value;
- confidence;
- evidence source;
- annotator/model version.

---

## 13. Statistical separation of errors

At minimum, distinguish:

### Measurement/model error

Error introduced by automated detection or measurement.

Report, where applicable:

- precision;
- recall;
- F1;
- calibration;
- sensitivity/specificity.

### Annotation error

Disagreement between human annotators.

Possible statistics:

- Cohen's κ for two raters;
- Fleiss' κ for multiple raters;
- Krippendorff's α for more general annotation structures.

### Sampling uncertainty

Uncertainty arising from the sample and estimator.

Report:

- confidence intervals;
- credible intervals where Bayesian methods are used;
- effect sizes;
- model assumptions.

Do not combine unrelated error sources into a single number unless a justified error-propagation model is specified.

---

## 14. Validation corpus

A reference corpus should contain:

- diverse genres;
- different production eras;
- different countries and cultures;
- animation;
- documentary/news;
- advertising;
- experimental media;
- multilingual material.

The corpus must have a documented sampling strategy.

### 14.1 Gold standard

A gold-standard subset should be independently annotated by trained human annotators under a written codebook.

The project should publish:

- annotation protocol;
- disagreement procedure;
- agreement statistics;
- adjudication rules;
- known blind spots.

The gold standard itself is a measurement instrument and must therefore be versioned.

---

## 15. Cultural and linguistic validity

The ontology should be hierarchical:

- Level 1 — broadly portable concept;
- Level 2 — regional or cultural subtype;
- Level 3 — local/specialized subtype.

For multilingual material:

original speech → transcription → linguistic analysis → optional translation

The original-language evidence should be retained whenever legally and ethically possible.

Translation must not silently replace the source signal.

---

## 16. Reproducibility contract

Every analysis should record:

- content hash;
- exact media version;
- ontology version;
- annotation schema version;
- vision model version;
- audio model version;
- NLP model version;
- preprocessing configuration;
- measurement parameters;
- statistical model;
- random seed where relevant;
- software/environment version;
- analysis hash.

A reproducibility record should make it possible to distinguish:

- deterministic reproducibility;
- statistical reproducibility;
- replication with independent data.

### Analysis hash

Conceptually:

H = SHA256(content_hash || ontology_version || model_versions || parameters || code_version)

The exact serialization format must be specified before production use.

---

## 17. Content Passport

The output for a media object should contain at least four separate blocks.

### A. Content Passport

What appears in the work.

### B. Exposure Profile

How often, how long, and in what configuration it appears.

### C. Response Profile

Only when a human experiment has actually been performed.

### D. Evidence and uncertainty

Validation, confidence intervals, model limitations, and external evidence.

This prevents an observational content report from being mistaken for a human-effects study.

---

## 18. Ethics

Human-response studies require appropriate ethical review for the jurisdiction and institution conducting the study.

The protocol should include, as applicable:

- informed consent;
- right to withdraw;
- participant risk assessment;
- debriefing;
- predefined stopping criteria;
- data minimization;
- secure handling of physiological and behavioural data;
- protection of potentially sensitive participant information.

High-risk stimuli should not be introduced experimentally merely to test a speculative hypothesis when a safer design can answer the question.

---

## 19. Prohibited inference rules

The following transformations are invalid without additional evidence:

presence → harm

frequency → harm

physiological response → pathology

emotion → belief

correlation → causation

single-study threshold → universal threshold

population average → individual prediction

content label → moral judgement

model confidence → scientific accuracy

These are methodological guardrails.

---

## 20. Research levels

The project should report evidence by level.

### Level A — Observational contentometry

What is present?

No human exposure experiment is required.

### Level B — Exposure characterization

How is it presented over time?

Requires validated temporal annotation.

### Level C — Controlled response experiment

What measurable response follows exposure under controlled conditions?

Requires human-subject methodology and ethical oversight.

### Level D — Causal experiment

Does changing the exposure cause a change in the predefined outcome?

Requires an appropriate causal design.

### Level E — Longitudinal outcome research

Are repeated exposures associated with or causally related to longer-term outcomes?

Requires a separate longitudinal research programme.

No result from Level A should be presented as if it were a Level E finding.

---

## 21. Minimal data schema

~~~json
{
  "content_id": "string",
  "content_hash": "sha256",
  "media_type": "film|series|documentary|advertising|animation|other",
  "ontology_version": "string",
  "annotation_version": "string",
  "events": [
    {
      "event_id": "string",
      "start_s": 0.0,
      "end_s": 0.0,
      "program": "string",
      "context": {},
      "confidence": 0.0,
      "source": "human|model|hybrid"
    }
  ],
  "exposure": {
    "duration_s": 0.0,
    "occurrences": 0,
    "modalities": [],
    "temporal_concentration": null,
    "salience": null
  },
  "response": {
    "study_id": null,
    "participant_id": null,
    "measure": null,
    "baseline": null,
    "change": null,
    "uncertainty": null
  },
  "evidence": [],
  "limitations": []
}
~~~

This schema is a research draft, not a clinical data standard.

---

## 22. Decision rule for the system

The system should prefer:

MEASURED

over

INFERRED

and:

UNKNOWN

over

UNJUSTIFIED CERTAINTY.

A missing value is not permission to guess.

---

## 23. Relationship to Ambivalent Solipsism

Within Ambivalent Solipsism:

WORLD → MEDIA → PERCEPTION → SUBJECT STATE

Cinema Catharsis investigates the media segment of this chain.

Its scientific boundary is:

> **The system describes the information entering the perceptual field; it does not decide what that information means to the Subject.**

The philosophical principle remains:

> **Do not decide for the Subject. Give the Subject a map.**

---

## 24. Falsifiability and failure conditions

The project must allow itself to fail.

The methodology should be revised if:

- trained annotators cannot achieve reproducible agreement for a proposed category;
- automated detection does not generalize beyond the development corpus;
- exposure indices fail to predict or characterize relevant stimulus variation;
- supposed thresholds are unstable across reasonable analytical specifications;
- physiological measures do not reliably distinguish the proposed experimental conditions;
- effects disappear under preregistered replication;
- cultural or linguistic transfer produces systematic measurement bias.

A failed hypothesis is a scientific result, not a defect to be hidden.

---

## 25. Current implementation roadmap

### Phase 1 — Formal ontology

- ontology specification;
- event schema;
- context schema;
- versioning.

### Phase 2 — Annotation

- codebook;
- annotation interface;
- gold-standard corpus;
- inter-rater validation.

### Phase 3 — Reference contentometer

- shot/event segmentation;
- multimodal detection;
- uncertainty propagation;
- Content Passport generation.

### Phase 4 — Exposure engine

- temporal exposure representation;
- repetition analysis;
- multimodal salience;
- validated exposure indices.

### Phase 5 — Psychophysiological research

- preregistered protocol;
- ethics review;
- baseline/control;
- response measurement;
- threshold modelling.

### Phase 6 — Causal and longitudinal research

- controlled exposure studies;
- mediation/moderation;
- longitudinal designs;
- replication.

---

## 26. References and methodological anchors

The protocol is informed by established methodological traditions rather than treating Cinema Catharsis itself as established science.

- CONSORT 2025 — reporting of randomized trials.
  https://www.equator-network.org/reporting-guidelines/consort/
- CONSORT-PRO — patient-reported outcomes in randomized trials.
  https://www.equator-network.org/reporting-guidelines/consort-pro/
- CONSORT Harms — reporting harms in randomized trials.
  https://www.equator-network.org/reporting-guidelines/consort-harms/
- CONSORT-SPI — social and psychological intervention trials.
  https://www.equator-network.org/reporting-guidelines/consort-spi/

Additional psychophysics, psychophysiology, causal-inference, preregistration, and measurement references should be added as the specific experimental modules are developed.

---

## 27. Status

**Cinema Catharsis — Scientific Contentometry Protocol v0.1**

This document defines the methodological boundary between:

content → exposure → response → effect → harm

The next implementation target is not a universal "harm score".

It is a reproducible measurement system whose outputs can be independently checked.

> **Не запрет. Не рекомендация. Не рейтинг.
> Сначала наблюдение. Затем измерение. Затем проверка.**

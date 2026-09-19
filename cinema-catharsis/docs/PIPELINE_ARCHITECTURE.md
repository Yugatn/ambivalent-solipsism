# Cinema Catharsis — Pipeline Architecture v0.5

## Principle

The public interface may accept a source reference, but the analysis layer must keep **ingestion**, **segmentation**, **multimodal observation**, **measurement**, and **interpretation** separate.

```
SOURCE → ORCHESTRATOR → INGESTION → SEGMENTATION → L0/L1/L2/L3 → MEASUREMENT → PASSPORT
```

## Source layer

Supported interface targets:

- direct user-uploaded video file;
- a permitted/public video URL;
- YouTube metadata/reference.

A torrent/magnet workflow is **not enabled by the public demo**. It requires a separate legal, licensing and infrastructure review. The project must not assume that “fair use” or a research purpose automatically authorizes acquisition or redistribution of copyrighted material.

## Orchestrator

Planned backend responsibilities:

1. parse source type;
2. create deterministic analysis request;
3. compute/cache source hashes where lawful and technically possible;
4. enqueue a background job;
5. expose progress;
6. persist provenance and versions;
7. return Content Map.

The static GitHub Pages demo currently performs local JSON analysis only. It does not claim to download or analyze remote media.

## Ingestion

Planned components:

- FFmpeg for normalization;
- source-specific adapters;
- SHA-256 provenance hashes;
- temporary working storage with explicit retention policy.

Normalization parameters must be versioned rather than silently assumed.

## Segmentation

Candidate components:

- PySceneDetect;
- TransNetV2;
- keyframe extraction.

Segmentation output:

```yaml
shot_id:
start_ms:
end_ms:
keyframe:
```

Segmentation is an observation layer, not a semantic conclusion.

## Multimodal observation

Candidate modules:

- vision: object/person/action detectors;
- audio: speech, acoustic-event and speaker models;
- NLP: transcription, entity and linguistic classifiers.

Outputs enter L0/L1/L2/L3 only when their operational definitions and validation procedures are documented.

No automatic L3 → interpretation transition is permitted.

## Measurement Engine

For category ω:

- `Nω` — event count;
- `Tω` — union of event intervals;
- `Sω = Tω/T` — screen-time share;
- `Cω` — declared coverage;
- `event_density = Nω/(T/60)`;
- `covered_time_density = Tω/(T/60)`;
- `Rω` — repeatability according to the current measurement specification.

Overlapping intervals within one category are merged before `Tω` is calculated.

## Status engine

`C_min = 0.95` is currently a project assumption.

- observation exists → `present`;
- no observation + coverage ≥ C_min → `absent`;
- no observation + coverage < C_min → `unknown`;
- unresolved classification → `ambiguous`.

## Results

The public result layer consists of:

- Content Map JSON;
- Content Passport;
- Content Wheel;
- vertical metric chart;
- event Timeline;
- machine-readable provenance/version metadata.

## Explicit non-goals

The pipeline does not infer viewer exposure, psychological effect, harm, recommendation, censorship, or causality from content measurements alone.

`screen_time_share ≠ viewer_exposure`.

## Implementation stages

### Current: Demo v0.3

Local JSON → validation → measurement → visualization → export.

### Next: Demo v0.4

Interactive event editor and Content Map authoring.

### Backend prototype

FastAPI API contract, job queue and progress reporting.

### Multimodal prototype

Controlled test corpus, segmentation and model outputs with human validation.

Remote-source ingestion should be added only after the provenance, legal, retention and reproducibility rules are specified.
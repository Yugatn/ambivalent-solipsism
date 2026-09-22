# Cattell visual-scene extension concept

Status: DEFERRED / DESIGN NOTE

## Idea

Future version of the Cattell 16PF-style research instrument may add controlled visual scenes to selected questions. The respondent would answer after observing a standardized scene rather than only reading an abstract verbal statement.

The visual stimulus should function as an additional elicitation layer, not as a claim that images reveal hidden personality automatically.

## Why this can be useful

A scene can provide context, ambiguity and social/environmental cues that a short verbal statement does not provide. This may make some items more concrete and can create a projective-style research layer.

The correct formulation is: visual stimulus; spontaneous response; structured answer; comparison with verbal response; contextual interpretation.

Do NOT describe this as a validated projective test until empirical validation exists.

## Proposed architecture

1. Baseline verbal 16PF-style item.
2. Optional visual-scene variant.
3. Same construct or factor target.
4. Response captured separately as VERBAL_RESPONSE and SCENE_RESPONSE.
5. Compare convergence/divergence.
6. Preserve uncertainty and context.
7. Never infer a hidden trait from the image alone.

## Visual design constraints

Because image-generation capacity is limited, scenes should initially be prepared as a small reusable library rather than generated for every item.

Priority: simple readable compositions; neutral facial expressions; no unnecessary text inside images; culturally non-specific environments where possible; consistent framing and visual language; mobile-first dimensions; alt text and a text-only equivalent; avoid emotionally manipulative imagery unless the research question explicitly requires it.

## Research safeguards

The scene must not secretly encode the expected answer through obvious visual cues.

Possible experimental conditions:

- verbal only;
- scene only;
- verbal + scene;
- repeated scene with altered context.

Potential measurements:

- response choice;
- response latency where technically reliable;
- confidence;
- verbal explanation;
- consistency between modalities.

## AS / PSY-TOOLS principle

The visual scene is a stimulus and the resulting score is a model.

STIMULUS != PERSON
RESPONSE != PERSON
MODEL != PERSON
UNKNOWN != ABSENT

The future feature should be presented as exploratory research and self-observation unless independent psychometric validation establishes stronger claims.

## Deferred implementation

Do not spend scarce Grok/image operations on this until:

1. the current Cattell page is verified;
2. the visual-scene item schema is designed;
3. a small pilot set of scenes is defined;
4. the image-generation budget is available;
5. a comparison protocol is specified.

This note exists so the concept can be resumed without reconstructing the discussion.

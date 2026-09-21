# TLA+ models

AntiReplay_Protocol.tla uses an acceptance counter rather than a set-only invariant. A set cannot detect duplicate acceptance because duplicate elements collapse by definition.

FavoriteReplication.tla models deterministic operation ordering. It is a specification seed, not a model-checked claim.

No claim is promoted to model_checked merely because a .tla file exists.

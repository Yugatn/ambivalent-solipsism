# Detection Status — Cinema Catharsis Demo v0.3

## C_min

`C_min = 0.95` is a **project assumption**, not an empirically validated threshold.

- `coverage >= C_min`: absence may be reported as `absent`.
- `coverage < C_min`: a zero observation must be reported as `unknown`, not `absent`.

This threshold must later undergo sensitivity analysis and empirical validation.

## Statuses

- `present`: at least one valid observed event for the category.
- `absent`: no observed event and sufficient coverage.
- `unknown`: no observed event, but coverage is insufficient to support absence.
- `ambiguous`: observation exists but classification remains ambiguous.
- `not_applicable`: category is outside the analysis scope.

## Epistemic rule

Absence of observation is not equivalent to observation of absence. `absent` is conditional on coverage.
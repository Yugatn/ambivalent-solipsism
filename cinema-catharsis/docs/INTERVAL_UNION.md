# Interval Union — Cinema Catharsis Demo v0.3

For category omega, `Tω` is the measure of the **union** of valid event intervals, not the sum of raw event durations.

If E1 = [120, 180] and E2 = [160, 220], then `Tω = |[120,220]| = 100 s`, rather than `60 + 60 = 120 s`.

This prevents double-counting screen time when events of the same category overlap.

Events from different categories may overlap independently. Therefore category-level `screen_time_share` values are not required to sum to 100%.

## Two density measures

`event_density = Nω / (T/60)` measures event frequency.

`covered_time_density = Tω / (T/60)` measures category-covered seconds per minute of work. It is not a perceptual exposure measure.
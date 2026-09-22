// PROF-MAP 2.0 — transparent MVP matching
export function profileFit(profile, model) {
  let numerator = 0, denominator = 0;
  for (const [scale, spec] of Object.entries(model.profile || {})) {
    if (profile[scale] == null) continue;
    const weight = Number(spec.weight || 1);
    numerator += weight * Math.abs(Number(profile[scale]) - Number(spec.target));
    denominator += weight;
  }
  if (!denominator) return null;
  return Math.max(0, 1 - numerator / (4 * denominator));
}

export function matchIndex({profileFitValue, environmentFit=1, valuesFit=1, skillsFit=1, penalty=0}) {
  const raw =
    0.45 * profileFitValue +
    0.20 * environmentFit +
    0.15 * valuesFit +
    0.20 * skillsFit -
    penalty;
  return Math.max(0, Math.min(100, raw * 100));
}

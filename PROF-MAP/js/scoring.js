// PROF-MAP 2.0 — transparent prototype scoring
export function reverseLikert(value) { return 6 - Number(value); }

export function scoreScale(items, responses) {
  const usable = items.filter(i => responses[i.id] !== undefined);
  if (!usable.length) return null;
  const values = usable.map(i => {
    const raw = Number(responses[i.id]);
    return i.reverse ? reverseLikert(raw) : raw;
  });
  return values.reduce((a,b) => a+b, 0) / values.length;
}

export function scoreProfile(questions, responses) {
  const groups = {};
  for (const item of questions) {
    if (!groups[item.scale]) groups[item.scale] = [];
    groups[item.scale].push(item);
  }
  return Object.fromEntries(
    Object.entries(groups)
      .map(([scale, items]) => [scale, scoreScale(items, responses)])
      .filter(([, value]) => value !== null)
  );
}

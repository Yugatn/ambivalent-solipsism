#!/usr/bin/env python3
"""Проверка целостности текста книги «Амбивалентный Солипсизм».

Скрипт не изменяет файлы. Он обнаруживает типографические артефакты,
следы инструментов, стрелочные обозначения и потенциально необъяснённые
сокращения. Решение о редактуре принимает человек.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "BOOK"

ARTIFACTS = [
    ("citation-token", re.compile(r"(?:cite|url|entity|image_group|video|navlist)[^]*")),
    ("tool-reference", re.compile(r"turn\d+(?:search|news|view|fetch|image)\d+")),
    ("replacement-character", re.compile(r"�")),
    ("mojibake", re.compile(r"(?:Ã.|Â.)")),
]

ARROWS = re.compile(r"[→←⇒⇐↔⇄⟶⟵]|->|=>")

# Технические и общепринятые обозначения, которые допустимы при наличии
# расшифровки в словаре или первом употреблении.
KNOWN = {
    "АС", "ИИ", "ЦНС", "ПИККС", "PICCS", "AI", "CNS", "AS",
    "Gf", "Gc", "16PF", "GDP", "ORES", "ACN", "ST",
    "EthicalAudit", "YUGATN", "Residual", "BreakAS",
    "OBSERVED", "DERIVED", "CLAIMED", "NOT_TESTED", "CONFLICTED",
}

# Потенциальные латинские аббревиатуры в обычном тексте.
LATIN_ABBR = re.compile(r"(?<![A-Za-z])[A-Z]{2,8}(?![A-Za-z])")
CYRILLIC_ABBR = re.compile(r"(?<![А-ЯЁ])[А-ЯЁ]{2,8}(?![А-ЯЁ])")

issues = []
files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".html", ".txt"})

for path in files:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        issues.append((str(path.relative_to(ROOT)), "read-error", str(exc)))
        continue

    rel = str(path.relative_to(ROOT))

    for label, pattern in ARTIFACTS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            issues.append((rel, label, f"line {line}"))

    for match in ARROWS.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        issues.append((rel, "arrow-notation", f"line {line}: {match.group()}"))

    for pattern, label in ((LATIN_ABBR, "latin-abbreviation"), (CYRILLIC_ABBR, "cyrillic-abbreviation")):
        for match in pattern.finditer(text):
            token = match.group()
            if token not in KNOWN:
                line = text.count("\n", 0, match.start()) + 1
                # Не считаем одиночные заголовки Markdown и распространённые
                # статусные метки автоматически ошибкой.
                issues.append((rel, label, f"line {line}: {token}"))

print(f"BOOK-TEXT-AUDIT: {len(files)} files, {len(issues)} findings")
for rel, label, detail in issues:
    print(f"{label}\t{rel}\t{detail}")

raise SystemExit(1 if any(x[1] in {"citation-token", "tool-reference", "replacement-character", "mojibake", "arrow-notation"} for x in issues) else 0)

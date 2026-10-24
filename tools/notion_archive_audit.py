#!/usr/bin/env python3
"""Read-only GitHub -> Notion archive audit for Ambivalent Solipsism.

Never edits Notion. Produces a deterministic manifest to review before any import.
"""
import csv
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, unquote
from urllib.request import Request, urlopen

OWNER = "Yugatn"
REPO = "ambivalent-solipsism"
ROOT = os.getenv("NOTION_PARENT_PAGE_ID", "403d1323-8599-818c-8df9-c8e3b6330393")
TOKEN = os.getenv("NOTION_TOKEN", "")
API = "https://api.notion.com/v1"
SOURCE = re.compile(
    r"https?://(?:www\\.)?github\\.com/Yugatn/ambivalent-solipsism/blob/[^/\\s]+/([^\\s)>\\]]+)",
    re.I,
)


def request(path):
    for attempt in range(7):
        try:
            url = API + path
            with urlopen(Request(url, headers={
                "Authorization": "Bearer " + TOKEN,
                "Notion-Version": "2022-06-28",
                "Accept": "application/json",
            }), timeout=60) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code == 429 and attempt < 6:
                time.sleep(float(exc.headers.get("Retry-After", "3")) + 0.5)
                continue
            if exc.code == 404:
                raise RuntimeError(
                    "Notion returned 404: connect the integration to the Ambivalent Solipsism "
                    "archive page and verify NOTION_PARENT_PAGE_ID."
                ) from None
            if exc.code in (401, 403):
                raise RuntimeError(
                    "Notion authorization failed (HTTP %d). Check NOTION_TOKEN and "
                    "integration Read content permission." % exc.code
                ) from None
            raise


def blocks(parent):
    cursor = None
    while True:
        suffix = "?page_size=100"
        if cursor:
            suffix += "&start_cursor=" + quote(cursor)
        data = request("/blocks/" + parent + "/children" + suffix)
        yield from data["results"]
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]
        time.sleep(0.34)


def source_from_blocks(page_id, known):
    candidates = set()
    lines = []
    for block in blocks(page_id):
        obj = block.get(block.get("type"), {})
        text = "".join(x.get("plain_text", "") for x in obj.get("rich_text", []))
        lines.append(text)
        for rich in obj.get("rich_text", []):
            if rich.get("href"):
                lines.append(rich["href"])
        if block.get("type") == "bookmark":
            lines.append(obj.get("url", ""))
    # Source labels prevent references to related chapters from being interpreted
    # as the archived document's identity.
    for i, line in enumerate(lines):
        if re.search(r"(?:Source path|Исходный файл|Источник|GitHub source)\s*:", line, re.I):
            segment = " ".join(lines[i:i+3])
            candidates.update(unquote(p.rstrip(".,;")) for p in SOURCE.findall(segment))
            candidates.update(p for p in known if p in segment)
    return sorted(p for p in candidates if p in known)


def tracked_files():
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    return sorted(p.decode("utf-8") for p in raw.split(b"\0")
                  if p and p.decode("utf-8").lower().endswith(".md"))


def make_report(paths, mapping, unclear, outdir):
    rows = []
    for path in paths:
        ids = sorted(set(mapping[path]))
        sha = subprocess.check_output(
            ["git", "hash-object", "--", path], text=True
        ).strip()
        status = ("missing_or_unmapped" if not ids else
                  "duplicate_review" if len(ids) > 1 else "mapped_unverified")
        rows.append({
            "path": path, "git_blob_sha": sha, "status": status,
            "notion_pages": len(ids),
            "notion_urls": " | ".join(
                "https://www.notion.so/" + pid.replace("-", "") for pid in ids
            ),
        })
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "report.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "github_markdown_files": len(paths),
        "mapped_unverified": sum(r["status"] == "mapped_unverified" for r in rows),
        "missing_or_unmapped": sum(r["status"] == "missing_or_unmapped" for r in rows),
        "duplicate_review": sum(r["status"] == "duplicate_review" for r in rows),
        "ambiguous_notion_pages": unclear,
        "mode": "read_only_audit",
        "warning": "Mapped does not mean byte-identical. No files were imported.",
    }
    (outdir / "report.json").write_text(
        json.dumps({"summary": summary, "files": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    text = ["# Ambivalent Solipsism: GitHub → Notion audit", ""]
    text += [f"- {key}: {value}" for key, value in summary.items() if key != "ambiguous_notion_pages"]
    text += ["", "Unresolved Notion pages: " + str(len(unclear)), "",
             "Read-only. Treat missing/unmapped paths as candidates for manual review."]
    (outdir / "summary.md").write_text("\n".join(text) + "\n", encoding="utf-8")
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("\n".join(text) + "\n")
    print("\n".join(text))
    return summary


def main():
    if not TOKEN:
        sys.exit("NOTION_TOKEN secret is missing in this repository.")
    paths = tracked_files()
    mapping = defaultdict(list)
    unclear = []
    pages = [b for b in blocks(ROOT) if b.get("type") == "child_page"]
    for index, block in enumerate(pages, 1):
        title = block.get("child_page", {}).get("title", "")
        if not title.startswith("Архив оригинала"):
            continue
        try:
            sources = source_from_blocks(block["id"], set(paths))
            if len(sources) == 1:
                mapping[sources[0]].append(block["id"])
            else:
                unclear.append({"page_id": block["id"], "title": title, "sources": sources})
        except Exception as exc:
            unclear.append({"page_id": block["id"], "title": title, "error": str(exc)})
        if index % 50 == 0:
            print("Scanned Notion pages:", index, "/", len(pages), flush=True)
        time.sleep(0.35)
    make_report(paths, mapping, unclear, Path("notion-audit-output"))


if __name__ == "__main__":
    main()

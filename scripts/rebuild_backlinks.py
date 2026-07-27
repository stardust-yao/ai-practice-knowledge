#!/usr/bin/env python3
"""Rebuild the backlinks index from Concept entry files.

Scans every `knowledge/entries/*.md` file for Markdown links inside the
"关联概念" (Related Concepts) section, inverts the mapping so each target
knows which entries point to it, and writes the result to
`knowledge/.backlinks.json`.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root
ENTRIES_DIR = ROOT / "knowledge" / "entries"
OUTPUT = ROOT / "knowledge" / ".backlinks.json"


def extract_backlinks(md_path: Path) -> list[tuple[str, str]]:
    """Return (source_stem, target_stem) pairs for one entry file."""
    text = md_path.read_text(encoding="utf-8")
    source = md_path.stem

    # Locate the "关联概念" section
    m = re.search(r"^##\s*关联概念\s*$", text, re.MULTILINE)
    if not m:
        return []

    # Grab everything from that heading to the next heading (or EOF)
    section_start = m.end()
    rest = text[section_start:]
    m_next = re.search(r"^##\s+", rest, re.MULTILINE)
    section_body = rest[: m_next.start()] if m_next else rest

    # Extract Markdown links [label](target.md)
    links = re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", section_body)
    return [(source, target.replace(".md", "")) for _, target in links]


def main() -> None:
    backlinks: dict[str, list[str]] = {}

    for md_file in sorted(ENTRIES_DIR.glob("*.md")):
        for source, target in extract_backlinks(md_file):
            backlinks.setdefault(target, []).append(source)

    OUTPUT.write_text(
        json.dumps(backlinks, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"✅ {len(backlinks)} concepts have backlinks → {OUTPUT}")


if __name__ == "__main__":
    main()

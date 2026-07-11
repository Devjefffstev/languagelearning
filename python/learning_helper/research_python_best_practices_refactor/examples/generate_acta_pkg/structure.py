"""Walk a Google Doc body and turn it into a structured list of "blocks".

A block is either:
    {"kind": "paragraph", "index": int, "start": int, "end": int, "text": str}
or
    {"kind": "table", "index": int, "start": int, "end": int,
     "rows": [[{cell dict}, ...], ...]}

Where a cell dict is:
    {"start": int, "end": int, "text": str, "paragraphs": [{start, end, text}, ...]}

This module is *pure*: it doesn't import anything from Google APIs and it
doesn't print. Pass it a `documents().get(...).execute()` result, get back
a list of blocks. That's why it's trivially testable.
"""
from __future__ import annotations

import re
from typing import Any

# Matches the {{TAG}} placeholders the structural injector places.
TAG_PATTERN = re.compile(r"\{\{[A-Z_0-9]+\}\}")


def cell_text(cell: dict[str, Any]) -> str:
    """Concatenate all textRun contents of a cell into one string."""
    parts: list[str] = []
    for c in cell.get("content", []):
        if "paragraph" in c:
            parts.append(
                "".join(
                    r["textRun"].get("content", "")
                    for r in c["paragraph"].get("elements", [])
                    if "textRun" in r
                )
            )
    return "".join(parts)


def cell_paragraph_ranges(cell: dict[str, Any]) -> list[dict[str, Any]]:
    """Yield `(start, end, text)` for each paragraph inside a cell.

    Cell boundaries themselves are immutable, but paragraph boundaries
    inside cells are valid delete/insert ranges.
    """
    return [
        {
            "start": c["startIndex"],
            "end": c["endIndex"],
            "text": "".join(
                r["textRun"].get("content", "")
                for r in c["paragraph"].get("elements", [])
                if "textRun" in r
            ),
        }
        for c in cell.get("content", [])
        if "paragraph" in c
    ]


def collect_structure(doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Walk the document body once. Return per-block structural info.

    See module docstring for the shape of each block.
    """
    blocks: list[dict[str, Any]] = []
    for elem in doc["body"]["content"]:
        if "paragraph" in elem:
            start, end = elem["startIndex"], elem["endIndex"]
            text = "".join(
                r["textRun"].get("content", "")
                for r in elem["paragraph"].get("elements", [])
                if "textRun" in r
            )
            blocks.append({
                "kind": "paragraph",
                "index": start,
                "start": start,
                "end": end,
                "text": text,
            })
        elif "table" in elem:
            rows = []
            for row in elem["table"].get("tableRows", []):
                cells = []
                for cell in row.get("tableCells", []):
                    paragraphs = cell_paragraph_ranges(cell)
                    cells.append({
                        "start": cell["startIndex"],
                        "end": cell["endIndex"],
                        "text": cell_text(cell),
                        "paragraphs": paragraphs,
                    })
                rows.append(cells)
            blocks.append({
                "kind": "table",
                "index": elem["startIndex"],
                "start": elem["startIndex"],
                "end": elem["endIndex"],
                "rows": rows,
            })
    return blocks


def find_table(blocks: list[dict], table_index: int) -> dict:
    """Return the Nth table block. Raise IndexError if out of range."""
    tables = [b for b in blocks if b["kind"] == "table"]
    if table_index >= len(tables):
        raise IndexError(
            f"table_index {table_index} out of range (only {len(tables)} tables)"
        )
    return tables[table_index]


def find_paragraph(blocks: list[dict], predicate) -> dict | None:
    """Return the first paragraph block matching `predicate(block)`, or None."""
    for b in blocks:
        if b["kind"] == "paragraph" and predicate(b):
            return b
    return None


def extract_doc_text(doc: dict[str, Any]) -> str:
    """Concatenate every paragraph + every cell text in the doc into one string.

    Used by `verify-tags` to scan for {{TAG}}s in the doc.
    """
    chunks: list[str] = []
    for elem in doc["body"]["content"]:
        if "paragraph" in elem:
            chunks.append(
                "".join(
                    r["textRun"].get("content", "")
                    for r in elem["paragraph"].get("elements", [])
                    if "textRun" in r
                )
            )
        elif "table" in elem:
            for row in elem["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    chunks.append(cell_text(cell))
    return "".join(chunks)


def find_tag_positions(doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Walk the doc and return one dict per {{TAG}} occurrence: `{tag, start, end}`.

    Paragraph boundaries are valid, so we track `startIndex` from each
    paragraph element and add the run-relative offset to find each tag.
    """
    positions: list[dict[str, Any]] = []

    def walk_paragraph(para_elem: dict[str, Any]) -> None:
        for run in para_elem.get("elements", []):
            if "textRun" not in run:
                continue
            text = run["textRun"].get("content", "")
            run_start = run.get("startIndex", 0)
            for m in TAG_PATTERN.finditer(text):
                positions.append({
                    "tag": m.group(0),
                    "start": run_start + m.start(),
                    "end": run_start + m.end(),
                })

    for elem in doc["body"]["content"]:
        if "paragraph" in elem:
            walk_paragraph(elem["paragraph"])
        elif "table" in elem:
            for row in elem["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    for c in cell.get("content", []):
                        if "paragraph" in c:
                            walk_paragraph(c["paragraph"])
    return positions


def parse_replacements(cell_text_value: str) -> list[str]:
    """Return the list of `{{TAG}}` strings found in `cell_text_value`."""
    return TAG_PATTERN.findall(cell_text_value or "")
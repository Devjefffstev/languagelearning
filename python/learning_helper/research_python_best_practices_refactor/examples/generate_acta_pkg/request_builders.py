"""Pure functions that build batchUpdate request lists.

Every function in this module takes parsed input (already-walked doc
structure, an already-loaded config dict, etc.) and returns a list of dicts
shaped like Google Docs API request bodies. **No Google calls. No prints.
No argparse.** That's why the whole file is testable with hand-built
fixtures.

Conventions used throughout this module:
- Ops inside a single batchUpdate are sorted by descending character index
  before batching. Google Docs shifts downstream indices after each edit,
  so processing the rightmost op first keeps every earlier index valid.
- `_request_index(op)` returns the highest index touched by an op, used as
  the sort key.
"""
from __future__ import annotations

import re
from typing import Any

from .structure import find_table

# Compile-once regex: see the same pattern in config.py.
ASIST_NOMBRE_RE = re.compile(r"^ASIST_(\d+)_NOMBRE$")
ASIST_PREFIX_RE = re.compile(r"^ASIST_\d+_")

# Attendee table geometry (matches the Consejo's base doc layout).
ATTENDEE_TABLE_INDEX = 1
ATTENDEE_FIRST_ROW = 3
ATTENDEE_NATIVE_ROWS = 9
ATTENDEE_COLS = [("NOMBRE", 0), ("APTO", 1), ("INTERIOR", 2), ("ASISTIO", 3)]
ADMIN_COLS = [("NOMBRE", 0), ("APTO", 1), ("INTERIOR", 2), ("ASISTIO", 3)]


# ---------- Helpers ----------

def _cell_fill_ops(cell: dict[str, Any], value: str) -> list[dict[str, Any]]:
    """Build delete+insert ops to set a table cell's first paragraph to `value`.

    Handles both pre-tagged cells (`{{ASIST_1_NOMBRE}}`) and freshly-inserted
    empty cells (a paragraph with no text).
    """
    ops: list[dict[str, Any]] = []
    paras = cell["paragraphs"]
    if not paras:
        if value:
            ops.append({"insertText": {"location": {"index": cell["start"]}, "text": value}})
        return ops

    p = paras[0]
    text = p["text"]
    if text.endswith("\n"):
        del_start, del_end = p["start"], p["end"] - 1
    else:
        del_start, del_end = p["start"], p["end"]
    if del_end > del_start:
        ops.append({"deleteContentRange": {"range": {"startIndex": del_start, "endIndex": del_end}}})
    if value:
        ops.append({"insertText": {"location": {"index": del_start}, "text": value}})
    return ops


def _request_index(req: dict[str, Any]) -> int:
    """Return the highest character index touched by `req`. Sort key for batching."""
    if "deleteContentRange" in req:
        return req["deleteContentRange"]["range"]["endIndex"]
    if "insertText" in req:
        return req["insertText"]["location"]["index"]
    return 0


def _max_op_index(ops: list[dict[str, Any]]) -> int:
    """Return the highest index touched by any op in `ops`."""
    idxs = [
        op["deleteContentRange"]["range"]["endIndex"]
        for op in ops if "deleteContentRange" in op
    ] + [
        op["insertText"]["location"]["index"]
        for op in ops if "insertText" in op
    ]
    return max(idxs) if idxs else 0


# ---------- Attendee / admin row builders ----------

def count_attendees(cfg: dict[str, Any]) -> int:
    """Return N = highest ASIST_n with a non-empty ASIST_n_NOMBRE in cfg."""
    max_n = 0
    for key, value in cfg.items():
        m = ASIST_NOMBRE_RE.match(key)
        if m and value not in (None, ""):
            max_n = max(max_n, int(m.group(1)))
    return max_n


def build_attendee_row_insert_requests(table_start_index: int, n_new_rows: int) -> list[dict[str, Any]]:
    """Build N sequential `insertTableRow` requests anchored below the last native row."""
    anchor_row = ATTENDEE_FIRST_ROW + ATTENDEE_NATIVE_ROWS - 1
    return [
        {
            "insertTableRow": {
                "tableCellLocation": {
                    "tableStartLocation": {"index": table_start_index},
                    "rowIndex": anchor_row + i,
                    "columnIndex": 0,
                },
                "insertBelow": True,
            }
        }
        for i in range(n_new_rows)
    ]


def build_attendee_fill_requests(blocks: list[dict], cfg: dict[str, Any], n_attendees: int) -> list[dict[str, Any]]:
    """Build direct cell-fill ops for attendee rows 1..n_attendees.

    Each builder sorts its own ops by descending index before returning.
    Callers that merge multiple builders together should re-sort the merged
    list once globally (see `generate.py`).
    """
    t01 = find_table(blocks, ATTENDEE_TABLE_INDEX)
    tagged: list[tuple[int, list[dict[str, Any]]]] = []
    for offset in range(n_attendees):
        row_idx = ATTENDEE_FIRST_ROW + offset
        if row_idx >= len(t01["rows"]):
            continue  # row insertion should have already grown the table
        n = offset + 1
        row = t01["rows"][row_idx]
        for col_name, col_idx in ATTENDEE_COLS:
            cell = row[col_idx]
            value = str(cfg.get(f"ASIST_{n}_{col_name}", "") or "")
            ops = _cell_fill_ops(cell, value)
            if ops:
                tagged.append((_max_op_index(ops), ops))
    tagged.sort(key=lambda t: t[0], reverse=True)
    return [op for _, ops in tagged for op in ops]


def find_administradora_row(blocks: list[dict], table_index: int = ATTENDEE_TABLE_INDEX) -> int:
    """Locate the ADMINISTRADORA data row in the attendees table (last row)."""
    t01 = find_table(blocks, table_index)
    return len(t01["rows"]) - 1


def build_admin_fill_requests(blocks: list[dict], cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Build direct cell-fill ops for the ADMIN row."""
    t01 = find_table(blocks, ATTENDEE_TABLE_INDEX)
    admin_row_idx = find_administradora_row(blocks)
    if admin_row_idx >= len(t01["rows"]):
        return []
    row = t01["rows"][admin_row_idx]
    tagged: list[tuple[int, list[dict[str, Any]]]] = []
    for col_name, col_idx in ADMIN_COLS:
        if col_idx >= len(row):
            continue
        cell = row[col_idx]
        value = str(cfg.get(f"ADMIN_{col_name}", "") or "")
        ops = _cell_fill_ops(cell, value)
        if ops:
            tagged.append((_max_op_index(ops), ops))
    tagged.sort(key=lambda t: t[0], reverse=True)
    return [op for _, ops in tagged for op in ops]


# ---------- Replace + inject builders ----------

def build_replace_requests(cfg: dict[str, Any], fields_doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Build one `replaceAllText` request per non-empty config field.

    Attendee / admin fields are skipped here — they're handled structurally
    by the attendee/admin fill builders above.
    """
    requests: list[dict[str, Any]] = []
    for name, value in cfg.items():
        if name not in fields_doc["fields"]:
            continue
        if ASIST_PREFIX_RE.match(name) or name.startswith("ADMIN_"):
            continue
        if value in (None, ""):
            continue
        placeholder = "{{" + name + "}}"
        requests.append({
            "replaceAllText": {
                "containsText": {"text": placeholder, "matchCase": True},
                "replaceText": str(value),
            }
        })
    return requests


def build_inject_requests(blocks: list[dict]) -> tuple[list[str], list[dict[str, Any]]]:
    """Build the list of batchUpdate requests for the structural injector.

    Returns `(labels, flat_requests)` where `labels[i]` is the human-readable
    description of the logical edit corresponding to `flat_requests[i]`.

    See module docstring for the "sort by descending index" invariant.
    """
    requests: list[dict[str, Any]] = []

    # ---------- Header paragraphs (P002, P003) ----------
    for b in blocks:
        if b["kind"] != "paragraph":
            continue
        text = b["text"]
        if "REUNIÓN EXTRAORDINARIA CONSEJO DE ADMINISTRACIÓN" in text:
            start = b["start"] + text.index("EXTRAORDINARIA")
            end = start + len("EXTRAORDINARIA")
            requests.append({
                "_label": "P002 TIPO_REUNION",
                "ops": [
                    {"deleteContentRange": {"range": {"startIndex": start, "endIndex": end}}},
                    {"insertText": {"location": {"index": start}, "text": "{{TIPO_REUNION}}"}},
                ],
            })
        elif "ACTA No. 07-05-2026" in text:
            start = b["start"] + text.index("07-05-2026")
            end = start + len("07-05-2026")
            requests.append({
                "_label": "P003 ACTA_NO",
                "ops": [
                    {"deleteContentRange": {"range": {"startIndex": start, "endIndex": end}}},
                    {"insertText": {"location": {"index": start}, "text": "{{ACTA_NO}}"}},
                ],
            })

    # ---------- Metadata table T00 ----------
    t00 = find_table(blocks, 0)
    meta_targets = [
        (0, 1, "{{FECHA_INICIO}}"),
        (0, 3, "{{FECHA_FIN}}"),
        (1, 1, "{{CIUDAD}}"),
        (1, 3, "{{DEPARTAMENTO}}"),
    ]
    for ri, ci, tag in meta_targets:
        cell = t00["rows"][ri][ci]
        for para in cell["paragraphs"]:
            text = para["text"]
            if not text.strip():
                continue
            start, end = para["start"], para["end"]
            replace_start, replace_end = (start, end - 1) if text.endswith("\n") else (start, end)
            requests.append({
                "_label": f"T00 R{ri} C{ci} -> {tag}",
                "ops": [
                    {"deleteContentRange": {"range": {"startIndex": replace_start, "endIndex": replace_end}}},
                    {"insertText": {"location": {"index": replace_start}, "text": tag}},
                ],
            })
            break

    # Sort by descending index — see module docstring.
    requests.sort(key=lambda r: _max_op_index(r["ops"]), reverse=True)
    labels = [r["_label"] for r in requests]
    flat = [op for r in requests for op in r["ops"]]
    return labels, flat
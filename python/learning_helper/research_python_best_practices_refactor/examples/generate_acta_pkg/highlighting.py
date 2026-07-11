"""Apply and strip the yellow background + bold highlight on {{TAG}}s.

The base doc carries a yellow highlight on every {{TAG}} so authors can
spot them during maintenance. Every generated copy strips that highlight
so the final Acta looks clean. Both operations live here.
"""
from __future__ import annotations

from typing import Any, Iterator

# Yellow background, matching the original script.
HIGHLIGHT_RGB = {"red": 1.0, "green": 0.95, "blue": 0.6}


def apply_highlight_to_tags(docs_service, doc_id: str, tags_positions: list[dict[str, Any]],
                            batch_size: int = 50) -> int:
    """Apply yellow background + bold to every {{TAG}} range. Return count applied."""
    requests = [
        {
            "updateTextStyle": {
                "range": {"startIndex": tp["start"], "endIndex": tp["end"]},
                "textStyle": {
                    "backgroundColor": {"color": {"rgbColor": HIGHLIGHT_RGB}},
                    "bold": True,
                },
                "fields": "backgroundColor,bold",
            }
        }
        for tp in tags_positions
    ]
    applied = 0
    for i in range(0, len(requests), batch_size):
        chunk = requests[i:i + batch_size]
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": chunk}
        ).execute()
        applied += len(chunk)
    return applied


def _iter_runs_with_range(elem: dict[str, Any]) -> Iterator[tuple[int, int, dict[str, Any]]]:
    """Yield `(startIndex, endIndex, textStyle)` for every textRun in `elem`.

    The Docs API doesn't put `startIndex`/`endIndex` on `textRun` itself;
    we compute it from the parent paragraph's `startIndex` plus the
    cumulative length of preceding runs.
    """
    if "paragraph" in elem:
        p_start = elem.get("startIndex", 0)
        cursor = p_start
        for r in elem["paragraph"].get("elements", []):
            if "textRun" not in r:
                continue
            text = r["textRun"].get("content", "")
            yield cursor, cursor + len(text), r["textRun"].get("textStyle", {})
            cursor += len(text)
    elif "table" in elem:
        for row in elem["table"].get("tableRows", []):
            for cell in row.get("tableCells", []):
                for c in cell.get("content", []):
                    if "paragraph" in c:
                        p_start = c.get("startIndex", 0)
                        cursor = p_start
                        for r in c["paragraph"].get("elements", []):
                            if "textRun" not in r:
                                continue
                            text = r["textRun"].get("content", "")
                            yield cursor, cursor + len(text), r["textRun"].get("textStyle", {})
                            cursor += len(text)


def build_strip_highlight_requests(doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Build `updateTextStyle` requests that clear backgroundColor + bold from every run."""
    targets: list[dict[str, Any]] = []
    for elem in doc["body"]["content"]:
        for start, end, style in _iter_runs_with_range(elem):
            if not style or end <= start:
                continue
            if style.get("backgroundColor") or style.get("bold"):
                targets.append({
                    "start": start,
                    "end": end,
                    "has_bg": bool(style.get("backgroundColor")),
                    "is_bold": bool(style.get("bold")),
                })

    requests: list[dict[str, Any]] = []
    for t in targets:
        text_style: dict[str, Any] = {}
        fields: list[str] = []
        if t["has_bg"]:
            text_style["backgroundColor"] = None
            fields.append("backgroundColor")
        if t["is_bold"]:
            text_style["bold"] = False
            fields.append("bold")
        if not fields:
            continue
        requests.append({
            "updateTextStyle": {
                "range": {"startIndex": t["start"], "endIndex": t["end"]},
                "textStyle": text_style,
                "fields": ",".join(fields),
            }
        })
    return requests


def strip_highlights(docs_service, doc_id: str, batch_size: int = 200) -> tuple[int, int]:
    """Walk the generated doc and strip yellow + bold from every run.

    Returns `(target_run_count, applied_request_count)`.
    """
    doc = docs_service.documents().get(documentId=doc_id).execute()
    requests = build_strip_highlight_requests(doc)
    applied = 0
    for i in range(0, len(requests), batch_size):
        chunk = requests[i:i + batch_size]
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": chunk}
        ).execute()
        applied += len(chunk)
    # target_run_count = number of runs that had a highlight (we don't store
    # that separately; approximate from request count).
    return len(requests), applied
"""`inject-comments` subcommand: attach Google Docs comments to each {{TAG}}.

Each comment carries the ruleset from `tag_rulesets.json` for that tag.
With `--highlight` (default), also applies a yellow background + bold
to each {{TAG}} in the doc body.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from ..config import load_tag_rulesets
from ..highlighting import apply_highlight_to_tags
from ..output import info, emit_result
from ..services import get_credentials, require_id
from ..structure import find_tag_positions


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def register(sub: argparse._SubParsersAction) -> None:
    """Attach this subcommand to the top-level parser."""
    p = sub.add_parser(
        "inject-comments",
        help="Attach Google Docs comment to each {{TAG}} in the base doc with its ruleset",
    )
    p.add_argument("--reset", action="store_true",
                   help="Delete all existing comments on the base doc before re-injecting")
    p.add_argument("--yes", "-y", action="store_true",
                   help="Skip the interactive YES prompt (for AI/automation)")
    p.add_argument("--simulate", action="store_true",
                   help="Print planned comment creations and exit without calling Drive")
    # The `--no-X` flag pattern in argparse: use `store_true` for the positive
    # flag (with default=True on the negative side) and `store_false` for the
    # negative flag. Both write to the same `dest` so the last one wins.
    p.add_argument("--highlight", dest="highlight", action="store_true", default=True,
                   help="Apply yellow background highlight + bold to each {{TAG}} (default: on)")
    p.add_argument("--no-highlight", dest="highlight", action="store_false",
                   help="Skip the background highlight step")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    """Subcommand body."""
    require_id(args.base_doc_id, "--base-doc-id", "ACTA_BASE_DOC_ID",
               info=info, emit_result=emit_result)
    doc_id = args.base_doc_id
    highlight_enabled = getattr(args, "highlight", True)

    try:
        rulesets_doc = load_tag_rulesets(Path(args.fields))
        rulesets = rulesets_doc.get("rulesets", {})
    except FileNotFoundError as e:
        info(f"ERROR: {e}")
        emit_result({"ok": False, "error": str(e)})
        import sys as _sys
        _sys.exit(1)

    if args.simulate:
        info("[SIMULATE] No Drive API calls will be made.")
        info(f"Rulesets loaded: {len(rulesets)} entries")
        emit_result({
            "ok": True,
            "simulated": True,
            "action": "inject-comments",
            "doc_id": doc_id,
            "rulesets_loaded": len(rulesets),
            "highlight_enabled": highlight_enabled,
        })
        return

    creds = get_credentials()
    from googleapiclient.discovery import build
    drive_service = build("drive", "v3", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)

    doc = docs_service.documents().get(documentId=doc_id).execute()
    all_positions = find_tag_positions(doc)

    # Dedup: keep first occurrence of each tag.
    seen: set[str] = set()
    unique_tags: list[dict] = []
    for tp in all_positions:
        if tp["tag"] not in seen:
            seen.add(tp["tag"])
            unique_tags.append(tp)

    info(f"Found {len(unique_tags)} unique tags in base doc")
    info(f"Rulesets available: {len(rulesets)}")

    if not args.yes:
        try:
            response = input("Type YES to proceed: ").strip()
        except EOFError:
            response = ""
        if response != "YES":
            info("Aborted. No changes made.")
            emit_result({"ok": False, "error": "aborted_by_user"})
            return

    # --reset: delete existing comments first.
    deleted = 0
    if args.reset:
        info("[RESET] Listing existing comments on the doc...")
        page_token = None
        existing_ids: list[str] = []
        while True:
            params = {"fileId": doc_id, "fields": "comments(id)", "pageSize": 100}
            if page_token:
                params["pageToken"] = page_token
            resp = drive_service.comments().list(**params).execute()
            existing_ids.extend(c["id"] for c in resp.get("comments", []))
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        info(f"Found {len(existing_ids)} existing comments; deleting...")
        for cid in existing_ids:
            try:
                drive_service.comments().delete(fileId=doc_id, commentId=cid).execute()
                deleted += 1
            except Exception as e:
                info(f"  [WARN] could not delete {cid}: {e}")

    # Highlight step (optional).
    highlighted = 0
    if highlight_enabled:
        info("Applying yellow background highlight to all {{TAG}}s in doc body...")
        highlighted = apply_highlight_to_tags(docs_service, doc_id, unique_tags)
        info(f"Highlighted {highlighted} tags.")

    # Create one comment per unique tag.
    info(f"Creating {len(unique_tags)} comments...")
    created = 0
    failures: list[dict] = []
    for tp in unique_tags:
        tag = tp["tag"]
        field_name = tag.strip("{}")
        rs = rulesets.get(field_name)
        if not rs:
            info(f"  [SKIP] no ruleset for {tag}")
            continue
        body_text = f"{tag}\n\n{_format_ruleset_comment(rs)}"
        anchor = {
            "r": tag,
            "a": [{"ls": "/", "lt": doc_id, "start": tp["start"] - 1, "end": tp["end"] - 1}],
        }
        try:
            drive_service.comments().create(
                fileId=doc_id,
                body={"content": body_text, "anchor": anchor},
                fields="id",
            ).execute()
            created += 1
        except Exception as e:
            failures.append({"tag": tag, "error": str(e)[:200]})
            info(f"  [ERR] {tag}: {str(e)[:120]}")

    info(f"Created {created} comments. Failed: {len(failures)}. "
         f"Deleted: {deleted}. Highlighted: {highlighted}.")
    emit_result({
        "ok": len(failures) == 0,
        "action": "inject-comments",
        "doc_id": doc_id,
        "comments_created": created,
        "comments_failed": len(failures),
        "comments_deleted": deleted,
        "tags_highlighted": highlighted,
        "failures": failures,
    })


def _format_ruleset_comment(ruleset: dict) -> str:
    """Render a ruleset dict as a comment body string (Markdown-flavored)."""
    lines: list[str] = []
    if "what" in ruleset:
        lines.append(f"**{ruleset['what']}**")
    parts: list[str] = []
    if "type" in ruleset:
        parts.append(f"Tipo: `{ruleset['type']}`")
    if "format" in ruleset:
        parts.append(f"Formato: `{ruleset['format']}`")
    if parts:
        lines.append(" · ".join(parts))
    if "values" in ruleset and isinstance(ruleset["values"], list):
        lines.append(f"Valores: {', '.join('`' + str(v) + '`' for v in ruleset['values'])}")
    if "rules" in ruleset and ruleset["rules"]:
        lines.append("")
        lines.append("**Reglas:**")
        for r in ruleset["rules"]:
            lines.append(f"- {r}")
    if "example" in ruleset:
        lines.append("")
        lines.append("**Ejemplo:**")
        lines.append("```")
        lines.append(str(ruleset["example"]))
        lines.append("```")
    if "deprecated" in ruleset and ruleset["deprecated"]:
        lines.append("")
        lines.append("> ⚠️ **DEPRECATED** — usa el campo recomendado en su lugar.")
    return "\n".join(lines)
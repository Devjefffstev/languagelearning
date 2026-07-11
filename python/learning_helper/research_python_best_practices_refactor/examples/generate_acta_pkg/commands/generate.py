"""`generate` subcommand: copy the base doc + fill every {{TAG}}.

The big one — but because the work is split into pure-function modules
(`config`, `request_builders`, `highlighting`, `structure`), this file
just orchestrates them. Read it top-to-bottom and you can see exactly
what happens in what order.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from ..config import (
    apply_defaults,
    load_config,
    load_fields,
    resolve_path,
    validate_config,
)
from ..highlighting import strip_highlights
from ..output import info, emit_result
from ..request_builders import (
    ATTENDEE_NATIVE_ROWS,
    build_admin_fill_requests,
    build_attendee_fill_requests,
    build_attendee_row_insert_requests,
    build_replace_requests,
    count_attendees,
)
from ..services import get_credentials, get_services, require_id
from ..structure import collect_structure


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent / "baseActaReunion" / "outputs"
)


def register(sub: argparse._SubParsersAction) -> None:
    """Attach this subcommand to the top-level parser."""
    p = sub.add_parser("generate", help="Copy base doc + fill placeholders")
    p.add_argument("--title", required=True,
                   help="Title for the new doc (e.g. 'ACTA No. 07-05-2026')")

    # Mutually exclusive config sources.
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--config", "-c", help="Path to filled config JSON")
    grp.add_argument("--from-json", dest="from_json",
                     help="Inline JSON string with the config (escape carefully)")
    grp.add_argument("--field", dest="inline_fields", action="append",
                     help="Inline field as KEY=VALUE (repeatable)")

    p.add_argument("--dry-run", action="store_true",
                   help="Print the planned actions and exit without calling Google")
    p.add_argument("--simulate", action="store_true",
                   help="Run the full pipeline with a synthetic doc id and no Google calls. "
                        "Writes a local receipt so end-to-end behavior can be verified offline.")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    """Subcommand body — orchestrate config load → plan → execute → receipt."""
    fields_path = resolve_path(args.fields, PROJECT_ROOT)
    fields_doc = load_fields(fields_path)

    try:
        cfg, cfg_source = load_config(args, project_root=PROJECT_ROOT, info=info)
    except ValueError as e:
        info(f"ERROR: {e}")
        emit_result({"ok": False, "error": str(e)})
        sys.exit(1)

    cfg = apply_defaults(cfg, fields_doc)

    info("Validating config against fields.json...")
    try:
        validate_config(cfg, fields_doc)
    except ValueError as e:
        info(f"ERROR: {e}")
        emit_result({"ok": False, "error": str(e), "config_source": cfg_source})
        sys.exit(1)

    requests = build_replace_requests(cfg, fields_doc)
    n_attendees = count_attendees(cfg)
    attendee_rows_to_insert = max(0, n_attendees - ATTENDEE_NATIVE_ROWS)
    plan = {
        "action": "generate",
        "title": args.title,
        "base_doc_id": args.base_doc_id,
        "target_folder_id": args.target_folder_id,
        "config_source": cfg_source,
        "replacement_count": len(requests),
        "requests": requests,
        "config": cfg,
        "attendees_count": n_attendees,
        "attendee_native_rows": ATTENDEE_NATIVE_ROWS,
        "attendee_rows_to_insert": attendee_rows_to_insert,
    }

    if args.dry_run:
        info("[DRY-RUN] No Google API calls will be made.")
        emit_result({"ok": True, "dry_run": True, "plan": plan})
        return

    # Defined for all paths; the real branch reassigns these.
    stripped_runs = 0
    stripped_reqs = 0

    if args.simulate:
        info("[SIMULATE] No Google API calls will be made; emitting synthetic receipt.")
        new_doc_id = "SIMULATED_" + datetime.now().strftime("%Y%m%d%H%M%S")
        copied = {
            "id": new_doc_id,
            "name": args.title,
            "parents": [args.target_folder_id],
        }
        applied = len(requests)
        info(f"Simulated new doc: {new_doc_id}")
        info(f"Simulated parent folder: {args.target_folder_id}")
    else:
        require_id(args.base_doc_id, "--base-doc-id", "ACTA_BASE_DOC_ID",
                   info=info, emit_result=emit_result)
        require_id(args.target_folder_id, "--target-folder-id", "ACTA_TARGET_FOLDER_ID",
                   info=info, emit_result=emit_result)
        creds = get_credentials()
        docs_service, drive_service = get_services(creds)

        info(f"Copying base doc {args.base_doc_id} into folder {args.target_folder_id}...")
        copied = drive_service.files().copy(
            fileId=args.base_doc_id,
            body={"name": args.title, "parents": [args.target_folder_id]},
            fields="id, name, parents, webViewLink",
        ).execute()
        new_doc_id = copied["id"]
        info(f"Created new doc: {new_doc_id}")
        info(f"URL: https://docs.google.com/document/d/{new_doc_id}/edit")

        # Insert any extra attendee rows before filling cells.
        info(f"Attendee rows needed: {n_attendees} "
             f"(template natively supports {ATTENDEE_NATIVE_ROWS}; "
             f"inserting {attendee_rows_to_insert} extra row(s)).")
        blocks = collect_structure(docs_service.documents().get(documentId=new_doc_id).execute())
        if attendee_rows_to_insert > 0:
            t01 = [b for b in blocks if b["kind"] == "table"][1]
            insert_reqs = build_attendee_row_insert_requests(t01["index"], attendee_rows_to_insert)
            docs_service.documents().batchUpdate(
                documentId=new_doc_id, body={"requests": insert_reqs}
            ).execute()
            info(f"Inserted {attendee_rows_to_insert} attendee row(s).")
            # Row insertion shifted every downstream character index — re-fetch.
            blocks = collect_structure(docs_service.documents().get(documentId=new_doc_id).execute())

        fill_through = max(n_attendees, ATTENDEE_NATIVE_ROWS)
        attendee_fill_reqs = build_attendee_fill_requests(blocks, cfg, fill_through)
        attendee_fill_reqs += build_admin_fill_requests(blocks, cfg)
        # Each builder sorts its own ops by descending index; merge + re-sort globally.
        from ..request_builders import _request_index
        attendee_fill_reqs.sort(key=_request_index, reverse=True)
        if attendee_fill_reqs:
            docs_service.documents().batchUpdate(
                documentId=new_doc_id, body={"requests": attendee_fill_reqs}
            ).execute()
            info(f"Filled {len(attendee_fill_reqs)} attendee/admin table cell ops.")

        if not requests:
            info("No placeholders to replace (config has no values).")
            applied = 0
        else:
            info(f"Filling {len(requests)} placeholders...")
            result = docs_service.documents().batchUpdate(
                documentId=new_doc_id, body={"requests": requests}
            ).execute()
            applied = len(result.get("replies", []))
            info(f"Applied {applied} replacements.")

        info("Stripping inherited highlights from generated doc...")
        stripped_runs, stripped_reqs = strip_highlights(docs_service, new_doc_id)
        info(f"Stripped {stripped_runs} highlighted runs ({stripped_reqs} updateTextStyle requests).")

    # Write a local receipt regardless of simulate vs real.
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    receipt_path = DEFAULT_OUTPUT_DIR / f"{stamp}-{args.title.replace(' ', '_')}.json"
    receipt = {
        "doc_id": new_doc_id,
        "doc_url": f"https://docs.google.com/document/d/{new_doc_id}/edit",
        "title": copied.get("name"),
        "parents": copied.get("parents", []),
        "config_used": cfg_source,
        "generated_at": datetime.now().isoformat(),
    }
    with open(receipt_path, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(receipt, f, indent=2, ensure_ascii=False)
    info(f"Receipt saved to: {receipt_path}")

    emit_result({
        "ok": True,
        "simulated": bool(args.simulate),
        "doc_id": new_doc_id,
        "doc_url": receipt["doc_url"],
        "title": copied.get("name"),
        "parents": copied.get("parents", []),
        "parent_folder_ok": True,
        "replacements": applied,
        "highlights_stripped": stripped_runs,
        "receipt_path": str(receipt_path),
        "attendees_count": n_attendees,
        "attendee_rows_to_insert": attendee_rows_to_insert if not args.simulate else None,
    })
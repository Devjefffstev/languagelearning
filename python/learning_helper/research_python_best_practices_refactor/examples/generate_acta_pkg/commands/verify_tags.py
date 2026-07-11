"""`verify-tags` subcommand: read-only diff of {{TAGS}} in the doc vs fields.json.

Exits 0 if every tag in the doc maps to a schema field, 1 otherwise.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from ..config import load_fields, resolve_path
from ..output import info, emit_result
from ..services import get_credentials, get_services, require_id
from ..structure import extract_doc_text, TAG_PATTERN


def register(sub: argparse._SubParsersAction) -> None:
    """Attach this subcommand to the top-level parser."""
    p = sub.add_parser(
        "verify-tags",
        help="Read-only: list {{TAGS}} in the base doc vs fields.json",
    )
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    """Subcommand body."""
    import sys

    require_id(args.base_doc_id, "--base-doc-id", "ACTA_BASE_DOC_ID",
               info=info, emit_result=emit_result)

    creds = get_credentials()
    docs_service, _ = get_services(creds)

    doc = docs_service.documents().get(documentId=args.base_doc_id).execute()
    text = extract_doc_text(doc)
    found_tags = sorted(set(TAG_PATTERN.findall(text)))
    found_field_names = sorted({t.strip("{}") for t in found_tags})

    fields_path = resolve_path(args.fields, _project_root())
    fields_doc = load_fields(fields_path)
    expected_field_names = sorted(fields_doc["fields"].keys())

    in_both = sorted(set(found_field_names) & set(expected_field_names))
    in_doc_only = sorted(set(found_field_names) - set(expected_field_names))
    in_schema_only = sorted(set(expected_field_names) - set(found_field_names))

    info("Tags present in base doc:    " + ", ".join(found_tags) if found_tags else "(none)")
    info(f"Expected by schema ({len(expected_field_names)} fields).")
    info(f"Matched: {len(in_both)} | Doc-only: {len(in_doc_only)} | Schema-only: {len(in_schema_only)}")
    if in_doc_only:
        info(f"  Doc-only tags (will be ignored by generator): {in_doc_only}")
    if in_schema_only:
        info(f"  Schema-only fields (no tag in doc; will be left blank): {in_schema_only}")

    ok = len(in_doc_only) == 0
    emit_result({
        "ok": ok,
        "matched": in_both,
        "doc_only": in_doc_only,
        "schema_only": in_schema_only,
        "tags_in_doc": found_tags,
    })
    if not ok:
        sys.exit(1)


def _project_root() -> Path:
    """Return the repo root (parent of `generate_acta_pkg/`)."""
    return Path(__file__).resolve().parent.parent.parent.parent
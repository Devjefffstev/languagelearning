"""`inject-tags` subcommand: structural injector that places `{{TAGS}}` in the base doc.

Walks the live base doc by position and replaces specific cells/paragraphs
with `{{TAGS}}`. Run this **once** before any `generate` call. Optional
`--reset` clears any existing tags first.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from ..output import info, emit_result
from ..request_builders import build_inject_requests
from ..services import get_credentials, get_services, require_id
from ..structure import collect_structure, extract_doc_text


TAG_RE = re.compile(r"\{\{[A-Z_0-9]+\}\}")


def register(sub: argparse._SubParsersAction) -> None:
    """Attach this subcommand to the top-level parser."""
    p = sub.add_parser(
        "inject-tags",
        help="Structural injector: place {{TAGS}} in the base doc by position",
    )
    p.add_argument(
        "--reset",
        action="store_true",
        help="Clear any existing {{TAGS}} from the base doc before injecting",
    )
    p.add_argument(
        "--simulate",
        action="store_true",
        help="Print planned operations and exit without calling Google",
    )
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    """Subcommand body."""
    require_id(args.base_doc_id, "--base-doc-id", "ACTA_BASE_DOC_ID",
               info=info, emit_result=emit_result)
    doc_id = args.base_doc_id

    if args.simulate:
        info("[SIMULATE] No Google API calls will be made.")
        info(f"Would inject {{TAGS}} into base doc {doc_id}.")
        info("(Use --simulate without auth to validate config; running for real requires credentials.)")
        emit_result({
            "ok": True,
            "simulated": True,
            "action": "inject-tags",
            "doc_id": doc_id,
        })
        return

    creds = get_credentials()
    docs_service, _ = get_services(creds)

    if args.reset:
        _reset_existing_tags(docs_service, doc_id)

    info("Reading base doc structure...")
    doc = docs_service.documents().get(documentId=doc_id).execute()
    blocks = collect_structure(doc)

    info(f"Building {len(blocks)} structural blocks into batchUpdate requests...")
    labels, requests = build_inject_requests(blocks)
    info(f"Will execute {len(requests)} API operations ({len(labels)} logical edits):")
    for label in labels:
        info(f"  - {label}")

    info("Executing batchUpdate...")
    result = docs_service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()
    replies = result.get("replies", [])
    info(f"Applied {len(replies)} operations.")

    # Verify by re-reading the doc and listing the tags now present.
    doc = docs_service.documents().get(documentId=doc_id).execute()
    text = extract_doc_text(doc)
    found_tags = sorted(set(TAG_RE.findall(text)))
    info(f"Tags now present in base doc ({len(found_tags)}): {found_tags}")

    emit_result({
        "ok": True,
        "action": "inject-tags",
        "doc_id": doc_id,
        "operations": len(replies),
        "tags_in_doc": found_tags,
    })


def _reset_existing_tags(docs_service, doc_id: str) -> None:
    """Delete every {{TAG}} from the base doc, right-to-left.

    Deletion right-to-left keeps earlier indices valid as later ones go away.
    """
    info("[RESET] Clearing existing {{TAGS}} from base doc...")
    doc = docs_service.documents().get(documentId=doc_id).execute()
    text = extract_doc_text(doc)
    existing_tags = sorted(set(TAG_RE.findall(text)))
    if not existing_tags:
        info("[RESET] No existing tags found.")
        return

    info(f"Found {len(existing_tags)} existing tags: {existing_tags}")
    for tag in sorted(existing_tags, key=lambda t: text.count(t), reverse=True):
        positions = []
        start = 0
        while True:
            idx = text.find(tag, start)
            if idx == -1:
                break
            positions.append(idx)
            start = idx + len(tag)
        for p in reversed(positions):
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": [{
                    "deleteContentRange": {
                        "range": {"startIndex": p + 1, "endIndex": p + 1 + len(tag)}
                    }
                }]},
            ).execute()
    info("[RESET] Cleared all existing tags.")
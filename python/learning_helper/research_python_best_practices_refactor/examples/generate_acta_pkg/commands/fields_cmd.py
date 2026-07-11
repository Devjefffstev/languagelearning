"""`fields` subcommand: print the fields.json schema.

Smallest subcommand. Good place to read first — it shows the full
subcommand contract (register + run) without any Google calls.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..config import load_fields, resolve_path


def register(sub: argparse._SubParsersAction) -> None:
    """Attach this subcommand to the top-level parser."""
    p = sub.add_parser("fields", help="Print the field schema")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    """Subcommand body — kept short and side-effect-light."""
    fields_path = resolve_path(args.fields, _project_root())
    fields_doc = load_fields(fields_path)
    print(json.dumps(fields_doc, indent=2, ensure_ascii=False))


def _project_root() -> Path:
    """Return the repo root (parent of `generate_acta_pkg/`)."""
    return Path(__file__).resolve().parent.parent.parent.parent
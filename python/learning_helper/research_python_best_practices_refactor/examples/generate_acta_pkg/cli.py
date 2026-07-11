"""Argparse wiring for every subcommand.

Each subcommand lives in its own module under `commands/`. This module's
only job is to declare the CLI shape and dispatch to the right function.
Adding a new subcommand = adding one file under commands/ + one line here.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Subcommand modules follow a uniform contract: each exports a
# `register(sub)` function that attaches itself to the top-level parser.
from .commands import (
    inject_tags,
    verify_tags,
    generate,
    fields_cmd,
    inject_comments,
)

# Top-level defaults pulled from the environment, just like the original script.
# PROJECT_ROOT is the repo root that contains both this package and `scripts/`.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_BASE_DOC_ID = os.environ.get("ACTA_BASE_DOC_ID", "")
DEFAULT_TARGET_FOLDER_ID = os.environ.get("ACTA_TARGET_FOLDER_ID", "")
DEFAULT_FIELDS_PATH = (
    Path(__file__).resolve().parent / "baseActaReunion" / "fields.json"
)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        description="Generate Consejo de Administración Acta from base Google Doc template."
    )
    parser.add_argument(
        "--base-doc-id",
        default=DEFAULT_BASE_DOC_ID,
        help="Base doc ID (default: $ACTA_BASE_DOC_ID env var)",
    )
    parser.add_argument(
        "--target-folder-id",
        default=DEFAULT_TARGET_FOLDER_ID,
        help="Target Drive folder ID (default: $ACTA_TARGET_FOLDER_ID env var)",
    )
    parser.add_argument(
        "--fields",
        default=str(DEFAULT_FIELDS_PATH),
        help="Path to fields.json schema",
    )

    sub = parser.add_subparsers(dest="action", required=True)

    # One line per subcommand — adding a new one means adding one line here
    # and one new file under commands/. No more scrolling to find where
    # subcommands are registered.
    inject_tags.register(sub)
    verify_tags.register(sub)
    generate.register(sub)
    fields_cmd.register(sub)
    inject_comments.register(sub)

    return parser


def main() -> None:
    """Parse args, dispatch to the chosen subcommand, exit cleanly."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
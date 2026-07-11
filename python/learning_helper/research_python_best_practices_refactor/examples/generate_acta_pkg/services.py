"""Google API auth + service builders — the only module that talks to Google.

Everything that constructs a `docs` or `drive` service lives here. Subcommand
modules import from this file; they never construct services themselves.
That gives you one place to change auth (swap OAuth for a service account,
add a token cache, etc.) without grepping every command.

The original script imported from `scripts/auth/auth.py` in the parent
repo. This refactor keeps that contract: the default `get_credentials()`
function looks for `scripts.auth.auth` on `sys.path`. If you ship this
package standalone, replace this with your own auth flow.
"""
from __future__ import annotations

import sys
from pathlib import Path


def get_credentials():
    """Return Google API credentials.

    By default, delegates to the existing `scripts.auth.auth.get_credentials`
    in the consejoMulticarabelas repo (the original script's behaviour).
    The repo root is added to `sys.path` so the existing `auth.py` can be
    imported without any setup.

    To use this package standalone, swap this body for your own OAuth flow
    (e.g. a `token.pickle` cache, a service account JSON key, etc.).
    """
    # Project root = the parent of the `generate_acta_pkg/` directory.
    # Resolved at call time, not at import time, so it works from any cwd.
    pkg_dir = Path(__file__).resolve().parent
    project_root = pkg_dir.parent.parent  # assumes this package lives at <root>/scripts/generate_acta_pkg/
    repo_root = project_root
    scripts_dir = repo_root / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    # Late import so this module is safe to import even when the parent
    # repo's auth module isn't on sys.path (e.g. during a unit test).
    from auth.auth import get_credentials as _get_credentials
    return _get_credentials()


def get_services(creds):
    """Build and return `(docs_service, drive_service)`."""
    # Late import: keeps `googleapiclient` out of the import path for
    # pure-function modules like `request_builders.py`.
    from googleapiclient.discovery import build
    return build("docs", "v1", credentials=creds), build("drive", "v3", credentials=creds)


def require_id(value: str, flag_name: str, env_name: str, *, info, emit_result) -> None:
    """Fail fast with a clear error if a required doc/folder ID is missing.

    Prints the same `[INFO] ERROR: …` line the original script prints, then
    emits a structured JSON result and exits with code 1. The caller (the
    subcommand's `run()` function) does not need to handle this — the process
    exits here.
    """
    if not value:
        info(f"ERROR: {flag_name} not set. Pass it explicitly or set ${env_name}.")
        emit_result({"ok": False, "error": f"missing_{env_name.lower()}"})
        sys.exit(1)
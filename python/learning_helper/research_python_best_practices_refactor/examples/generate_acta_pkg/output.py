"""Single source of truth for human logs and machine-readable results.

Both `info()` and `emit_result()` write to stdout on purpose: the original
script's contract is "[INFO] lines for humans, last JSON line for
machines." Putting both here means if you ever want to switch to real
logging, change a colour prefix, or split logs to stderr, you do it in
one file.
"""
from __future__ import annotations

import json
from typing import Any


def info(msg: str) -> None:
    """Print a human-readable log line prefixed with `[INFO] `.

    Goes to stdout (not stderr) because the original script's contract is
    "every output line is captured by the AI agent that calls us." If you
    move this to stderr, you'd need to update the agent's parser too.
    """
    print(f"[INFO] {msg}")


def emit_result(payload: dict[str, Any]) -> None:
    """Print a single JSON line as the final result.

    This is the contract the calling agent reads. Always the *last* line on
    stdout; everything before it is `[INFO]` log lines.
    """
    print(json.dumps(payload, ensure_ascii=False))
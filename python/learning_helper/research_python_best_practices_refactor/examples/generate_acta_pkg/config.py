"""Config loading and validation.

Three responsibilities, all kept in this one module because they're tightly
related:

1. Read `fields.json` (the schema) from disk.
2. Read a per-meeting config dict from one of three sources (file path,
   inline JSON string, or repeated `--field KEY=VALUE` flags).
3. Validate the merged config against the schema (required fields present,
   enums in range) and apply defaults from the schema.

Kept *pure* (no Google calls, no prints, no sys.exit) so you can call it
from a unit test and assert on the result.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# These two regexes are the only piece of "structural knowledge" the config
# module needs to share with request_builders.py. Compiled once at import
# time so the regex isn't recompiled on every call.
ASIST_NOMBRE_RE = re.compile(r"^ASIST_(\d+)_NOMBRE$")
ASIST_PREFIX_RE = re.compile(r"^ASIST_\d+_")


# ---------- Path + file helpers ----------

def resolve_path(p: str | Path, project_root: Path) -> Path:
    """Resolve a path: absolute paths stay, relative paths join to project_root."""
    p = Path(p)
    if not p.is_absolute():
        p = project_root / p
    return p


def load_fields(path: Path) -> dict[str, Any]:
    """Load the field schema from `fields.json`."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tag_rulesets(path: Path) -> dict[str, Any]:
    """Load `tag_rulesets.json` — used by `inject-comments` for the ruleset body."""
    p = Path(path)
    if p.name == "fields.json":
        # If user passed fields.json, the rulesets live next to it.
        p = p.parent / "tag_rulesets.json"
    if not p.exists():
        raise FileNotFoundError(f"tag_rulesets.json not found at {p}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Config source parsing ----------

def parse_inline_fields(items: list[str] | None) -> dict[str, str]:
    """Parse repeated `--field KEY=VALUE` flags into a dict."""
    cfg: dict[str, str] = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"--field must be KEY=VALUE, got: {item!r}")
        k, v = item.split("=", 1)
        cfg[k.strip()] = v
    return cfg


def parse_from_json(blob: str | None) -> dict[str, Any]:
    """Parse an inline `--from-json '{...}'` string."""
    if blob is None:
        return {}
    try:
        return json.loads(blob)
    except json.JSONDecodeError as e:
        raise ValueError(f"--from-json is not valid JSON: {e}")


def load_config(args: Any, *, project_root: Path, info) -> tuple[dict[str, Any], str]:
    """Load the merged config dict from whichever source the user provided.

    Returns `(cfg, source_label)` where `source_label` is one of:
        - the resolved path to the config file
        - "<from-json>" for inline JSON
        - "<inline-fields>" for repeated --field flags

    Raises ValueError if zero or more than one source was provided.
    """
    provided = sum([bool(args.config), bool(args.from_json), bool(args.inline_fields)])
    if provided == 0:
        raise ValueError(
            "Provide one of: --config, --from-json, or --field KEY=VALUE (repeatable)."
        )
    if provided > 1:
        raise ValueError(
            "--config, --from-json, and --field are mutually exclusive; pass exactly one."
        )

    if args.config:
        cfg_path = resolve_path(args.config, project_root)
        info(f"Loading config from file: {cfg_path}")
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f), str(cfg_path)
    if args.from_json:
        info("Loading config from --from-json string")
        return parse_from_json(args.from_json), "<from-json>"
    info("Loading config from --field flags")
    return parse_inline_fields(args.inline_fields), "<inline-fields>"


# ---------- Validation + defaults ----------

def apply_defaults(cfg: dict[str, Any], fields_doc: dict[str, Any]) -> dict[str, Any]:
    """Fill in any defaults from the schema for keys missing from cfg."""
    for name, spec in fields_doc["fields"].items():
        if name not in cfg and "default" in spec:
            cfg[name] = spec["default"]
    return cfg


def validate_config(cfg: dict[str, Any], fields_doc: dict[str, Any]) -> None:
    """Validate cfg against the schema. Raises ValueError on the first failure."""
    fields = fields_doc["fields"]
    errors: list[str] = []

    for name, spec in fields.items():
        if not spec.get("required", False):
            continue
        if name not in cfg or cfg[name] in (None, ""):
            errors.append(f"Missing required field: {name}")

    # Enum check for TIPO_REUNION; also normalize to uppercase.
    if "TIPO_REUNION" in cfg and isinstance(cfg["TIPO_REUNION"], str):
        cfg["TIPO_REUNION"] = cfg["TIPO_REUNION"].upper()
    if "TIPO_REUNION" in cfg and cfg["TIPO_REUNION"] not in fields["TIPO_REUNION"]["values"]:
        errors.append(
            f"TIPO_REUNION must be one of {fields['TIPO_REUNION']['values']}, "
            f"got {cfg['TIPO_REUNION']!r}"
        )

    if errors:
        raise ValueError("; ".join(errors))
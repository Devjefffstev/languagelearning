# generate_acta_pkg — refactored package

Refactored package version of `scripts/generate_acta/generate_acta.py`. Same
behavior, same subcommands, same env vars — just split into modules where each
file has one job.

See the parent directory's `README.md` for the full tour of Python packages,
modules, and best practices that motivated this refactor.

## Install

This package is meant to be embedded inside the `consejoMulticarabelas` repo
(it imports the existing `scripts/auth/auth.py` for OAuth). For standalone
use, replace `services.get_credentials()` with your own auth flow.

```bash
# Editable install (recommended for development):
pip install -e .

# Or just use it without installing:
python -m generate_acta_pkg --help
```

## Run

```bash
# Show all subcommands:
python -m generate_acta_pkg --help

# Print the schema:
python -m generate_acta_pkg fields

# Full pipeline, no Google calls (uses synthetic doc id):
python -m generate_acta_pkg generate \
  --title "ACTA No. TEST-DRYRUN" \
  --field ACTA_NO=01-01-2026 \
  --field TIPO_REUNION=Ordinaria \
  --field FECHA_INICIO="01/01/2026 09:00:00" \
  --field FECHA_FIN="01/01/2026 11:00:00" \
  --field HORA_CIERRE="11:00 A.M." \
  --field PRESIDENTE="GLADYS AMADO T." \
  --field SECRETARIO="JEFFERSON S. SOTO M." \
  --field ORDEN_DIA="1. Tema A\n2. Tema B" \
  --field ORDEN_DIA_DESCRIPTIVO="1. Tema A — descripción.\n2. Tema B — descripción." \
  --simulate

# Or via the Makefile:
make simulate
make fields
make inject-simulate
```

## Environment

Required for real (non-simulate) runs:

| Variable                | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| `ACTA_BASE_DOC_ID`      | The base Acta template doc               |
| `ACTA_TARGET_FOLDER_ID` | The Drive folder to drop new Actas into  |

The OAuth token (`token.pickle`) is loaded from the parent repo's
`scripts/auth/auth.py` — see `services.py`.

## Layout

```
generate_acta_pkg/
├── __init__.py             package metadata
├── __main__.py             entry point
├── cli.py                  argparse
├── config.py               load + validate config
├── output.py               info() / emit_result()
├── services.py             Google auth + service builders
├── structure.py            walk the doc body
├── request_builders.py     build batchUpdate request lists
├── highlighting.py         apply + strip highlights
├── commands/               one subcommand per file
│   ├── __init__.py
│   ├── inject_tags.py
│   ├── verify_tags.py
│   ├── generate.py
│   ├── fields_cmd.py
│   └── inject_comments.py
└── baseActaReunion/        data files (fields.json, sample.json)
```
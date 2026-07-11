"""generate_acta_pkg — refactored package version of scripts/generate_acta/generate_acta.py.

This package is a 1:1 logical refactor of the original single-file script.
Same behavior, same subcommands, same env vars — just split into modules
where each file has one job.

Public surface (re-exported here for convenience):
    from generate_acta_pkg import cli  # argparse entry point

Package layout:
    generate_acta_pkg/
    ├── __init__.py             (you are here)
    ├── __main__.py             (entry point: `python -m generate_acta_pkg`)
    ├── cli.py                  (argparse)
    ├── config.py               (load + validate config dicts)
    ├── output.py               (info / emit_result)
    ├── services.py             (Google auth + service builders)
    ├── structure.py            (walk a doc body)
    ├── request_builders.py     (build batchUpdate request lists — pure)
    ├── highlighting.py         (apply + strip highlights — pure)
    ├── commands/               (one subcommand per file)
    │   ├── __init__.py
    │   ├── inject_tags.py
    │   ├── verify_tags.py
    │   ├── generate.py
    │   ├── fields_cmd.py
    │   └── inject_comments.py
    └── baseActaReunion/        (data files: fields.json, sample.json)
"""
__version__ = "1.0.0"
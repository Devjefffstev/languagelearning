# Python Best Practices: Modules, Packages, and a Refactored `generate_acta`

## Description

Python is a language that grows with you. You can write a useful program in a
single `.py` file, run it, and move on. But the moment that file gets over a
few hundred lines — or holds more than one job (parsing CLI flags, walking a
document structure, calling a remote API, formatting output) — the "one big
script" style starts to hurt: you can't find anything, you can't test pieces
in isolation, and you can't reuse a function without copying the whole file.

This guide is about two ideas that solve that pain:

1. **Modules** — a single `.py` file that groups related code under one name.
   Every file you've ever written is already a module; the trick is to use
   that fact deliberately.
2. **Packages** — a directory of modules with a special `__init__.py` file.
   A package gives you a *namespace* so `generate_acta.config` and
   `generate_acta.structure` can live side-by-side without their names
   colliding.

The official Python tutorial says it directly:

> *Packages are a way of structuring Python's module namespace by using
> "dotted module names". … The use of dotted module names saves the authors
> of multi-module packages from having to worry about each other's module
> names.*
> — [Python Tutorial §6](https://docs.python.org/3/tutorial/modules.html)

Once you internalize this, **imports** stop being magic. `from generate_acta_pkg.structure import collect_structure` reads in plain English as:
*"from the `generate_acta_pkg` package, take the `structure` module, and give me the `collect_structure` function."*

Your current `scripts/generate_acta/generate_acta.py` is **1,366 lines** doing
seven different jobs (CLI parsing, OAuth auth, Google service construction,
document structure walking, request building, output formatting, and the five
subcommands themselves). That's a textbook case for splitting into modules.
The refactor on disk here turns it into an 11-module package where every file
has one clear responsibility and most modules are under 200 lines.

The mental model to take away: **a module is a drawer, a package is a
toolbox, `__init__.py` is the toolbox's nameplate, and an `import` is you
saying "open that drawer, hand me that tool."** When you put a 1,400-line
file into a toolbox of labeled drawers, every tool becomes findable,
testable, and reusable — even by future-you, six months from now.

## Analogy

**Imagine a busy workshop.**

- A **module** (e.g. `structure.py`) is **one labeled drawer in a toolbox**.
  It holds one focused set of tools — in this case, functions that walk a
  Google Doc and report what they find (paragraphs, tables, cells).
- A **package** (`generate_acta_pkg/`) is **the whole toolbox**. The folder
  exists, but it's just an empty box until you put an **`__init__.py`** file
  in it. That file is the **nameplate** on the outside of the toolbox: it
  tells Python "this folder is a package; you can import things from it."
- An **import statement** is you walking to the toolbox and saying
  *"open the **structure** drawer and hand me the **collect_structure**
  tool."* In Python: `from generate_acta_pkg.structure import collect_structure`.
- A **subcommand** (`inject-tags`, `verify-tags`, `generate`, …) becomes
  its own drawer (`commands/inject_tags.py`, etc.) — small, single-purpose,
  easy to find when something breaks.

The mapping back to your script:

| Big script concept            | In the toolbox (refactored package)             |
| ----------------------------- | ----------------------------------------------- |
| `collect_structure()`         | `structure.py` — pure functions, no API calls   |
| `build_inject_requests()`     | `request_builders.py` — pure functions          |
| `apply_highlight_to_tags()`   | `highlighting.py`                               |
| `cmd_inject_tags()`           | `commands/inject_tags.py`                       |
| `info()` / `emit_result()`    | `output.py` — one place for log/JSON rules      |
| `get_credentials()` etc.      | `services.py` — one place for Google concerns   |
| `parse_args()` at the bottom  | `cli.py` — one place for the CLI shape          |
| The `if __name__ == "__main__"` block | `__main__.py` — makes it `python -m …` |

The toolbox rule: **if you can't describe what a drawer holds in one short
sentence, it's holding too much.** Apply that test to every new module you
create and you'll avoid the "1000-line file" trap on your very next project.

## Tooling: `pyproject.toml` + `Makefile`

Two files sit at the **root of every Python package** and do work that
isn't part of the code itself but is essential for using the package. Both
appear in both examples in this guide (look for `pyproject.toml` and
`Makefile` inside `examples/hello_package/` and `examples/generate_acta_pkg/`).

### `pyproject.toml` — the package's "spec sheet"

`pyproject.toml` (PEP 621) is the modern, declarative way to describe your
package to the rest of the Python world. Before PEP 621 (2020) you had to
write a procedural `setup.py` full of `setup(...)` calls; the new format is
a single TOML file with five sections you'll use 95% of the time:

```toml
[build-system]                              # 1. Who builds this package
requires = ["hatchling >= 1.26"]            #    (a build backend: hatchling,
build-backend = "hatchling.build"           #     setuptools, flit, pdm, …)

[project]                                   # 2. The package itself
name = "hello-package"                      #    distribution name on PyPI
version = "0.1.0"                           #    semver, single source of truth
description = "A 5-line demo package."      #    one-liner shown in search
requires-python = ">=3.9"                   #    minimum supported Python
dependencies = []                           #    runtime deps (google-api,
                                            #    requests, etc. live here)

[project.scripts]                           # 3. CLI entry points
hello = "hello_package.__main__:main"        #    after `pip install`, you get
                                            #    a `hello` command on $PATH

[tool.ruff]                                 # 4. Tool config (linters, formatters,
line-length = 100                            #    test runners, etc.) live under
                                            #    their own [tool.X] section
```

What it does *for you*, in concrete terms:

| Without `pyproject.toml`                | With `pyproject.toml`                        |
| --------------------------------------- | -------------------------------------------- |
| `python script.py` to run it            | `pip install -e .` once, then `hello` works  |
| Dependencies installed by hand          | `pip install .` reads `dependencies = [...]` |
| Version buried in code comments         | `pip show hello-package` shows it            |
| No metadata for tools to discover       | `ruff`, `mypy`, `pytest`, etc. auto-discover |

The build backend (`hatchling` here) is the actual program that turns your
package directory into a wheel (`.whl`) and a source distribution
(`.tar.gz`). You almost never need to switch it; pick one and move on. The
PyPA tutorial in the References section walks through this end-to-end.

### `Makefile` — muscle memory for the long commands

A `Makefile` is the boring, 50-year-old tool that saves you from typing
the same long shell command over and over. Each "target" maps a friendly
name to a shell command:

```makefile
.PHONY: help
help:                       ## Show this help message.
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} \
	     /^[a-zA-Z_-]+:.*##/ \
	       { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' \
	    $(MAKEFILE_LIST)

.PHONY: run
run:                        ## Run the package as a module (equivalent to `python -m`).
	python3 -m hello_package Jefferson

.PHONY: install
install:                    ## Install the package in editable mode.
	python3 -m pip install -e .
```

You invoke it with `make <target>`:

```bash
make help        # list every target with its description
make run         # python -m hello_package Jefferson
make install     # pip install -e .  (one-time setup)
```

The double `##` after a target name is what powers the auto-generated
`help` target — it greps your own `Makefile` for targets with `##` and
prints them. No extra config needed.

### Why bother with both?

You *can* skip them. `python -m hello_package` works without either file.
But the moment you:

- want to **share** the package with a teammate (`pip install .`),
- want to **type** a one-word command instead of a 5-flag CLI invocation
  (`make simulate` vs `python -m generate_acta_pkg generate --field ...`),
- want **linters and formatters** to know your line-length and target
  Python version,

…you'll add both files. They're tiny, they're standard, and they pay for
themselves the first time you use them. Both `examples/hello_package/`
and `examples/generate_acta_pkg/` ship with them — read the hello_package
versions first (40 lines total) and the generate_acta_pkg versions
afterward (the same ideas, plus Google API deps and per-subcommand
targets).

## Examples

### Example #1

The two examples below sit side-by-side in `./examples/`. The first is a
deliberately tiny "hello package" you can read in two minutes. The second is
the real refactor of your `generate_acta.py` script — a working package you
can copy into your project and run today.

#### Quick setup

The smallest possible demonstration of the **package + module + entrypoint**
pattern. Three files, one folder, no dependencies. This is the "if you only
remember three things, remember these" version.

```
examples/
└── hello_package/
    ├── __init__.py      # the nameplate (marks this folder as a package)
    ├── hello.py         # one module with one function
    └── __main__.py      # makes `python -m hello_package` work
```

File contents (copied verbatim into `examples/hello_package/`):

```python
# hello_package/__init__.py
# An empty file is enough to mark this folder as a package.
# You can also expose things here, e.g.: from .hello import greet
__version__ = "0.1.0"
```

```python
# hello_package/hello.py
"""A single module inside the hello_package package."""

def greet(name: str) -> str:
    """Return a friendly greeting for `name`."""
    return f"Hello, {name}! Welcome to your first package."
```

```python
# hello_package/__main__.py
"""Entry point: `python -m hello_package Jefferson`."""
from .hello import greet

def main() -> None:
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "world"
    print(greet(name))

if __name__ == "__main__":
    main()
```

Run it:

```bash
cd examples
python -m hello_package Jefferson
# -> Hello, Jefferson! Welcome to your first package.
```

Three things to notice:

1. **`__init__.py` is the package marker.** Empty is fine.
2. **`__main__.py` lets you run the package as a script.** No `python
   hello_package.py` shenanigans — `python -m <package_name>` is the
   modern, portable way.
3. **Relative imports** (`from .hello import greet`) tie the package's
   internal modules together. Use them inside a package; use absolute
   imports (`from hello_package.hello import greet`) from outside.

#### Complete setup

The full refactor of your `scripts/generate_acta/generate_acta.py` script,
broken into one module per concern. It is **runnable today** in
`--simulate` mode (no Google credentials required), and runs against the
real Google APIs once you wire your `scripts/auth/auth.py` into
`services.py` and set the `ACTA_BASE_DOC_ID` / `ACTA_TARGET_FOLDER_ID`
environment variables.

The package layout (everything under `examples/generate_acta_pkg/`):

```
generate_acta_pkg/
├── __init__.py              # package metadata + re-exports
├── __main__.py              # entry point: `python -m generate_acta_pkg …`
├── cli.py                   # argparse: parser, subcommands, main()
├── config.py                # load + validate the config dict
├── output.py                # info() / emit_result() — single source of truth
├── services.py              # Google auth + service builders
├── structure.py             # walk the doc body (paragraphs, tables, cells)
├── request_builders.py      # build batchUpdate request lists (pure)
├── highlighting.py          # apply + strip highlights (pure)
├── commands/
│   ├── __init__.py
│   ├── inject_tags.py
│   ├── verify_tags.py
│   ├── generate.py
│   ├── fields_cmd.py
│   └── inject_comments.py
├── baseActaReunion/
│   ├── fields.json          # copy of the schema
│   └── sample.json          # copy of the sample config
├── pyproject.toml           # modern packaging metadata (PEP 621)
├── Makefile                 # `make simulate`, `make fields`, etc.
└── README.md                # package-specific instructions
```

Three key snippets that show the wins of the refactor. The first is what
used to be a 20-line `main()` function in the script's tail — now it's its
own tiny module:

```python
# generate_acta_pkg/cli.py
"""Argparse wiring for every subcommand.

Each subcommand lives in its own module under `commands/`. This module's
only job is to declare the CLI shape and dispatch to the right function.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from .commands import inject_tags, verify_tags, generate, fields_cmd, inject_comments

# Top-level defaults pulled from the environment, just like the original script.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_DOC_ID = os.environ.get("ACTA_BASE_DOC_ID", "")
DEFAULT_TARGET_FOLDER_ID = os.environ.get("ACTA_TARGET_FOLDER_ID", "")
DEFAULT_FIELDS_PATH = PROJECT_ROOT / "generate_acta_pkg" / "baseActaReunion" / "fields.json"


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        description="Generate Consejo de Administración Acta from base Google Doc template."
    )
    parser.add_argument("--base-doc-id", default=DEFAULT_BASE_DOC_ID,
                        help="Base doc ID (default: $ACTA_BASE_DOC_ID env var)")
    parser.add_argument("--target-folder-id", default=DEFAULT_TARGET_FOLDER_ID,
                        help="Target Drive folder ID (default: $ACTA_TARGET_FOLDER_ID env var)")
    parser.add_argument("--fields", default=str(DEFAULT_FIELDS_PATH),
                        help="Path to fields.json schema")

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
    """Parse args, dispatch to the chosen subcommand."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
```

The second is the smallest subcommand — `fields` just prints the schema.
Notice how it's a tiny, self-contained module with one public function
`register(parser)`:

```python
# generate_acta_pkg/commands/fields_cmd.py
"""`fields` subcommand: print the fields.json schema."""
from __future__ import annotations

import argparse
import json

from ..config import load_fields, resolve_path


def register(sub: argparse._SubParsersAction) -> None:
    """Attach this subcommand to the top-level parser."""
    p = sub.add_parser("fields", help="Print the field schema")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    """Subcommand body — kept short and side-effect-light."""
    fields_path = resolve_path(args.fields)
    fields_doc = load_fields(fields_path)
    print(json.dumps(fields_doc, indent=2, ensure_ascii=False))
```

The third is the pure-function part of the package — the structural
injector that used to live inline in `cmd_inject_tags()`. Now it takes a
list of "blocks" (already-walked doc structure) and returns a list of
labels and a flat list of API requests. **No Google calls. No prints. No
argparse.** That's what makes it unit-testable:

```python
# generate_acta_pkg/request_builders.py
"""Pure functions that turn walked-doc data into batchUpdate request lists.

Nothing in this module talks to Google. Pass it parsed structure, get back
a list of dicts ready for `documents().batchUpdate(body=...)`. That makes
the whole thing trivially unit-testable with a hand-built `blocks` fixture.
"""
from __future__ import annotations

import re
from typing import Any

# Compile once, reuse forever — module-level regex is the idiomatic place.
ASIST_NOMBRE_RE = re.compile(r"^ASIST_(\d+)_NOMBRE$")


def find_table(blocks: list[dict], table_index: int) -> dict:
    """Return the Nth table block. Raise IndexError if out of range."""
    tables = [b for b in blocks if b["kind"] == "table"]
    if table_index >= len(tables):
        raise IndexError(
            f"table_index {table_index} out of range (only {len(tables)} tables)"
        )
    return tables[table_index]


def count_attendees(cfg: dict) -> int:
    """Return N = highest ASIST_n with a non-empty ASIST_n_NOMBRE in cfg."""
    max_n = 0
    for key, value in cfg.items():
        m = ASIST_NOMBRE_RE.match(key)
        if m and value not in (None, ""):
            max_n = max(max_n, int(m.group(1)))
    return max_n
```

Run the refactored package:

```bash
cd examples
# Validate the package structure is sane:
python -c "import generate_acta_pkg; print(generate_acta_pkg.__version__)"

# No Google creds needed — exercise the full pipeline with a synthetic doc id:
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

# Other subcommands work the same way:
python -m generate_acta_pkg fields
python -m generate_acta_pkg verify-tags --simulate    # verify-tags only simulates
                                                     # when --base-doc-id is also set
python -m generate_acta_pkg inject-tags --simulate
python -m generate_acta_pkg inject-comments --simulate --yes
```

The full file contents of every module are in `examples/generate_acta_pkg/`.
Read them top-to-bottom — the order matches the order the original script
does its work, so you can map old → new one chunk at a time.

## Research

### Reference URLs

- https://docs.python-guide.org/writing/structure/ — The Hitchhiker's Guide to Python: the chapter that started this. Covers modules vs packages, `__init__.py` semantics, and the canonical sample repository layout (Kenneth Reitz's `samplemod`).
- https://docs.python.org/3/tutorial/modules.html — Official Python tutorial §6: "Modules". Definitive reference for how `import` works, the role of `__init__.py`, and intra-package relative imports.
- https://docs.python.org/3/howto/argparse.html — Official argparse tutorial. The right mental model for subcommands, mutually exclusive groups, `action="store_true"`, and `type=` converters.
- https://packaging.python.org/en/latest/tutorials/packaging-projects/ — PyPA's canonical packaging tutorial using `pyproject.toml` + Hatchling/Setuptools. Walks through the modern way to make a package installable.
- https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/ — `src/` layout vs flat layout: when and why to put your import package under a `src/` directory. Directly relevant if you decide to publish or test this package in CI.
- https://docs.python.org/3/tutorial/venv.html — Virtual environments with `python -m venv`. The non-negotiable habit for any Python project that has dependencies.
- https://realpython.com/python-application-layouts/ — Real Python's layout reference: one-off script → single package → multi-package app. Great for visualizing how a project grows in stages.

## Next steps

Once you've read the modules in `examples/generate_acta_pkg/` and run
`python -m generate_acta_pkg generate --simulate …`, three concrete
follow-ups will lock in what you've learned:

1. **Add a unit test.** Pick one module — `request_builders.py` is the
   easiest because it's pure functions — and write a `tests/` folder with
   one pytest test. The whole point of the refactor was making things
   testable; prove it. The Real Python layout reference linked above shows
   where `tests/` should sit.
2. **Wire your real `auth.py` into `services.py`.** Right now
   `services.py` exposes a single `get_credentials()` that you point at
   the existing `scripts/auth/auth.py` from your repo. That single import
   is the bridge between this package and the rest of your project.
3. **Read PEP 8 and run a linter.** PEP 8 is short (one page) and gives you
   the style rules Pythonistas actually follow. Then run `ruff check` (or
   `flake8`) on the package — it'll flag a handful of small things
   (mostly whitespace and line length) and you'll absorb them by
   repetition.
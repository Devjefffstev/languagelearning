"""Subcommand package — one module per subcommand.

Every subcommand module exports the same two things:
    def register(sub: argparse._SubParsersAction) -> None: ...
    def run(args: argparse.Namespace) -> None: ...

`register` attaches the subparser and sets `func=run` on it. `cli.main()`
calls `args.func(args)` to dispatch.

The subpackages/ directory convention: put related-but-distinct entry
points in their own folder so you don't end up with 30 .py files at the
top level of your package. (See Real Python's "Application with Internal
Packages" layout for the same idea at a larger scale.)
"""
# Re-export the subcommand register functions so `cli.py` only has to
# import this package, not every individual module.
from . import fields_cmd, generate, inject_comments, inject_tags, verify_tags  # noqa: F401

__all__ = [
    "fields_cmd",
    "generate",
    "inject_comments",
    "inject_tags",
    "verify_tags",
]
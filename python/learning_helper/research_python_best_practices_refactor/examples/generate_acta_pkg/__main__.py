"""Entry point: `python -m generate_acta_pkg …`.

This module is intentionally tiny — its only job is to hand control to
`cli.main()`. Putting the entry point in `__main__.py` (instead of at the
bottom of a single big script) is the pattern that lets you both import
the package as a library and run it as a command.
"""
from .cli import main

if __name__ == "__main__":
    main()
"""Entry point for `python -m hello_package [name]`.

The presence of `__main__.py` in a package makes the package directly runnable
via `python -m <package_name>`. Without it, you can only import the package;
you can't "execute" it. This is the modern, portable replacement for the
old `python some_script.py` habit.
"""
from .hello import greet


def main() -> None:
    """Parse argv, call `greet`, print the result.

    Notice `from .hello import greet` — that leading dot means "import from
    the same package." This is a *relative import* and it's the right tool
    when one module inside a package needs another module in the same
    package. For cross-package imports, use absolute imports:
        from hello_package.hello import greet
    """
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "world"
    print(greet(name))


# This idiom (`if __name__ == "__main__":`) means:
# "Only run `main()` if this file is being executed directly (e.g.
#  `python -m hello_package`), not just imported (`import hello_package`)."
# It's what lets the same file be both a runnable script and a reusable module.
if __name__ == "__main__":
    main()
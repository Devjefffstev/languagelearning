"""A single module inside the hello_package package.

The leading docstring is what `help(hello_package.hello)` shows you — keep it
short and to the point. Module-level docstrings follow PEP 257.
"""


def greet(name: str) -> str:
    """Return a friendly greeting for `name`.

    This is a *type-hinted* function: `name: str` declares the expected input
    type, `-> str` declares the return type. Type hints are optional in
    Python, but they make every function self-documenting and let editors
    give you better autocomplete and error checking.
    """
    return f"Hello, {name}! Welcome to your first package."
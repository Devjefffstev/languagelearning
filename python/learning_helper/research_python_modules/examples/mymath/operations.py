# mymath/operations.py — submodule of the mymath package.

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def _internal_helper():
    # Not exported by __all__; underscore signals "private".
    return "not part of the public API"
# mymath/__init__.py
# Marks this directory as a regular Python package and decides
# what `from mymath import *` will expose.

from .operations import add, multiply           # relative import: same package
from .stats.basic import mean                   # relative import: into a subpackage's submodule

__all__ = ["add", "multiply", "mean", "VERSION"]  # explicit public API

# A package-level constant — reachable as mymath.VERSION
VERSION = "1.0"
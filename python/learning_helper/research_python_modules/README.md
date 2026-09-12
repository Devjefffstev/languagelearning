# Python Modules

## Description

A Python **module** is simply a `.py` file containing definitions (functions, classes, variables) and statements. Modules are how you organize code into reusable, named units that can be imported by other modules, scripts, or interactive sessions. The official Python tutorial puts it this way: "a module is a file containing Python definitions and statements. The file name is the module name with the suffix `.py` appended."

When you write a program longer than a screenful, you stop putting everything in one file. You split definitions into several files, give each a descriptive name, and `import` what you need where you need it. The import system is the backbone that turns a pile of `.py` files into a working program — it locates the right file, executes it once, gives you a module object with its own namespace, and caches it in `sys.modules` so it isn't re-run on subsequent imports.

A **package** is the next level up: a directory of modules grouped under a common name. Python recognizes a directory as a package when it contains an `__init__.py` file (called a *regular package* — namespace packages without `__init__.py` also exist, added in Python 3.3). Packages let you carve a large project into a hierarchy with dotted names like `sound.effects.echo` and control what `from package import *` exposes via the `__all__` list.

The core mental model is simple: every `.py` file is a module, every directory with `__init__.py` is a package, and `import` is the verb that ties them together. Master those three concepts and the rest of the import system (search path, relative imports, `if __name__ == '__main__':`, `dir()`, `__all__`, `importlib.reload()`) is just refinement on the same theme.

## Analogy

Think of Python's module system as a **kitchen recipe box**.

- A **module** is a single recipe card — a focused, named set of instructions you can pull out and use on its own.
- A **package** is the recipe box itself, organized with dividers (subpackages like `effects/` and `formats/`) and labeled with a title page (`__init__.py`) that says "yes, this is a recognized section."
- The `import` statement is you asking the chef: "Bring me the chocolate-cake recipe from the desserts section." The chef doesn't photocopy the whole box — they hand you just the one card you asked for.
- `sys.path` is the chef's lookup list: first check the recipe box on the counter (the script's directory), then look in the other boxes on the shelf (`PYTHONPATH`), then fall back to the master library in the back of the kitchen (the standard library).
- `if __name__ == "__main__":` is the note at the bottom of the recipe card: "Run this card by itself as a test batch when nobody's importing it." When the chef pulls the card to use a single ingredient, that note is ignored — but if you hand the card directly to the oven as the day's main recipe, the note kicks in.

Just as a chef wouldn't photocopy the entire recipe book into every dish, Python runs each module exactly once and reuses the cached result. And just as a well-organized recipe box keeps desserts from clashing with main courses, packages keep related modules grouped without name collisions.

## Examples

### Example #1

#### Quick setup

Two files in the same directory. The first defines a module; the second imports from it.

**File `greet.py`:**

```python
# greet.py — a tiny module with one public function.
# Anything not starting with an underscore is considered public.

def greet(name):
    """Return a friendly greeting."""
    return f"Hello, {name}! Welcome to modules."

def _secret():
    """Leading underscore signals 'internal use only'."""
    return "ssssh"
```

**File `app.py`:**

```python
# app.py — the script that uses the greet module.
# Run with: python app.py

import greet                # 1) bind the module itself
from greet import greet     # 2) pull one name into our namespace directly

print(greet.greet("Ada"))   # use the module attribute (form 1)
print(greet("Ada"))         # use the imported function (form 2)
print("module name is:", greet.__name__)
```

Run it:

```bash
python app.py
```

Expected output:

```
Hello, Ada! Welcome to modules.
Hello, Ada! Welcome to modules.
module name is: greet
```

#### Complete setup

A small package that demonstrates regular-package mechanics, dotted names, `__init__.py`, `__all__`, and absolute vs relative imports.

**Project layout:**

```
mymath/
├── __init__.py
├── operations.py
└── stats/
    ├── __init__.py
    └── basic.py
main.py
```

**File `mymath/__init__.py`:**

```python
# mymath/__init__.py
# Marks this directory as a regular Python package and decides
# what `from mymath import *` will expose.

from .operations import add, multiply           # relative import: same package
from .stats.basic import mean                   # relative import: into a subpackage's submodule

__all__ = ["add", "multiply", "mean", "VERSION"]  # explicit public API

# A package-level constant — reachable as mymath.VERSION
VERSION = "1.0"
```

**File `mymath/operations.py`:**

```python
# mymath/operations.py — submodule of the mymath package.

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def _internal_helper():
    # Not exported by __all__; underscore signals "private".
    return "not part of the public API"
```

**File `mymath/stats/__init__.py`:**

```python
# mymath/stats/__init__.py — empty is fine; just marks the subpackage.
```

**File `mymath/stats/basic.py`:**

```python
# mymath/stats/basic.py — lives inside a subpackage.

def mean(numbers):
    return sum(numbers) / len(numbers)
```

**File `main.py`:**

```python
# main.py — uses the mymath package.
# Run from the directory containing `mymath/` and `main.py`.

# Three equivalent ways to reach the same function:

# 1) Absolute import, full dotted path
from mymath.stats.basic import mean
print("mean([1,2,3,4]) =", mean([1, 2, 3, 4]))

# 2) Absolute import, shorter form (because mymath/__init__.py re-exports mean)
from mymath import mean as avg
print("avg([10, 20, 30]) =", avg([10, 20, 30]))

# 3) Importing the package and reaching in via attribute
import mymath
print("mymath.add(2, 3) =", mymath.add(2, 3))
print("mymath.multiply(4, 5) =", mymath.multiply(4, 5))
print("mymath.VERSION =", mymath.VERSION)
```

Run it:

```bash
python main.py
```

Expected output:

```
mean([1,2,3,4]) = 2.5
avg([10, 20, 30]) = 20.0
mymath.add(2, 3) = 5
mymath.multiply(4, 5) = 20
mymath.VERSION = 1.0
```

What this exercise demonstrates:

- The directory `mymath/` becomes a package the moment it contains `__init__.py`.
- `mymath/stats/` is a *subpackage* — a package nested inside another.
- The `__all__` list controls what `from mymath import *` exposes (here: `add`, `multiply`, `mean`, `VERSION`).
- A leading dot in `from .operations import ...` is a **relative import**: "from the package I'm currently in."
- Once `mymath/__init__.py` imports `mean`, `import mymath` makes `mean` reachable as `mymath.mean` — but only because someone re-exported it.

## Exercises

These build from a single module up to a small multi-file package. Each one reinforces a concept from the description.

- `exercises/01_single_module/` — Create `greeter.py` with a `greet(name)` function and `main.py` that imports it three different ways. (Easy — reinforces the basic `import` vs `from ... import` distinction plus the `as` alias.)
- `exercises/02_module_search_path/` — Print `sys.path`, then dynamically add a directory and import a module from it. (Medium — reinforces the module search path and `sys.path` mutability.)
- `exercises/03_main_guard/` — Make a module that works both as a runnable script and as an importable library using `if __name__ == "__main__":`. (Medium — reinforces the `__name__` global and command-line arguments.)
- `exercises/04_package/` — Build a `shapes/` package with `__init__.py`, an `__all__` list, two submodules, and a main script that uses both `from shapes import *` and a direct submodule import. (Hard — reinforces packages, dotted names, `__all__`, and intra-package references.)

## Research

### Reference URLs

- https://docs.python.org/3/tutorial/modules.html — The official Python Tutorial chapter that this guide follows section-by-section; covers modules, packages, the search path, `dir()`, `__all__`, and intra-package references.
- https://docs.python.org/3/reference/import.html — The language reference for the full import system: finders, loaders, `sys.modules`, `sys.meta_path`, package relative imports, and the `__main__` module's special handling.
- https://docs.python.org/3/library/importlib.html — The `importlib` package, which exposes the import machinery as a public API: `import_module()`, `reload()`, finder/loader ABCs, and `ModuleSpec`.
- https://docs.python.org/3/library/sys_path_init.html — Exactly how `sys.path` is initialized at startup: the script directory, `PYTHONPATH`, `PYTHONHOME`, virtual environments, `.pth` files, and the `site` module.
- https://peps.python.org/pep-0328/ — PEP 328, the original rationale and BDFL decision on absolute-by-default imports and leading-dot relative imports inside packages.

Last verified: 2026-09-03.

## Next steps

When you're comfortable with the material in this guide, go deeper with:

- **`importlib`** for programmatic imports — `importlib.import_module('pkg.mod')` is the recommended way to import by string, and `importlib.reload(module)` lets you re-execute a module in a long-running session without restarting.
- **Packaging for distribution** — once your `mymath` package works locally, the next step is making it installable with `pyproject.toml` and uploading it to PyPI. Read the [Python Packaging User Guide](https://packaging.python.org/).
- **Virtual environments** — when you start juggling multiple projects with conflicting dependencies, `python -m venv .venv` plus `PYTHONPATH`-aware tools become essential; the [venv module docs](https://docs.python.org/3/library/venv.html) are the starting point.

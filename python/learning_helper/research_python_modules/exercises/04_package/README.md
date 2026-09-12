# Exercise 04 — Build a Package

## Goal

Build a regular Python package with submodules, an `__init__.py` that exposes an `__all__` list, and use both `from package import *` and a direct submodule import to access the package's contents.

## Task

Build the following layout inside this folder (create `shapes/` as a subdirectory):

```
shapes/
    __init__.py
    circle.py
    square.py
main.py
```

Requirements:

- `shapes/circle.py` defines `area(r)` that returns `3.14159 * r * r`.
- `shapes/square.py` defines `area(s)` that returns `s * s`.
- `shapes/__init__.py` sets `__all__ = ["circle", "square"]`. (Optionally re-export the submodules so `import shapes; shapes.circle` also works.)
- `main.py`:
  - Uses `from shapes import *` then prints `circle.area(2)` and `square.area(3)`.
  - Uses an absolute import `from shapes.circle import area as circle_area` and prints `circle_area(5)`.
  - Imports `shapes` and prints `shapes.square.area(4)`.

## Hints

- A directory becomes a regular Python package the moment you put an `__init__.py` inside it — even an empty one.
- `from package import *` only imports the names listed in `package/__init__.py`'s `__all__`. If `__all__` is missing, Python imports whatever names `__init__.py` itself defined (not the submodules).
- Putting `__all__ = ["circle", "square"]` in `shapes/__init__.py` means `from shapes import *` brings the **submodule names** `circle` and `square` into your namespace — so you call `circle.area(...)`, not just `area(...)`.
- The starter files have `TODO` markers at every spot where you need to fill in code.

## Success criteria

Running `python main.py` prints, in order:

```
12.56636
9
78.53975
12.56636
```

with no `ImportError`. The first line comes from `circle.area(2)`, the second from `square.area(3)`, the third from `circle_area(5)` (5² × π ≈ 78.53975), and the fourth from `shapes.square.area(4)`.

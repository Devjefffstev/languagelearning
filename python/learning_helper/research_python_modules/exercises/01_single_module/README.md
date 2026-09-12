# Exercise 01 — Single Module

## Goal

Create a Python module in one file and import it from another file using two different `import` styles.

## Task

Create two files inside this folder:

1. `greeter.py` — defines a function `greet(name)` that returns the string `"Hello, {name}!"`.
2. `main.py` — uses the module in **three** different ways:
   - `import greeter` then call `greeter.greet("World")`
   - `from greeter import greet` then call `greet("Python")`
   - `import greeter as g` then call `g.greet("Modules")`

Each call should print a different greeting so you can see all three styles worked.

## Hints

- The "More on Modules" section of the tutorial walks through `import x`, `from x import y`, and `import x as y` — they all bind different names into your namespace, but the module is loaded only once.
- Module attributes are reached with the dot operator: `module.attribute`.
- The `as` keyword renames the binding in *your* namespace; it doesn't change the module object itself.
- The starter files have `TODO` markers where you need to fill in code.

## Success criteria

Running `python main.py` prints exactly three greeting lines — one to `"World"`, one to `"Python"`, one to `"Modules"` — with no `NameError` or `ImportError`.

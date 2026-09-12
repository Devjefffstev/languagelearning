# Exercise 02 — Module Search Path

## Goal

Understand how Python finds a module when you `import` it, and practice extending `sys.path` so a module becomes importable from a directory that wasn't on the path initially.

## Task

Write a single `main.py` that does the following, in order:

1. Print the current contents of `sys.path` (one item per line is easiest to read).
2. Choose a directory not currently on `sys.path` (a fresh temp directory works well — e.g. `pathlib.Path("/tmp/mods_demo")`). Make sure it exists.
3. Write a small file inside that directory called `hidden.py` that defines one function, `ping()`, which returns the string `"pong from <absolute-path-of-hidden.py>"`.
4. Append that directory to `sys.path` with `sys.path.append(...)`.
5. `import hidden` and call `hidden.ping()`, then print the result.
6. After importing, print `hidden.__file__` and `hidden.__name__` so you can see where Python found the module.

## Hints

- `sys.path` is a regular Python list — `print(sys.path)` shows it, `.append()` extends it, and Python re-searches it every time an `import` runs.
- The first entry of `sys.path` is usually the directory containing the script being run; entries after that come from `PYTHONPATH` and the standard library.
- `pathlib.Path.mkdir(parents=True, exist_ok=True)` creates a directory tree without erroring if it already exists.
- `pathlib.Path.write_text(...)` is the simplest way to create a small text file from Python code.
- The starter file has `TODO` markers for each numbered step.

## Success criteria

Running `python main.py` ends with the line `pong from /tmp/mods_demo/hidden.py` (or whatever absolute path you chose), and prints both `hidden.__file__` and `hidden.__name__` — proving Python found and imported the dynamically-added module without a `ModuleNotFoundError`.

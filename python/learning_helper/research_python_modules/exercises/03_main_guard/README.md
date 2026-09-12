# Exercise 03 — The `__name__ == "__main__"` Guard

## Goal

Write a module that is both **importable as a library** and **runnable as a script**, using the `if __name__ == "__main__":` idiom so the script-only behavior never fires on import.

## Task

Create two files in this folder:

1. `greeter.py` — defines:
   - `greet(name)` returning `"Hello, {name}!"`
   - A `if __name__ == "__main__":` block that reads a name from `sys.argv[1]` (with a default like `"World"` if no argument is given), calls `greet(name)`, and prints the result.
2. `main.py` — imports `greet` from `greeter` and calls it directly with `"Imported"` so you can prove the guard block did **not** run during import.

## Hints

- `__name__` is a string the runtime sets automatically. It's `"__main__"` only when the file is executed directly (e.g. `python greeter.py`), and the module's filename (e.g. `"greeter"`) when imported by another file.
- `sys.argv` is a list; `sys.argv[0]` is the script name, and the first user-supplied argument is `sys.argv[1]`. Use `len(sys.argv) > 1` to check whether an argument was passed.
- A common one-liner for a default: `name = sys.argv[1] if len(sys.argv) > 1 else "World"`.
- The starter file `greeter.py` has `TODO` markers in three places: the `greet` body, the guard block, and the command-line parsing.
- The starter file `main.py` has one `TODO` for the import + call.

## Success criteria

- `python greeter.py Ada` prints `Hello, Ada!`.
- `python greeter.py` (no argument) prints `Hello, World!`.
- `python -c "import greeter"` produces **no** greeting output (the guard did not fire).
- `python main.py` prints `Hello, Imported!` from the direct call, and produces **no** extra greeting from the guard.

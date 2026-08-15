# Exercise 02 — Swap and Unpack

## Goal

Get fluent with **tuple unpacking** and the `a, b = b, a` swap idiom —
two of the most-used variable patterns in Python.

## Task

Open `starter.py`. It defines three small sub-tasks, each marked with
a `TODO`. Implement them in order:

1. **`swap(a, b)`** — return `a` and `b` with their values exchanged,
   using **one line** that relies on tuple unpacking. Don't use a temp
   variable.

2. **`first_and_rest(items)`** — given a list of at least one element,
   return a tuple `(first, rest)` where `first` is the first element
   and `rest` is everything else as a new list. Hint: this is also
   one line using tuple unpacking with a starred target.

3. **`rotate_three(x, y, z)`** — return `(y, z, x)` — the three values
   shifted left. Again, one line using tuple unpacking.

The file's `main()` calls each function with sample inputs and prints
the result so you can sanity-check your work.

## Hints

1. The Python language reference says: *"the right-hand side expressions
   are all evaluated first before any of the assignments take place."*
   That guarantee is what makes `a, b = b, a` work without a temp
   variable — both `b` and `a` are read first, *then* the swap happens.
2. For `first_and_rest`, the starred-target syntax is `first, *rest = items`.
   Python will put the first item into `first` and the rest (possibly
   an empty list) into `rest`. This works for any iterable, not just lists.
3. For `rotate_three`, just bind the three parameters to three new names
   in the rotated order. The `return` line itself can be the swap.
4. If a function returns `(a, b)` and the caller writes
   `x, y = swap(...)`, the caller's `x` and `y` get the two values
   individually — that's the unpacking on the receiving side.

## Success criteria

- `python3 starter.py` runs without errors and prints:
  - `swap(1, 2) -> (2, 1)`
  - `swap("a", "b") -> ('b', 'a')`
  - `first_and_rest([10, 20, 30, 40]) -> (10, [20, 30, 40])`
  - `first_and_rest([7]) -> (7, [])`
  - `rotate_three(1, 2, 3) -> (2, 3, 1)`
  - `rotate_three("a", "b", "c") -> ('b', 'c', 'a')`
- Each function is **one line of code in its body** (the `def ...:` line
  doesn't count).
- No temporary variables — everything is tuple unpacking.

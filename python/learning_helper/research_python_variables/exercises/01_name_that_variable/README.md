# Exercise 01 — Name That Variable

## Goal

Train your eye for **legal vs illegal** and **idiomatic vs non-idiomatic**
Python variable names. No logic to write — just classify and rewrite.

## Task

Open `starter.py`. It contains a list of variable names, every one of
which has a problem. For each name in the list:

1. Decide whether it's **illegal** (won't even parse) or just
   **non-idiomatic** (parses fine, but violates Python conventions).
2. If illegal, write the `SyntaxError` message Python would produce.
3. Rewrite each name as a legal, idiomatic alternative that describes
   what the variable is *for*, not what it *is*.

`starter.py` is set up so you fill in two parallel lists:

- `PROBLEMS` — your one-line diagnosis for each bad name.
- `FIXED`    — your replacement name.

When you run the file, it prints your answers next to the originals so
you can review them.

## Hints

1. There are exactly **8 names** to fix. Some are illegal (Python
   refuses to even run them); the rest are legal but bad style.
2. The legal-but-bad ones violate at least one PEP 8 rule from the
   *Naming Conventions* section: snake_case for variables, descriptive
   names, avoid single letters that look like digits (`l`, `O`, `I`).
3. Two of the names are illegal because they **start with a digit**.
   One is illegal because it's a **Python keyword**. One is illegal
   because of an **invalid character**. That accounts for the four
   illegal ones — the other four are legal but should still be renamed.
4. The replacement names should describe what the value *represents*
   (e.g. `max_retries` is better than `n`). When in doubt, pretend
   you're naming it for a teammate who has never seen your code.

## Success criteria

- `python3 starter.py` prints **8 lines**, each in the form
  `original -> diagnosis -> fixed`.
- Every `fixed` name is **legal Python** (no `SyntaxError`).
- Every `fixed` name follows **PEP 8 snake_case** and is
  **descriptive** (not `x`, `n`, `tmp`).
- You can explain, in one sentence per line, *why* the original was
  illegal or non-idiomatic.

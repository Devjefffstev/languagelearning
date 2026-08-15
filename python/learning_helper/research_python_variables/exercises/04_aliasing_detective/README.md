# Exercise 04 — Aliasing Detective

## Goal

Build intuition for the **aliasing** and **`is` vs `==`** traps. You'll
read six short snippets, **predict the output before you run**, then
run them to check yourself. Finally, you'll fix two real-world aliasing
bugs.

## Task

Open `starter.py`. It contains:

- **Part A — Predict the output.** Six snippets, each ending with a
  `print(...)`. Read each one, write your predicted output in the
  `PREDICTIONS` list (one line per snippet), then run the file. The
  runner reveals which predictions you got right.

- **Part B — Fix two aliasing bugs.** Two functions
  (`strip_nicknames` and `add_to_each`) have subtle bugs because their
  callers assumed an assignment was a copy. Fix them without changing
  what the program is supposed to *do* — only the *mechanics*.

## Hints

1. For Part A, work snippet-by-snippet on paper before touching the
   computer. Ask yourself, for each snippet: "are the two names stuck
   on the same object, or on different objects with the same value?".
2. Snippet 2 is the canonical aliasing trap: `b = a` puts two sticky
   notes on one jar. `b.append(...)` changes the jar, so `a` sees the
   change too.
3. Snippet 3 shows that for **integers**, `b = a; b += 1` does NOT
   mutate `a`. Integers are immutable, so `+=` rebinds `b` to a new
   int. (Compare to snippet 2 where the list `+=` can mutate in place.)
4. Snippet 5 is the `is` vs `==` check for `None`. PEP 8 says: *"Comparisons
   to singletons like None should always be done with is or is not,
   never the equality operators."* This snippet demonstrates *why* —
   `is` is faster and avoids the trap of an `__eq__` that lies.
5. For Part B, `strip_nicknames` receives a list from the caller and
   mutates it via `.pop()`. The caller doesn't expect the original list
   to shrink — it expected a *new* list. The fix is to not mutate the
   caller's list; build a new one and return it.
6. For `add_to_each`, the aliasing is sneakier: `total = 0` inside the
   loop is fine on its own, but the function is supposed to *return*
   the running total. Read what the function currently does vs what its
   docstring says — the bug is in what gets returned.

## Success criteria

- Part A: all six of your `PREDICTIONS` strings exactly match what the
  snippet actually prints. (The runner tells you which ones matched.)
- Part B:
  - `strip_nicknames(["alice", "bob", "carol"], {"bob"})` returns
    `["alice", "carol"]` **and** leaves the caller's original list
    unchanged.
  - `add_to_each([1, 2, 3])` returns `6`, and the caller's list is
    unchanged.
- You can explain in one sentence per snippet why your prediction was
  right (or what surprised you).

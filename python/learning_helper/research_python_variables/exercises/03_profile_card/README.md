# Exercise 03 — Profile Card

## Goal

Re-implement a smaller version of `examples/profile_card.py` from
scratch, this time writing every variable yourself. Practices **type
hints on variables**, **constants by convention**, **augmented
assignment** (`+=`), and the **mutable-list-as-accumulator** pattern.

## Task

Open `starter.py`. It defines the skeleton of a "stats card" program
that takes a player's name, level, and a series of score gains, then
prints a summary. Implement the four `TODO` blocks.

The four pieces, in order:

1. **Define two module-level "constants"** at the top of the file:
   - `MAX_LEVEL: int = 99`  — the cap on the level field.
   - `DEFAULT_NAME: str = "Anonymous"` — used when the player enters
     a blank name.

2. **In `clamp_level(level)`**, return `level` clamped to the range
   `[1, MAX_LEVEL]`. Use augmented assignment or `min`/`max` — your call.

3. **In `record_gain(scores, amount)`**, append `amount` to the
   `scores` list **only if** it is positive (greater than zero). The
   list should grow in place — no `return` value needed.

4. **In `build_summary(name, level, scores)`**, return a multi-line
   string using an f-string. Format:
   ```
   Player: <name>
   Level : <level>
   Score : <total>  (<count> gains)
   ```
   where `<total>` is the sum of `scores` and `<count>` is
   `len(scores)`.

   If `scores` is empty, `<total>` should print as `0` and the
   parenthetical should read `(0 gains)` — singular vs plural is up
   to you, but be consistent.

The `main()` function is already written — it prompts for the name,
level, and a stream of score gains (blank line to stop), then prints
your summary. You only fill in the four TODOs.

## Hints

1. Constants with type hints look like `MAX_LEVEL: int = 99` — name,
   colon, type, equals, value. PEP 526 added this syntax. They behave
   like any other variable at runtime; the uppercase is the convention.
2. `clamp_level` has two cases to handle: `level < 1` and
   `level > MAX_LEVEL`. The cleanest one-liner is `return max(1, min(level, MAX_LEVEL))`.
   Think about *why* `min` is on the inside.
3. For `record_gain`, the only check is `if amount > 0: scores.append(amount)`.
   The function doesn't need to return anything because lists are mutable —
   the caller's `scores` is the same object as this function's `scores`.
4. For the summary, f-strings can embed any expression: `len(scores)`,
   `sum(scores)`, and a conditional like `f"{n} gain{'s' if n != 1 else ''}"`
   for the plural are all valid inside `{}`.

## Success criteria

- `python3 starter.py` runs without errors.
- Entering `ada`, level `5`, and gains `10`, `20`, `-5`, `15` (blank to
  stop) prints:
  ```
  Player: Ada
  Level : 5
  Score : 45  (3 gains)
  ```
  (note that `-5` was filtered out — only positive gains count).
- Entering a blank name uses `DEFAULT_NAME` instead of crashing.
- Entering a level of `9999` is clamped down to `99`.
- Entering a level of `-3` is clamped up to `1`.
- You can point to each line you wrote and say which of the four
  foundations it demonstrates (assignment, dynamic typing, naming,
  mutability, etc.).

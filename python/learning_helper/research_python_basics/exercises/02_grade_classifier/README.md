# Exercise 02 — Grade Classifier

## Goal

Take a numeric score from the user (0–100) and turn it into a letter grade,
with input validation.

## Task

Write a script that:

1. Asks the user for a score between **0 and 100** (inclusive).
2. Rejects scores outside that range with a friendly error message.
3. Rejects non-numeric input with a friendly error message.
4. Classifies the score using the standard US scale:
   - `90–100` → `A`
   - `80–89`  → `B`
   - `70–79`  → `C`
   - `60–69`  → `D`
   - `0–59`   → `F`
5. Prints the score and its letter grade on one line, e.g.
   `Score 87 -> B`.

Use an `if / elif / else` chain. Put the classification in a function called
`classify(score: int) -> str`.

A skeleton is provided in `starter.py`.

## Hints

1. `int(s)` will raise `ValueError` if `s` is not a whole number. Catch it
   with `try: ... except ValueError:`.
2. Once you have an integer, the check `0 <= score <= 100` is the
   Pythonic way to test "is the score in range?" — you don't need `and`.
3. The natural order for an `if / elif / else` chain is from the highest
   bracket down. Otherwise `score >= 60` would catch everything that
   should be a B.
4. The last `else` of an `if/elif/else` chain is your "unreachable" safety
   net — you can have it return `"?"` or raise an exception.

## Success criteria

Running `python3 starter.py`:

| Input    | Output                  |
|----------|-------------------------|
| `87`     | `Score 87 -> B`         |
| `95`     | `Score 95 -> A`         |
| `59`     | `Score 59 -> F`         |
| `60`     | `Score 60 -> D`         |
| `-5`     | error, no letter grade  |
| `150`    | error, no letter grade  |
| `hello`  | error, no traceback     |

## Stretch goals (optional)

- Add a `+`/`-` modifier: 90–93 is `A-`, 94–96 is `A`, 97–100 is `A+`
  (and the same idea for B/C/D).
- Round half-values (`88.5`) — but be careful, since your input is now
  a float, not an int.
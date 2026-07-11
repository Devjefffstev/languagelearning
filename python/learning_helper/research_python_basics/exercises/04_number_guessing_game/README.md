# Exercise 04 — Number Guessing Game

## Goal

Build a small command-line game where the program picks a secret number and
the player has to guess it, with hints and an attempt counter.

## Task

Write a script that:

1. Picks a random integer between **1 and 100** (inclusive) at the start
   of each game, using the `random` module.
2. Greets the player and explains the rules in one or two lines.
3. Loops, asking for a guess each turn:
   - If the guess is **too low**, print `Higher!`.
   - If the guess is **too high**, print `Lower!`.
   - If the guess is correct, print a congratulations that includes the
     **number of attempts** it took, then exit the loop.
4. Rejects guesses that aren't whole numbers, with a friendly error
   message that does **not** count as an attempt.
5. (Optional polish) allows the player to type `quit` to give up early.

Use a `while` loop and `break` to exit. Put the random-target selection in
a function called `pick_target()` and the comparison logic in a function
called `check_guess(guess: int, target: int) -> str` (returning one of
`"higher"`, `"lower"`, `"correct"`).

## Hints

1. `import random` at the top of the file, then `random.randint(1, 100)`
   gives you a random integer in `[1, 100]` inclusive.
2. `int(s)` raises `ValueError` if `s` isn't a whole number. Wrap your
   `input()` → `int()` conversion in `try: ... except ValueError:` and
   `continue` the loop on failure.
3. The natural shape is:
   ```python
   while True:
       guess = ...             # read input
       result = check_guess(...)  # "higher" / "lower" / "correct"
       if result == "correct":
           break
       print("Higher!" if result == "higher" else "Lower!")
   ```
   A common trick is `if/elif/else` inside the loop body instead of a
   dict-lookup; both are fine.
4. Count attempts with a counter that you `+= 1` *only* when the input
   was valid.

## Success criteria

Running `python3 starter.py`:

- Picks a new secret number each run (you can verify by adding
  `print(target)` temporarily — just remove it before you're done).
- Prompts the player, accepts guesses, prints `Higher!` or `Lower!`, and
  eventually prints a winning line that includes the attempt count.
- Typing `abc` prints a polite error and re-prompts without counting the
  attempt.

A typical winning interaction looks like:

```
I'm thinking of a number between 1 and 100.
Your guess? 50
Higher!
Your guess? 75
Lower!
Your guess? 62
You got it in 3 attempts!
```

## Stretch goals (optional)

- After the game ends, ask `Play again? (y/n)` and restart with a fresh
  number.
- Add a difficulty mode: `easy` is 1–50, `hard` is 1–1000, `insane` is
  1–10000. Bigger ranges are harder because binary search gives you about
  `log2(N)` attempts — see if you can hit it in 7 when `N == 100`.
- Track and print the **personal best** (lowest attempt count) across
  games in the same session.
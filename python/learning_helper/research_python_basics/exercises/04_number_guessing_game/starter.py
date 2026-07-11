"""Starter for Exercise 04 — Number Guessing Game.

Fill in the TODO sections. Run with: python3 starter.py
"""

import random


def pick_target(low: int = 1, high: int = 100) -> int:
    """TODO: return a random integer in [low, high] inclusive."""
    pass


def check_guess(guess: int, target: int) -> str:
    """TODO: return one of 'higher', 'lower', or 'correct'."""
    pass


def main() -> None:
    target = pick_target()
    attempts = 0

    print("I'm thinking of a number between 1 and 100.")

    # TODO: loop forever (while True). Inside the loop:
    #   1) read input and try to convert it to int; on ValueError, print
    #      a friendly message and `continue` WITHOUT incrementing attempts.
    #   2) increment `attempts` once the guess is valid.
    #   3) call check_guess(guess, target); on 'correct', break out of the
    #      loop after printing a winning line that includes `attempts`.


if __name__ == "__main__":
    main()
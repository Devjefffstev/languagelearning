"""Starter for Exercise 04 — Number Guessing Game.

Fill in the TODO sections. Run with: python3 starter.py
"""

import random


def pick_target(low: int = 1, high: int = 100) -> int:
    """TODO: return a random integer in [low, high] inclusive."""
    return random.randint(low, high)


def check_guess(guess: int, target: int) -> str:
    """TODO: return one of 'higher', 'lower', or 'correct'."""
    return "higher" if guess < target else "lower" if guess > target else "correct"


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
    while True: 
        try:
            guess = int(input("Enter your guess: "))            
        except ValueError:
            print("Please enter a valid integer.")
            continue    
        attempts += 1
        result = check_guess(guess, target)
        if result == "correct":
            print(f"Correct! You guessed it in {attempts} attempts.")
            break
        elif result == "higher":
            print("Try higher.")
        else:
            print("Try lower.")
        

if __name__ == "__main__":
    main()
"""A tiny interactive greeter that picks a greeting based on the hour.

Demonstrates:
- importing from the standard library
- defining functions with parameters, return values, and type hints
- if / elif / else
- f-strings
- the standard if __name__ == "__main__" entry point

Run with: python3 examples/greet.py
"""

from datetime import datetime


def greeting_for(hour: int) -> str:
    """Return a time-appropriate greeting for the given hour (0-23)."""
    if hour < 5:
        return "Working late"
    elif hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def build_message(name: str, hour: int) -> str:
    """Combine the greeting and the user's name into one printable line."""
    # .strip() removes surrounding whitespace; .title() capitalizes each word.
    return f"{greeting_for(hour)}, {name.strip().title()}!"


def main() -> None:
    # input() always returns a string; datetime.now() gives the current moment.
    name = input("What is your name? ")
    hour = datetime.now().hour
    print(build_message(name, hour))


# This guard means: run main() only when this file is executed directly.
# If some other file does `import greet`, main() will NOT run automatically.
if __name__ == "__main__":
    main()
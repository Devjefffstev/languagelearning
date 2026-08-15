"""Build a profile card and explore variables in the wild.

Demonstrates the go-deeper half of README.md:
- Type hints on module-level variables (PEP 526)
- The constants-by-convention pattern (UPPER_SNAKE_CASE)
- Input + type conversion (input() always returns a string)
- Immutability of strings vs mutability of lists
- Aliasing: two names, one underlying object
- is vs == for identity vs equality
- Augmented assignment (+=, .append)
- if __name__ == "__main__" entry point

Run with: python3 examples/profile_card.py
"""

# Module-level "constants" -- uppercase per PEP 8. Python doesn't enforce
# these; the convention is a promise to the reader that you won't reassign.
MAX_HOBBIES: int = 5
DEFAULT_GREETING: str = "Hello"


def clean(text: str) -> str:
    """Strip surrounding whitespace and title-case the result."""
    return text.strip().title()


def add_hobby(hobbies: list[str], hobby: str) -> None:
    """Append a cleaned hobby, but never exceed MAX_HOBBIES.

    'hobbies' is a list -- a mutable object. The caller still holds a
    reference to the same list, so changes made here are visible to
    the caller. Strings ('hobby') are immutable; 'cleaned' is a new str.
    """
    cleaned = clean(hobby)
    if cleaned and cleaned not in hobbies:
        if len(hobbies) >= MAX_HOBBIES:
            print(f"  (max {MAX_HOBBIES} hobbies -- '{cleaned}' skipped)")
            return
        hobbies.append(cleaned)


def build_summary(name: str, age: int, city: str, hobbies: list[str]) -> str:
    """Compose the printable profile card.

    Strings are immutable: every '+' or .upper() produces a NEW string.
    The original 'name' is unchanged when we do 'name = name.strip().title()';
    we just rebind the local name to a new string object.
    """
    name = name.strip().title()
    greeting = f"{DEFAULT_GREETING}, {name}!"
    hobby_list = ", ".join(hobbies) if hobbies else "(none yet)"
    return (
        f"{greeting}\n"
        f"  Age : {age}\n"
        f"  City: {city}\n"
        f"  Hobbies ({len(hobbies)}): {hobby_list}"
    )


def demonstrate_identity_vs_equality() -> None:
    """Show why `is` and `==` are different questions."""
    # Two SEPARATE list objects with the SAME contents.
    list_a: list[int] = [1, 2, 3]
    list_b: list[int] = [1, 2, 3]
    print(f"list_a == list_b  ->  {list_a == list_b}   (values equal)")
    print(f"list_a is list_b  ->  {list_a is list_b}   (same object? no)")

    # ONE list object with TWO names stuck on it (aliasing).
    list_c: list[int] = [1, 2, 3]
    list_d: list[int] = list_c       # <-- no copy, just another sticky note
    list_d.append(4)
    print(f"after list_d.append(4): list_c={list_c}  list_d={list_d}")
    print("  -> one object, two names -- both views show 4.")

    # The None singleton: there is exactly ONE None object in the program,
    # so `is` is the right check (and faster than ==).
    maybe: str | None = None
    print(f"maybe is None  ->  {maybe is None}   (use `is` for None)")


def main() -> None:
    name = input("What is your name? ")
    age = int(input("How old are you? "))
    city = input("What city do you live in? ")

    hobbies: list[str] = []        # mutable list, starts empty
    print(f"Enter up to {MAX_HOBBIES} hobbies (blank line to finish):")
    while len(hobbies) < MAX_HOBBIES:
        hobby = input(f"  hobby #{len(hobbies) + 1}: ")
        if hobby.strip() == "":
            break
        add_hobby(hobbies, hobby)

    print()
    print(build_summary(name, age, city, hobbies))
    print()
    demonstrate_identity_vs_equality()


if __name__ == "__main__":
    main()

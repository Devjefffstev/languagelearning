# Python Variables

> Session 2 — drill down on what `x = 5` actually means.
> Code samples target **Python 3.14** and run on 3.11+.

## Description

In Python, a **variable** is a *name* that is bound to an *object*. When you
write `x = 5`, the name `x` does not "hold the number 5" — `x` is a label
that *points to* an integer object whose value is `5`. The official docs
say it directly: *"Names refer to objects. Names are introduced by name
binding operations."* (Python Language Reference, §4.2.1). That single
sentence is the foundation for almost every Python surprise you'll ever
meet, including the ones in the "go deeper" half of this guide.

The basics side of this guide covers four things:

1. **How assignment works** — what `=` actually does, including reassignment,
   multiple assignment (`a = b = 5`), and tuple unpacking (`a, b = 1, 2`).
2. **Naming rules and conventions** — what's legal (letters, digits,
   underscores; can't start with a digit; case-sensitive) and what's
   idiomatic per PEP 8 (`snake_case` for variables, `UPPER_SNAKE_CASE`
   for module-level constants).
3. **Dynamic typing** — the type lives on the *object*, not on the name.
   You can re-point `x` at anything of any type.
4. **The basic scalar types you'll touch first** — `int`, `float`, `str`,
   `bool`, `None`.

The go-deeper side covers the four ideas that turn "I can write `x = 5`"
into "I understand what my program is actually doing at runtime":

5. **Mutability vs immutability** — `int`, `float`, `str`, `tuple`,
   `frozenset`, `bool`, `None` are *immutable* (you can't change them in
   place; you make new ones). `list`, `dict`, `set`, `bytearray` are
   *mutable* (you can change them in place). This distinction is what
   makes strings safe as dict keys but lists not safe as dict keys.
6. **References and aliasing** — `a = [1, 2]; b = a` does **not** copy the
   list. Both names point at the same object, so `b.append(3)` is also
   visible through `a`. The official tutorial calls this out: *"Simple
   assignment in Python never copies data."* (Tutorial, §3.1.3).
7. **`is` vs `==`** — `==` asks "do these objects have equal *values*?",
   `is` asks "are these the *same object* in memory?". Most of the time
   you want `==`. `is` is for `None` and a few other singletons.
8. **Variable annotations and augmented assignment** — `name: str = "Ada"`
   is just a label for humans and type checkers; Python does not enforce
   it. And `x += 1` is mostly the same as `x = x + 1`, except that for
   mutable objects it can mutate in place rather than rebind.

The mental model to keep: **the name is a sticky note, the object is the
jar**. Re-pointing the sticky note is reassignment. Writing on the jar is
mutation. Two sticky notes on the same jar is aliasing.

## Analogy

Picture your kitchen. Each ingredient is in a jar on a shelf, and each
jar has a sticky note on the front with its name: `flour`, `sugar`,
`eggs`. The sticky note is **not** the ingredient — it's just a label
that points to a specific jar on a specific shelf.

That's `x = flour` in Python: the name `flour` is a sticky note, and
it's been placed on the jar labeled "flour". Two rules govern the rest:

- **You can move a sticky note.** Peel `flour` off its jar and stick it on
  the jar labeled "sugar". Now `flour` points to sugar. This is
  **reassignment** — and notice that the old jar (flour) is unchanged;
  only the *label* moved.
- **But not every jar lets you write on it.** The flour jar is glass —
  you can see what's inside, but if you want a different amount of flour,
  you have to get a new jar and re-stick the note. The eggs carton,
  though, is a plastic bag — you can crack one open, remove an egg, and
  put the carton back on the shelf. The carton (the object) is still the
  same carton, and the sticky note is still on it. **Glass jars are
  immutable objects. Plastic bags are mutable objects.**

This single image explains all four deep ideas:

| Concept           | Sticky-note version                                      |
|-------------------|----------------------------------------------------------|
| **Reassignment**  | Peel `x` off jar A and stick it on jar B.                |
| **Mutation**      | Take the plastic-bag jar (a list) and add something to it — the sticky note stays put, the jar's contents change. |
| **Aliasing**      | Put **two** sticky notes (`a` and `b`) on the *same* plastic-bag jar. Now anything you do through `a` is visible through `b`. |
| **`is` vs `==`**  | `==` asks "do the jars contain the same *stuff*?". `is` asks "are the two sticky notes on the *same* jar?". Two jars of sugar look the same, but they're two different jars. |

A subtle but important corollary: the sticky note has *no idea what's in
the jar*. It doesn't say "I am a string note" or "I am an integer note".
If you peel it off and stick it on a jar of eggs, that's fine. This is
**dynamic typing**: the type lives on the object (the jar), not on the
name (the sticky note).

## Examples

### Example #1

#### Quick setup

A 20-line tour of everything in the foundations half — assignment,
dynamic typing, multiple assignment, augmented assignment, and the five
basic scalar types:

```python
# examples/sticky_notes.py
"""Foundations: assignment, dynamic typing, multiple + augmented assignment."""

# 1. Plain assignment. The name 'language' points to a str object.
language = "Python"

# 2. The name 'version' points to a float. We never declared a type —
#    Python figured it out from the literal on the right.
version = 3.14

# 3. Reassignment: 'language' is the SAME sticky note, now stuck on a
#    different object (a different str). The old str is unchanged.
language = "Python 🐍"

# 4. Multiple assignment: the same object is bound to three names at once.
#    All three names point to the same integer object 42.
a = b = c = 42

# 5. Tuple unpacking: the right-hand side builds a tuple, and the three
#    names on the left are bound to its three elements, position by
#    position. Right-hand side is fully evaluated FIRST, then assigned.
x, y, z = 1, 2, 3

# 6. Augmented assignment: 'counter += 1' is shorthand for
#    'counter = counter + 1' for immutable types. For mutable types
#    (lists, dicts) it can mutate in place instead — see the README.
counter = 0
counter += 1   # 1
counter += 1   # 2

# 7. The five scalar types you'll meet first.
an_int     = 7          # int      — whole numbers
a_float    = 3.14       # float    — decimals
a_str      = "hello"    # str      — text
a_bool     = True       # bool     — True or False (subclass of int!)
nothing    = None       # NoneType — "no value yet" / "absence of a value"

print(f"{language} {version}")
print(f"a={a}  b={b}  c={c}  ->  all three point to the same int object")
print(f"x={x}  y={y}  z={z}  ->  tuple unpacking")
print(f"counter={counter}")
print(f"types: {type(an_int).__name__}, {type(a_float).__name__}, "
      f"{type(a_str).__name__}, {type(a_bool).__name__}, "
      f"{type(nothing).__name__}")
```

Run it:

```bash
python3 examples/sticky_notes.py
```

Expected output:

```
Python 🐍 3.14
a=42  b=42  c=42  ->  all three point to the same int object
x=1  y=2  z=3  ->  tuple unpacking
counter=2
types: int, float, str, bool, NoneType
```

#### Complete setup

A small interactive program that builds a profile "card" from your input
and demonstrates the go-deeper half: type hints on variables (PEP 526),
immutable strings vs mutable lists, references and aliasing, `is` vs
`==`, and the constants-by-convention pattern:

```python
# examples/profile_card.py
"""Build a profile card and explore variables in the wild.

Demonstrates:
- Type hints on module-level variables (PEP 526)
- The constants-by-convention pattern (UPPER_SNAKE_CASE)
- Input + type conversion
- Immutability of strings vs mutability of lists
- Aliasing: two names, one underlying object
- is vs == for identity vs equality
- Augmented assignment (+=, .append)
- if __name__ == "__main__" entry point
"""

# Module-level "constants" — uppercase per PEP 8. Python doesn't enforce
# these; the convention is a promise to the reader that you won't reassign.
MAX_HOBBIES: int = 5
DEFAULT_GREETING: str = "Hello"


def clean(text: str) -> str:
    """Strip surrounding whitespace and title-case the result."""
    return text.strip().title()


def add_hobby(hobbies: list[str], hobby: str) -> None:
    """Append a cleaned hobby, but never exceed MAX_HOBBIES.

    'hobbies' is a list — a mutable object. The caller still holds a
    reference to the same list, so changes here are visible to the caller.
    """
    cleaned = clean(hobby)
    if cleaned and cleaned not in hobbies:
        if len(hobbies) >= MAX_HOBBIES:
            print(f"  (max {MAX_HOBBIES} hobbies — '{cleaned}' skipped)")
            return
        hobbies.append(cleaned)


def build_summary(name: str, age: int, city: str, hobbies: list[str]) -> str:
    """Compose the printable profile card."""
    # Strings are immutable: every '+' or .upper() produces a NEW string.
    # The original `name` is unchanged.
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
    print(f"  -> one object, two names — both views show 4.")

    # The None singleton: there is exactly ONE None object in the program,
    # so `is` is the right check (and faster).
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
```

Run it:

```bash
python3 examples/profile_card.py
```

Sample interaction:

```
What is your name?  ada lovelace
How old are you?  36
What city do you live in?  London
Enter up to 5 hobbies (blank line to finish):
  hobby #1: math
  hobby #2: writing
  hobby #3:

Hello, Ada Lovelace!
  Age : 36
  City: London
  Hobbies (2): Math, Writing

list_a == list_b  ->  True   (values equal)
list_a is list_b  ->  False  (same object? no)
after list_d.append(4): list_c=[1, 2, 3, 4]  list_d=[1, 2, 3, 4]
  -> one object, two names — both views show 4.
maybe is None  ->  True   (use `is` for None)
```

The four things this example shows beyond the basics:

- **Type hints on variables** — `hobbies: list[str] = []` and the
  constants `MAX_HOBBIES: int = 5`. These are PEP 526 annotations; they
  are documentation for humans and type checkers. Python does not
  enforce them at runtime.
- **Constants by convention** — `MAX_HOBBIES` is uppercase to signal
  "don't reassign this". Nothing stops you from writing
  `MAX_HOBBIES = 999` later; the convention is the contract.
- **Aliasing in action** — `list_d = list_c` puts two sticky notes on
  one jar. `list_d.append(4)` changes the jar's contents, and the
  change shows up through `list_c` too.
- **`is` vs `==`** — two lists with equal contents compare `==` True
  but `is` False; one list with two names compares both True; and
  `is None` is the idiomatic check for the None singleton.

## Exercises

The four exercises drill one piece at a time, easiest first. They are
designed to be done in order.

- `exercises/01_name_that_variable/` — Given a list of variable names,
  classify each as legal/illegal and idiomatic/non-idiomatic, then rewrite
  the bad ones. Pure conceptual warmup; no logic. **Easy.**
- `exercises/02_swap_and_unpack/` — Swap two values and unpack a list
  into head/tail. Practices tuple unpacking and the `a, b = b, a` idiom.
  **Easy–medium.**
- `exercises/03_profile_card/` — Build a small profile program using
  type hints, augmented assignment, and the constants-by-convention
  pattern. Reinforces everything in `profile_card.py`. **Medium.**
- `exercises/04_aliasing_detective/` — Given snippets, predict the
  output, then run them to check. Fix two aliasing bugs without changing
  what the program is supposed to do. **Medium–hard.**

Each exercise folder has its own `README.md` with the goal, task, hints,
and success criteria, plus a `starter.py` marked with `TODO` where you
write your code. Hints point the way; they don't hand over the answer.

## Research

### Reference URLs

All links fetched and verified on 2026-07-29.

- <https://docs.python.org/3/tutorial/introduction.html> — The official
  tutorial's first chapter: `width = 20` style assignment, the `NameError`
  for undefined names, and the explicit note that *"Simple assignment in
  Python never copies data"* (the source of the aliasing surprise).
- <https://docs.python.org/3/reference/executionmodel.html> — The
  language reference's section on *"Names refer to objects. Names are
  introduced by name binding operations"* — the foundation for
  everything in the Description above.
- <https://docs.python.org/3/reference/simple_stmts.html> — The exact
  specification for assignment statements, augmented assignment
  (`+=`, `.append` vs rebind), and annotated assignment statements.
- <https://peps.python.org/pep-0008/> — PEP 8, the Style Guide for
  Python Code. The *Naming Conventions* and *Constants* subsections
  explain `snake_case` for variables and `UPPER_CASE` for module-level
  constants.
- <https://peps.python.org/pep-0526/> — PEP 526, the proposal that
  introduced the `name: str = "Ada"` variable-annotation syntax used
  throughout `profile_card.py`.
- <https://docs.python.org/3/library/constants.html> — The official
  reference for `True`, `False`, `None`, `NotImplemented`, `Ellipsis`,
  and `__debug__`. Note the line *"The names None, False, True and
  __debug__ cannot be reassigned."*
- <https://docs.python.org/3/glossary.html> — Python's glossary
  entries for **immutable** (*"An object with a fixed value... Such an
  object cannot be altered"*) and **mutable** — the one-paragraph
  definitions you can quote when explaining the difference to a teammate.

## Next steps

Once the four exercises feel easy, the natural directions to go deeper
are: (1) read the *Naming and binding* and *Resolution of names*
sections of the Execution Model reference end-to-end — they cover scope,
the `global` and `nonlocal` statements, and the subtle rule that
"Python lacks declarations and allows name binding operations to occur
anywhere within a code block"; (2) re-implement `profile_card.py` using
a `dataclass` from the `dataclasses` module, which lets you write
`name: str` as a *class attribute* (not a module variable) and get
`__init__`, `__repr__`, and `__eq__` for free; (3) experiment with
`copy.copy()` and `copy.deepcopy()` on a list of lists to see exactly
how shallow vs deep copying differs when aliasing gets nested.

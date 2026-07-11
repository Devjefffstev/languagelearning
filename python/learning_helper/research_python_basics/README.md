# Python Basics

> Session 1 — first contact with the language.
> Code samples are written for **Python 3.14** (latest stable as of July 2026)
> and run unchanged on the 3.11 interpreter available on this machine.

## Description

Python is a high-level, general-purpose programming language whose design
philosophy emphasizes code that reads like English. It is **interpreted** (no
separate compilation step), **dynamically typed** (you don't declare the type
of a variable — Python figures it out from the value you give it), and ships
with a very large **standard library** so you can do real work with very few
extra dependencies.

Python programs are organized as **modules** (`.py` files) containing **statements**
and **expressions**. An expression is anything that produces a value (`2 + 2`,
`len(name)`, `"hello".upper()`); a statement is a complete instruction
(`x = 2`, `if x > 0:`, `def greet(): ...`). The interpreter runs them top to
bottom.

In this first session you will touch the eight building blocks you will use
in nearly every program you ever write in Python:

1. **Values and variables** — assigning names to data with `=`.
2. **Basic types** — `int`, `float`, `str`, `bool`, `None`.
3. **Operators** — arithmetic (`+ - * / // % **`), comparison (`== != < > <= >=`),
   logical (`and`, `or`, `not`).
4. **Strings and f-strings** — text plus the `f"..."` syntax for embedding values.
5. **Control flow** — `if / elif / else` and `for / while` loops.
6. **Data structures** — `list`, `tuple`, `dict`, `set`.
7. **Functions** — `def name(...): ...`, with parameters and `return`.
8. **The standard library** — `random`, `datetime`, etc. are already there,
   you just `import` them.

The core mental model is: **names point to objects**. When you write
`x = 5`, the name `x` becomes a label that points to the integer object `5`.
If you later write `x = "hello"`, you are not "changing the type of `x`" — you
are re-pointing the same label at a different object. This is why Python is
called dynamically typed: the type lives on the object, not on the name.

## Analogy

Think of Python as **executable pseudocode**. Other languages often force you
to write a parts list (declare every type, every size, every connection)
before the program will do anything — like assembling flat-pack furniture by
listing every dowel and screw in advance. Python is more like a recipe
written in plain English: "mix the flour, add the eggs, bake at 350°." You
describe *what* should happen, and the interpreter (the "chef") worries
about the rest.

To extend the recipe analogy:

- **Variables** are the sticky notes you stick on jars — `flour = 2` writes
  "2 cups" on a sticky note labeled `flour`.
- **Lists** are the numbered steps of the recipe — order matters, you can
  reorder them, and you can add new ones.
- **Dictionaries** are the spice rack — instead of looking up by step number,
  you look up by name (`spices["cumin"]`).
- **Functions** are the named sub-recipes ("make the dough") that you can
  reuse every time the recipe calls for them.
- **The standard library** is the kitchen that comes with the cookbook —
  knife, oven, whisk, and a few pantry staples are already there.

## Examples

### Example #1

#### Quick setup

A 5-line "Hello, Python" that touches variables, dynamic typing, an f-string,
a list, and `print`:

```python
# examples/hello.py
name = "Python"        # a string assigned to the name 'name'
version = 3.14         # a float — note we did NOT declare the type
features = ["dynamic", "readable", "batteries included"]  # a list of strings

print(f"Hello, {name} {version}!")          # f-string embeds the values
print(f"Top features: {features}")          # lists print with brackets
print(type(name).__name__, type(version).__name__, type(features).__name__)
```

Run it:

```bash
python3 examples/hello.py
```

Expected output:

```
Hello, Python 3.14!
Top features: ['dynamic', 'readable', 'batteries included']
str float list
```

#### Complete setup

A small interactive program that asks for your name and the current hour,
then prints a personalized greeting. It demonstrates `input`, type conversion,
an `if/elif/else` chain, a function with parameters and a return value, and
a `main()` entry point — the standard "real Python script" shape:

```python
# examples/greet.py
"""A tiny interactive greeter that picks a greeting based on the hour."""

from datetime import datetime


def greeting_for(hour: int) -> str:
    """Return a time-appropriate greeting for the given hour (0–23)."""
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
    return f"{greeting_for(hour)}, {name.strip().title()}!"


def main() -> None:
    # input() always returns a string, so we need datetime.now() for the hour
    name = input("What is your name? ")
    hour = datetime.now().hour
    print(build_message(name, hour))


# This guard makes the file runnable directly but skips main()
# if it is imported by another script — a Python best practice.
if __name__ == "__main__":
    main()
```

Run it:

```bash
python3 examples/greet.py
```

Sample interaction:

```
What is your name?  ada lovelace
Good evening, Ada Lovelace!
```

Why this version is "complete": it separates concerns (`greeting_for` decides
*what* to say, `build_message` decides *how* to format it, `main` handles I/O),
uses type hints to document the contract, and uses the `if __name__ ==
"__main__"` idiom so the file is both runnable and importable.

## Going deeper on two pieces of `greet.py`

Two lines from the complete setup above deserve a closer look, because the
same patterns appear in nearly every real Python program you'll ever read.

### The arrow in `def build_message(name: str, hour: int) -> str:` — type hints

That single line is actually four pieces glued together:

```
def build_message(name: str, hour: int) -> str:
^^^                ^^     ^   ^  ^   ^^   ^
|                  ||     |   |  |   ||   return-type annotation
|                  ||     |   |  |   ||   "this function returns a str"
|                  ||     |   |  |   |+--- end of the def header
|                  ||     |   |  |   +---- the arrow
|                  ||     |   |  +-------- second parameter's type
|                  ||     |   +----------- second parameter (hour)
|                  ||     +--------------- colon separating name from type
|                  |+--------------------- first parameter's type
|                  +---------------------- first parameter (name)
+------------------------------------------ function name
+------------------------------------------ the `def` keyword
```

So:

- **`name: str`** — "I expect the caller to pass a string for `name`."
- **`hour: int`** — "I expect the caller to pass an integer for `hour`."
- **`-> str`** — "this function returns a string."

These are called **type hints** (or type annotations). They were added to
Python 3.5 ([PEP 484](https://peps.python.org/pep-0484/)) and have been
refined since.

#### What type hints ARE

Labels — pure documentation. They are stored on the function object and
you can read them back any time:

```python
def shout(text: str) -> str:
    return text.upper()

>>> shout.__annotations__
{'text': <class 'str'>, 'return': <class 'str'>}
```

#### What type hints ARE NOT

They are **not enforced at runtime**. Python will happily let you call a
function with the "wrong" type. Watch what happens when we pass an `int`
into a function annotated `text: str`:

```python
def shout(text: str) -> str:
    return text.upper()

shout("hello")   # → "HELLO"
shout(42)        # → AttributeError: 'int' object has no attribute 'upper'
```

Notice where the crash happens: **inside** the function, on the line that
calls `.upper()`. The call itself succeeds — Python did **not** stop you
from passing an `int` where the annotation said `str`. The error comes
later, from a real operation failing. This is the opposite of Java or
C++, where `shout(42)` would be refused at compile time.

#### So why bother with them?

1. **Humans** reading your code know what you intended without reading the body.
2. **IDEs** (PyCharm, VS Code) use them for autocomplete and inline warnings.
3. **Static type checkers** like `mypy` and `pyright` read them and warn
   you *before* you ever run the code.
4. **Libraries** (dataclasses, Pydantic, FastAPI, attrs) use annotations
   at runtime to generate behavior.

In `greet.py`, the annotations are a promise to the reader: "trust me, I
will pass a string and an int, and I will give you back a string."

### `if __name__ == "__main__":` — runnable AND importable

Every Python file (every **module**) automatically gets a built-in variable
named `__name__`. Its value depends on how the file is being used:

| You do this…                       | Python sets `__name__` to…   |
|------------------------------------|------------------------------|
| `python3 greet.py`                 | `"__main__"`                 |
| From another file: `import greet`  | `"greet"` (the module name)  |

#### A related subtlety: module name vs. filename

`__name__` is the **module name** (no `.py`), not the filename. You can
verify this on any imported module:

```python
import greeter
greeter.__name__     # → 'greeter'         (module name, no extension)
greeter.__file__     # → '.../greeter.py'  (actual file on disk)
```

The two usually match by convention — you wrote `greeter.py` and imported
it as `greeter`. But `import` is using the **module name**; Python then
looks for a file with that name plus `.py` (or a package directory
containing `__init__.py`). They don't even have to match — a common
example is the machine-learning package installed on disk as
`scikit-learn` but imported as `sklearn`:

```bash
pip install scikit-learn
python3 -c "import sklearn; print(sklearn.__name__, sklearn.__file__)"
# → sklearn  .../site-packages/sklearn/__init__.py
```

So the rule: the `import` statement uses the module name; Python uses
that name to locate a file (or package) with the matching name. The
filename and the import name usually agree, but they are not the same
thing.

That is the whole trick. The idiom

```python
if __name__ == "__main__":
    main()
```

literally translates to: **"If I am the program being run directly, do
this; otherwise, stay quiet."**

#### Why this matters

Imagine `greet.py` had `print(build_message("Ada", 20))` at the top level
instead of guarded by `if __name__ == "__main__":`. The file would still
work fine when you run `python3 greet.py`. But when a teammate writes
their own program and does `from examples.greet import build_message` to
reuse your function, **importing your file would also run your demo** —
their program would spit out `"Good evening, Ada!"` before it even
started. That is a side effect of being imported, which is rude.

With the guard, importing just gives them access to the function; the
demo code only runs when *they* explicitly run `greet.py`.

#### See it in action with two tiny files

Save these two files side-by-side in a temp folder and run them:

```python
# greeter.py
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(f"[greeter.py] loaded. __name__ = {__name__!r}")

if __name__ == "__main__":
    print("[greeter.py] running as the main program -> calling greet()")
    print(greet("Ada"))
else:
    print("[greeter.py] imported by another module -> staying quiet")
```

```python
# runner.py
import greeter

print("[runner.py] is the main program now.")
print(f"[runner.py] my own __name__ = {__name__!r}")
print("[runner.py] calling greeter.greet() directly:")
print(greeter.greet("Linus"))
```

**Run 1** — `python3 greeter.py` (greeter is the main program):

```
[greeter.py] loaded. __name__ = '__main__'
[greeter.py] running as the main program -> calling greet()
Hello, Ada!
```

**Run 2** — `python3 runner.py` (runner is the main program, greeter is imported):

```
[greeter.py] loaded. __name__ = 'greeter'
[greeter.py] imported by another module -> staying quiet
[runner.py] is the main program now.
[runner.py] my own __name__ = '__main__'
[runner.py] calling greeter.greet() directly:
Hello, Linus!
```

Same `greeter.py` file, same `import`, same function — but its `__name__`
is different, and the guarded block fires only in the first run.

#### Tying it back to `greet.py`

The `if __name__ == "__main__":` block at the bottom of `greet.py` means:

- When **you** run `python3 examples/greet.py`, you are the program →
  `__name__ == "__main__"` → `main()` runs → the program prompts you
  and prints a greeting.
- When **someone else** writes their own script and does
  `from examples.greet import build_message` (or similar), your `main()`
  does **not** run automatically. They get access to `build_message`,
  `greeting_for`, and `datetime`, and can compose them into their own
  program. If they ever want the demo behavior, they call `main()`
  themselves.

That dual nature — "demo when run, library when imported" — is what
people mean by "the file is both runnable and importable."

## Going deeper on the word counter

The hint in Exercise 03 shows the classic loop version of `count_words`:

```python
def count_words(text: str) -> dict:
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

You arrived at a one-liner instead:

```python
def count_words(text: str) -> dict:
    return {word: text.split().count(word) for word in set(text.split())}
```

Both produce the same dictionary — yours just rewrites the loop as a
**dict comprehension**. Let's unpack the four pieces.

### Anatomy of the dict comprehension

```python
{word: text.split().count(word) for word in set(text.split())}
^^      ^^^^^^^^^^^^^^^^^^^^^^^^   ^^^   ^^^^^^^^^^^^^^^^^
|       |                           |     |
|       |                           |     the iterable we loop over
|       |                           the loop variable — one word at a time
|       the expression that becomes each value
the key in each (key, value) pair
                                                          
opening brace — makes this a dict (vs. [] list, () tuple, () with set() inside)
```

A **dict comprehension** has the shape:

```python
{key_expr: value_expr for item in iterable}
```

It is the loop version written sideways, with Python collecting each
`(key, value)` pair into a fresh dict for you. Sister syntaxes you will
meet later:

```python
[x * 2 for x in [1, 2, 3]]      # [2, 4, 6]    – list comprehension
{x * 2 for x in [1, 2, 3]}      # {2, 4, 6}    – set comprehension
{x: x * 2 for x in [1, 2, 3]}   # {1: 2, 2: 4} – dict comprehension
```

### What each piece does in your one-liner

- **`text.split()`** — splits the paragraph into a list of words.
- **`set(text.split())`** — wraps the list in a `set`, removing
  duplicates. Why? Because we want exactly one row in the dict per
  unique word, and the dict comprehension body runs once per element
  in the source iterable.
- **`for word in set(text.split())`** — iterates over those unique words.
- **`text.split().count(word)`** — counts how many times `word` appears
  in the **full** split list (not the deduplicated one). `list.count(v)`
  returns the number of occurrences of `v` in the list.
- **`{word: ... for word in ...}`** — collects each `(word, count)` pair
  into a dict.

Side note on order: because `set` has no defined iteration order, the
keys in your version can land in any order (interpreter-dependent).
The loop version's keys arrive in the order words first appear in the
text. Both dicts are **equal as dicts** — only the printed order
differs.

### The tradeoff

Yours reads beautifully. The loop is faster.

- **Loop version**: walks the list **once**, incrementing a counter as
  it goes. Total work is O(n) where n is the number of tokens.
- **Comprehension version**: calls `text.split().count(word)` **once
  per unique word**. Each `.count` call walks the list from the start,
  so total work is O(n × unique_words).

For 22 words in 23 tokens it doesn't matter. For a million-word text
you would notice. The loop stays fast regardless of input size.

Rule of thumb: when the data is small (paragraphs, log lines, test
fixtures), prefer the comprehension — it reads more clearly. When the
data is large (logs, books, web corpora), prefer the loop or a
purpose-built tool.

### Bonus: the standard library has a one-liner too

If counting is all you need, `collections.Counter` does the job without
any hand-rolled logic:

```python
from collections import Counter

def count_words(text: str) -> dict:
    return dict(Counter(text.split()))
```

`Counter` is a `dict` subclass designed exactly for "how many times
does each thing appear?". It runs at loop speed (~O(n)) because it uses
the same increment-counter trick as the loop version. It is the
standard library answer to the problem you just solved two different
ways by hand.

## Going deeper on the increment trick

The hint loop version of `count_words` is:

```python
def count_words(text: str) -> dict:
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

The interesting line is the increment:

```python
counts[word] = counts.get(word, 0) + 1
```

It's three pieces of work packed into one expression, and it has to
handle two distinct situations without an explicit branch. Let's
unpack it.

### Three pieces, three jobs

```python
counts[word] = counts.get(word, 0) + 1
^^^^      ^^^^^                 ^^^
|         |                     |
|         |                     the +1 = "I just saw one more occurrence"
|         |
|         dict.get(key, default): return the value at `word`
|                                  if it exists, otherwise return 0
|
the assignment — store the new total back into counts at key `word`
```

Read **right-to-left**, because that's the order Python evaluates:

1. `counts.get(word, 0)` — look up `word`. If it's already a key
   return the current count; if not, return `0`. `dict.get` **never
   raises** — it always returns the value or the default.
2. `+ 1` — "I just saw one more occurrence of this word."
3. `counts[word] = ...` — write the new total back into the dict at
   key `word`. If `word` was missing, this creates the entry; if it
   was already there, it overwrites it.

### Two code paths converge on the same line

The same expression handles both first occurrence and re-occurrence
without an explicit `if`:

- **First time we see `word`** — `counts.get(word, 0)` returns `0`,
  then `0 + 1 = 1`, then `counts[word] = 1`. The dict gains the entry.
- **Subsequent time** — `counts.get(word, 0)` returns the current
  count, then `current + 1 = new`, then `counts[word] = new`. The dict
  updates the entry.

A trace through `["the", "cat", "the", "dog", "the"]`:

```
 word   before                              after
 'the'  {}                                  {'the': 1}                ← first time, get(.., 0) → 0, +1 → 1
 'cat'  {'the': 1}                          {'the': 1, 'cat': 1}      ← first time, same story
 'the'  {'the': 1, 'cat': 1}                {'the': 2, 'cat': 1}      ← 'the' was there, get → 1, +1 → 2
 'dog'  {'the': 2, 'cat': 1}                {'the': 2, 'cat': 1, 'dog': 1}
 'the'  {'the': 2, 'cat': 1, 'dog': 1}      {'the': 3, 'cat': 1, 'dog': 1}
```

Same expression, two paths, same destination: a dict mapping each
word to its total.

### Three other ways to spell the same thing

Python has more than one idiomatic way to bump a counter in a dict.
They're equivalent in behavior; they trade off readability and
Python-version requirements.

```python
# (1) The hint version — works on every Python 3.x
counts[word] = counts.get(word, 0) + 1

# (2) if/in — most explicit, slightly more lines
if word in counts:
    counts[word] += 1
else:
    counts[word] = 1

# (3) defaultdict — say once what the default is; then += "just works"
from collections import defaultdict
counts = defaultdict(int)         # missing keys default to 0
for word in text.split():
    counts[word] += 1
```

`defaultdict(int)` is the nicest in real code: you tell it "missing
keys default to `0`," and from then on `counts[word] += 1` works on
first-time words just as naturally as on repeats. The catch: you have
to construct the dict with the right default **before** the loop
starts — you can't sprinkle `defaultdict(int)` into an already-empty
dict mid-flow.

### And the standard library answer, one more time

`collections.Counter` is purpose-built for this exact problem:

```python
from collections import Counter
counts = dict(Counter(text.split()))
```

It runs at loop speed (~O(n)) and replaces the whole increment dance
— the same module that the one-liner `count_words` from the previous
section also relies on. It's the answer Python gives you when you
say "I just want to count things," and it makes both of the
hand-rolled versions obsolete for production work.

## Exercises

Each exercise lives in its own folder under `exercises/`. They are ordered
easiest → hardest; do them in order if this is your first Python session.

- `exercises/01_temperature_converter/` — Read a temperature and a unit
  from the user, convert it, and print the result. Practices input,
  arithmetic, formatted output, and a small function. **Easy.**
- `exercises/02_grade_classifier/` — Take a numeric score and classify it
  as A/B/C/D/F using `if/elif/else`, with input validation. **Easy–medium.**
- `exercises/03_word_frequency/` — Count how often each word appears in a
  short paragraph and print the top 5. Practices strings, `dict`, loops, and
  `sorted()` with a key. **Medium.**
- `exercises/04_number_guessing_game/` — Build a number-guessing game with
  random target, hints, and attempt counting. Practices `import`, `while`,
  `break`, and string formatting. **Medium–hard.**

Each folder has its own `README.md` with the goal, task, hints, and success
criteria, plus a starter file marked with `TODO` where you write your code.

## Research

### Reference URLs

All links were fetched and verified on 2026-07-09.

- <https://docs.python.org/3/tutorial/index.html> — Official Python Tutorial
  landing page; the canonical starting point for new Python programmers.
- <https://docs.python.org/3/tutorial/introduction.html> — Covers values,
  numbers, strings, lists, and your first multi-line program (the Fibonacci
  example).
- <https://docs.python.org/3/tutorial/controlflow.html> — `if`, `for`, `while`,
  `match`, and function definitions with default and keyword arguments.
- <https://docs.python.org/3/tutorial/datastructures.html> — Lists, tuples,
  sets, dictionaries, and looping techniques (`enumerate`, `zip`, `sorted`,
  `reversed`).
- <https://docs.python.org/3/library/functions.html> — Every built-in
  function (`print`, `len`, `range`, `input`, `int`, `sorted`, …) in one
  alphabetical reference.
- <https://wiki.python.org/moin/BeginnersGuide> — Curated list of beginner
  tutorials and learning resources, grouped by whether you've programmed
  before.

## Next steps

Once the four exercises feel comfortable, two natural directions to go
deeper are: (1) read chapters 4 and 5 of the official tutorial end-to-end and
re-implement `greet.py` using a `match` statement instead of `if/elif/else`,
and (2) build a small project that combines everything — for example, a
command-line flashcard app that loads questions from a file and tracks your
score in a dictionary. Along the way you'll meet **lists of dictionaries**,
**list comprehensions**, and **reading/writing files**, which are the next
layer of Python fluency.
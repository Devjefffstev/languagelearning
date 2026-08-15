"""Foundations: assignment, dynamic typing, multiple + augmented assignment.

Run with: python3 examples/sticky_notes.py

This file pairs with the Quick setup section of README.md. Every line
maps to one of the four foundation ideas:

  1. Plain assignment           -> language, version
  2. Dynamic typing             -> type() output at the bottom
  3. Reassignment               -> language = "Python \U0001F40D"
  4. Multiple assignment        -> a = b = c = 42
  5. Tuple unpacking            -> x, y, z = 1, 2, 3
  6. Augmented assignment       -> counter += 1
  7. The five scalar types      -> int, float, str, bool, NoneType
"""

# 1. Plain assignment. The name 'language' points to a str object.
language = "Python"

# 2. The name 'version' points to a float. We never declared a type --
#    Python figured it out from the literal on the right.
version = 3.14

# 3. Reassignment: 'language' is the SAME sticky note, now stuck on a
#    different object (a different str). The old str is unchanged;
#    only the label moved.
language = "Python \U0001F40D"

# 4. Multiple assignment: the same object is bound to three names at once.
#    All three names point to the same integer object 42.
a = b = c = 42

# 5. Tuple unpacking: the right-hand side builds a tuple (1, 2, 3), and
#    the three names on the left are bound to its three elements, one by
#    one. The right-hand side is fully evaluated FIRST, then assigned --
#    so something like x, y = y, x actually works as a swap.
x, y, z = 1, 2, 3

# 6. Augmented assignment: 'counter += 1' is shorthand for
#    'counter = counter + 1' for immutable types. For mutable types
#    (lists, dicts) it can mutate in place instead -- see README.md.
counter = 0
counter += 1   # 1
counter += 1   # 2

# 7. The five scalar types you'll meet first.
an_int     = 7          # int      -- whole numbers
a_float    = 3.14       # float    -- decimals
a_str      = "hello"    # str      -- text
a_bool     = True       # bool     -- True or False (subclass of int!)
nothing    = None       # NoneType -- "no value yet" / "absence of a value"

print(f"{language} {version}")
print(f"a={a}  b={b}  c={c}  ->  all three point to the same int object")
print(f"x={x}  y={y}  z={z}  ->  tuple unpacking")
print(f"counter={counter}")
print(
    f"types: {type(an_int).__name__}, {type(a_float).__name__}, "
    f"{type(a_str).__name__}, {type(a_bool).__name__}, "
    f"{type(nothing).__name__}"
)

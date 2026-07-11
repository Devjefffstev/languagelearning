"""A 5-line 'Hello, Python' that touches variables, dynamic typing,
f-strings, and a list.

Run with: python3 examples/hello.py
"""

name = "Python"                     # a string assigned to the name 'name'
version = 3.14                      # a float — note we did NOT declare the type
features = ["dynamic", "readable", "batteries included"]  # a list of strings

# f-strings (formatted string literals) embed the value of any expression
# inside curly braces. The leading 'f' is required.
print(f"Hello, {name} {version}!")
print(f"Top features: {features}")

# Every value in Python has a type. type(x) returns the type object;
# .__name__ gives just the class name as a string.
print(type(name).__name__, type(version).__name__, type(features).__name__)
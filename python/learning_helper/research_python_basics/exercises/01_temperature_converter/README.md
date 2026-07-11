# Exercise 01 — Temperature Converter

## Goal

Build a small command-line program that converts a temperature between
Celsius and Fahrenheit based on user input.

## Task

Write a script that:

1. Greets the user with a single line explaining what the program does.
2. Asks the user for a **temperature value** (a number, possibly with
   decimals).
3. Asks the user for the **current unit** — either the letter `C` (Celsius)
   or `F` (Fahrenheit). Accept both upper- and lowercase.
4. Converts the temperature to the other unit using these formulas:
   - C → F: `F = C * 9/5 + 32`
   - F → C: `C = (F - 32) * 5/9`
5. Prints the converted value formatted to **2 decimal places**.
6. Rejects anything that isn't a number or isn't `C`/`F`, prints a friendly
   error message, and exits.

Use at least **one function** in your solution (e.g. `c_to_f(c)` /
`f_to_c(f)`), and prefer an f-string for the final output.

A skeleton is provided in `starter.py` — fill in the `TODO` sections.

## Hints

1. `input()` always returns a string. To do arithmetic you must convert it:
   `float(value_str)` will accept decimals; `int()` will reject them.
2. You can normalize the unit with `.upper()` so the user can type `c`,
   `C`, `f`, or `F` interchangeably.
3. The standard formula check is: `celsius * 9 / 5 + 32` and
   `(fahrenheit - 32) * 5 / 9`. Mind the parentheses on the second one.
4. To format to 2 decimals: `f"{value:.2f}"` (the `:.{n}f` part is the
   format spec; `.2f` means "float with 2 digits after the decimal point").

## Success criteria

Running `python3 starter.py` and entering `100` and `C` prints:

```
100.00°C = 212.00°F
```

Entering `32` and `F` prints:

```
32.00°F = 0.00°C
```

Entering `hot` and `C` (or anything else non-numeric) prints a polite
error message and exits with a non-zero status — your program does **not**
crash with a raw Python traceback.

## Stretch goals (optional)

- Loop and keep asking until the user types `quit`.
- Support a `K` (Kelvin) unit too. (Kelvin → Celsius is just `K - 273.15`.)
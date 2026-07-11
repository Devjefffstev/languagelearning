"""Starter for Exercise 01 — Temperature Converter.

Fill in the TODO sections. Run with: python3 starter.py
"""


def celsius_to_fahrenheit(c: float) -> float:
    """TODO: return the Fahrenheit equivalent of the Celsius value c."""
    # Hint: the formula is F = C * 9/5 + 32
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f: float) -> float:
    """TODO: return the Celsius equivalent of the Fahrenheit value f."""
    # Hint: the formula is C = (F - 32) * 5/9 — keep the parentheses!
    return (f - 32) * 5 / 9


def main() -> None:
    print("Temperature converter (Celsius <-> Fahrenheit)")

    # TODO: ask the user for a temperature (a number), convert it to float,
    #       and handle the case where the user types something that isn't
    #       a number (e.g. wrap the conversion in try / except ValueError).
    try: 
        temp = float(input("Enter a temperature:"))
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return
    # TODO: ask the user for the unit ('C' or 'F', case-insensitive).
    #       If they type anything else, print an error and return early.
    unit = input("Enter the unit (C or F):").strip().upper()
    if unit not in ['C','F']:
        print("Invalid unit. Please enter 'C' for Celsius or 'F' for Fahrenheit.")

    # TODO: based on the unit, call the right conversion function and
    #       print the result formatted to 2 decimal places using an f-string.
    #       Example final line:  "100.00°C = 212.00°F"

    if unit == 'C': 
        converted_temp = celsius_to_fahrenheit(temp)
        print(f"{temp:.2f}°C = {converted_temp:.2f}°F")
    else:
        converted_temp = fahrenheit_to_celsius(temp)
        print(f"{temp:.2f}°F = {converted_temp:.2f}°C")

if __name__ == "__main__":
    main()
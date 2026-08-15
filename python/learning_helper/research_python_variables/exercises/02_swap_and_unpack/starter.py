"""Exercise 02 -- Swap and Unpack.

Practice tuple unpacking in three idiomatic forms.

Run with: python3 starter.py
"""

def swap(a, b):
    """Return (b, a) -- the two arguments with values exchanged."""
    # TODO: one line using tuple unpacking. No temporary variable.
    ...


def first_and_rest(items: list):
    """Return (first, rest) where rest is a new list of everything after index 0."""
    # TODO: one line using a starred target (*).
    ...


def rotate_three(x, y, z):
    """Return (y, z, x) -- shift left by one."""
    # TODO: one line using tuple unpacking.
    ...


def main() -> None:
    print(f'swap(1, 2) -> {swap(1, 2)}')
    print(f'swap("a", "b") -> {swap("a", "b")}')
    print(f'first_and_rest([10, 20, 30, 40]) -> {first_and_rest([10, 20, 30, 40])}')
    print(f'first_and_rest([7]) -> {first_and_rest([7])}')
    print(f'rotate_three(1, 2, 3) -> {rotate_three(1, 2, 3)}')
    print(f'rotate_three("a", "b", "c") -> {rotate_three("a", "b", "c")}')


if __name__ == "__main__":
    main()

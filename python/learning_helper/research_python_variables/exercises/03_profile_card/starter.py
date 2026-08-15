"""Exercise 03 -- Profile Card.

A smaller version of examples/profile_card.py that you write yourself.
Four TODOs to fill in.

Run with: python3 starter.py
"""

# TODO(1): declare two module-level constants with type hints:
#   MAX_LEVEL     -- an int cap on the level field (pick 99)
#   DEFAULT_NAME  -- a str used when the player enters a blank name
# (Use uppercase snake_case names per PEP 8.)


def clamp_level(level: int) -> int:
    """Return `level` clamped to the range [1, MAX_LEVEL]."""
    # TODO(2): one expression that returns the clamped value.
    ...


def record_gain(scores: list[int], amount: int) -> None:
    """Append `amount` to `scores` only if it is positive."""
    # TODO(3): filter for amount > 0, then append. No return value
    # (lists are mutable -- the caller's list is updated in place).
    ...


def build_summary(name: str, level: int, scores: list[int]) -> str:
    """Compose the printable summary card as a single string."""
    # TODO(4): return a multi-line f-string in this exact format:
    #   Player: <name>
    #   Level : <level>
    #   Score : <total>  (<count> gains)
    # where <total> = sum(scores) and <count> = len(scores).
    # If scores is empty, total should be 0 and the line should
    # still read cleanly (e.g. "(0 gains)").
    ...


def main() -> None:
    name = input("Player name (blank for default): ").strip() or DEFAULT_NAME
    level = int(input("Starting level: "))
    level = clamp_level(level)

    scores: list[int] = []
    print("Enter score gains one per line (blank line to finish):")
    while True:
        raw = input(f"  gain #{len(scores) + 1}: ").strip()
        if raw == "":
            break
        try:
            amount = int(raw)
        except ValueError:
            print("    (not a number -- skipped)")
            continue
        record_gain(scores, amount)

    print()
    print(build_summary(name, level, scores))


if __name__ == "__main__":
    main()

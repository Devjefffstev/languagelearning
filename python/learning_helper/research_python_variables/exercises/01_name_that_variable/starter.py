"""Exercise 01 -- Name That Variable.

You don't need to import anything. Just edit the two lists below and
run the file. It prints your answers next to the originals.

Run with: python3 starter.py
"""

# Eight variable names with problems. The format is:
#   (original, what_is_wrong, your_fixed_name)
#
# 1. Fill in WHAT_IS_WRONG for each -- one short sentence.
# 2. Fill in FIXED_NAME with a legal, idiomatic alternative.
#
# TODO: complete the two lists below.
PROBLEMS = [
    # (original,            diagnosis,                       fixed_name)
    ("2nd_attempt",         "",                              ""),
    ("user-name",           "",                              ""),
    ("class",               "",                              ""),
    ("l",                   "",                              ""),
    ("O",                   "",                              ""),
    ("UserName",            "",                              ""),
    ("n",                   "",                              ""),
    ("MAX_RETRIES",         "",                              ""),
]


def review() -> None:
    """Print each original alongside your diagnosis and your fix."""
    print(f"{'original':<14} {'diagnosis':<48} {'fixed':<14}")
    print("-" * 78)
    for original, diagnosis, fixed in PROBLEMS:
        print(f"{original:<14} {diagnosis:<48} {fixed:<14}")


if __name__ == "__main__":
    review()

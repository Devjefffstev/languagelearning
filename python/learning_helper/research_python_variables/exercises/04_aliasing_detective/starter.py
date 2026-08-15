"""Exercise 04 -- Aliasing Detective.

Predict the output of each snippet in Part A, then run the file to check.
Fix the two aliasing bugs in Part B.

Run with: python3 starter.py
"""

# ---------------------------------------------------------------------------
# Part A -- Predict the output
# ---------------------------------------------------------------------------
#
# Six snippets. For each, write the EXACT text you expect to be printed.
# Hint: run the file once before filling in PREDICTIONS to see how the
# grader works -- but the real exercise is doing it on paper first.
#
# TODO: fill in PREDICTIONS with one string per snippet, in order.
PREDICTIONS = [
    "",   # snippet 1
    "",   # snippet 2
    "",   # snippet 3
    "",   # snippet 4
    "",   # snippet 5
    "",   # snippet 6
]


def snippet_1() -> str:
    """Two ints with the same value. CPython interns small ints."""
    a = 7
    b = 7
    return f"{a == b} / {a is b}"


def snippet_2() -> str:
    """Two names, one list. Mutation through one name is visible through the other."""
    a = [1, 2, 3]
    b = a
    b.append(4)
    return f"a={a}  b={b}"


def snippet_3() -> str:
    """int += rebinds; list += mutates in place."""
    a = 10
    b = a
    b += 1            # ints are immutable, so this rebinds b to a new int

    c = [10]
    d = c
    d += [1]          # lists are mutable; += is shorthand for d.extend([1])

    return f"a={a} b={b}  c={c} d={d}"


def snippet_4() -> str:
    """Slicing a list makes a SHALLOW COPY. The new list is its own object."""
    original = [1, 2, 3]
    copy = original[:]      # new list, same element references
    copy.append(4)
    return f"original={original}  copy={copy}"


def snippet_5() -> str:
    """is None is the idiomatic check for the None singleton."""
    maybe_value = None
    return (
        f"maybe_value is None -> {maybe_value is None}  "
        f"|  maybe_value == None -> {maybe_value == None}"
    )


def snippet_6() -> str:
    """Tuple of ints vs tuple of lists -- immutability is shallow."""
    t = (1, 2, [3, 4])
    t[2].append(5)          # the tuple itself is immutable, but its list member is not
    return f"t={t}"


SNIPPETS = [snippet_1, snippet_2, snippet_3, snippet_4, snippet_5, snippet_6]


def grade_part_a() -> None:
    print("Part A -- predictions vs actual output")
    print("-" * 60)
    correct = 0
    for i, snippet in enumerate(SNIPPETS, start=1):
        actual = snippet()
        predicted = PREDICTIONS[i - 1]
        match = predicted.strip() == actual.strip()
        correct += int(match)
        marker = "OK " if match else "X  "
        print(f"{marker} #{i}")
        print(f"     predicted: {predicted!r}")
        print(f"     actual   : {actual!r}")
    print(f"\n{correct}/{len(SNIPPETS)} correct")


# ---------------------------------------------------------------------------
# Part B -- Fix the aliasing bugs
# ---------------------------------------------------------------------------


def strip_nicknames(names: list[str], nicknames: set[str]) -> list[str]:
    """Return a NEW list with any name that's in `nicknames` removed.

    The caller MUST NOT see their original list mutated. The current
    implementation uses .pop(), which mutates the caller's list in place
    because lists are mutable and the parameter `names` is just another
    sticky note on the same list object.
    """
    # TODO: rewrite so that the caller's list is not modified.
    # Hint: iterate, build a new list, return it.
    for nickname in nicknames:
        while nickname in names:
            names.pop(names.index(nickname))
    return names


def add_to_each(values: list[int]) -> int:
    """Return the SUM of the integers in `values`.

    The caller MUST NOT see their original list mutated.
    """
    # TODO: fix the return-value bug.
    # The function correctly computes `total` as it loops, but the
    # last line returns the *input list* instead of `total`. That's an
    # aliasing-style bug: the caller gets back the same object they
    # passed in, so `result == 6` will be False (it's a list).
    total = 0
    for v in values:
        total = total + v
    return values


def grade_part_b() -> None:
    print("\nPart B -- aliasing bug fixes")
    print("-" * 60)

    # Test 1: strip_nicknames
    call_list = ["alice", "bob", "carol"]
    result = strip_nicknames(call_list, {"bob"})
    ok1 = result == ["alice", "carol"] and call_list == ["alice", "bob", "carol"]
    marker = "OK " if ok1 else "X  "
    print(f"{marker} strip_nicknames: returned {result}, caller's list now {call_list}")
    if not ok1:
        print("     expected: returned ['alice', 'carol'], caller's list unchanged")

    # Test 2: add_to_each
    call_list2 = [1, 2, 3]
    result2 = add_to_each(call_list2)
    ok2 = result2 == 6 and call_list2 == [1, 2, 3]
    marker = "OK " if ok2 else "X  "
    print(f"{marker} add_to_each: returned {result2}, caller's list now {call_list2}")
    if not ok2:
        print("     expected: returned 6, caller's list unchanged")


if __name__ == "__main__":
    grade_part_a()
    grade_part_b()

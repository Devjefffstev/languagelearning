"""Starter for Exercise 03 — Word Frequency Counter.

Fill in the TODO sections. Run with: python3 starter.py
"""

# A small paragraph to analyse. You can edit this to anything you like.
PARAGRAPH = (
    "Python is a programming language that lets you work quickly "
    "and integrate systems more effectively. Python is easy to learn "
    "and readable, and Python has a huge standard library."
)


def normalize(text: str) -> str:
    """TODO: return text lower-cased with end-of-word punctuation stripped."""
    # You can decide what punctuation to strip — at minimum: . , ! ? : ;
    return text.strip(".!?,:;").lower()


def count_words(text: str) -> dict:
    """TODO: split `text` into words and return a dict mapping each word to
    the number of times it appears."""
    # return {word: text.split().count(word) for word in set(text.split())}
    counts = {}
    for word in text.split():        
        counts[word] = counts.get(word, 0) + 1
        print(f"Word: {word}, Count: {counts[word]}")
    return counts


def top_n(counts: dict, n: int) -> list:
    """TODO: return the top-n (word, count) pairs sorted by count desc."""
    print(f"Counts: {counts.items()}")
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[:n]


def main() -> None:
    text = normalize(PARAGRAPH)
    counts = count_words(text)
    for word, count in top_n(counts, 5):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
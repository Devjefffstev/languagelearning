# Exercise 03 — Word Frequency Counter

## Goal

Read a paragraph of text and print the **top 5 most frequent words**, with
their counts.

## Task

Write a script that:

1. Has a paragraph of text hard-coded at the top of the file (at least 3
   sentences — see the sample below).
2. Normalizes the text: lowercase, and strip the punctuation `. , ! ? : ;`
   from the ends of words. (You don't have to strip internal punctuation
   like `don't`.)
3. Splits the text into a list of words.
4. Counts how often each word appears, using a `dict` (word → count).
5. Prints the **top 5** words by count, highest first, one per line, like:
   ```
   the: 4
   python: 3
   and: 2
   to: 2
   a: 2
   ```
   Ties can be broken in any order — Python's `sorted` is stable.

The starter file in this folder gives you the paragraph and a `TODO` for
each step.

## Hints

1. `"Hello, world!".lower()` gives `"hello, world!"`. For punctuation,
   `str.strip(chars)` removes any of those characters from **both ends**
   of a string — useful, but it won't help with `it's` (apostrophe inside).
2. The classic idiom is:
   ```python
   for word in text.split():
       counts[word] = counts.get(word, 0) + 1
   ```
   `dict.get(key, default)` returns `default` instead of raising
   `KeyError` when the key isn't there yet.
3. To sort by value (not alphabetically), pass a `key` function:
   ```python
   sorted(counts.items(), key=lambda item: item[1], reverse=True)
   # → returns a list of (word, count) tuples, highest count first
   ```
4. To take only the first `n` items from a list, use **slice notation**:
   `sorted_list[:n]`. Apply it to the result of step 3 and use the
   `n` parameter your function already receives — don't hard-code `5`.

## Success criteria

Running `python3 starter.py` on the sample paragraph in the starter file
produces **5 lines**, each shaped `word: count`, with the words sorted by
count descending. The exact counts will depend on the paragraph you write,
but the top word should appear at least 3 times and all five top words
should appear at least once.

## Stretch goals (optional)

- Strip **all** punctuation, not just at the ends of words — use
  `str.translate(str.maketrans("", "", ".,!?;:"))` on the whole text.
- Ignore common "stop words" (`the`, `a`, `of`, `and`, `to`, `is`) and
  show the top 5 of what remains.
- Print the full table, then ask the user for a word and report its count.
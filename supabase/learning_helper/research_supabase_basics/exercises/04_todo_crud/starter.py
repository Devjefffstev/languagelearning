"""
Exercise 04 (capstone) — A command-line vocabulary tracker with full CRUD.

Prereqs: run examples/setup_complete.sql, activate .venv at the guide
root, and have your .env there (copy .env.example and fill it in).

The menu loop is provided. Your job is to implement each action function
where the TODO markers are. Keep each function small and test it from the
menu as you go.
"""

import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()  # reads SUPABASE_URL / SUPABASE_KEY from the .env file
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

MENU = """
========================================
 Vocabulary tracker — choose an action
========================================
 1) Add a word (or update it if it already exists)
 2) List all words
 3) Mark a word as learned
 4) Delete a word
 5) Show stats per language
 6) Quit
"""


def add_word() -> None:
    """Ask for word, translation, language; upsert into words."""
    word = input("word: ").strip()
    translation = input("translation: ").strip()
    language = input("language: ").strip()
    # TODO 1: upsert {"word": ..., "translation": ..., "language": ...}
    # with on_conflict="word", then print a confirmation.


def list_words() -> None:
    """Print every row, ordered by language then word."""
    # TODO 2: select all, ordered with .order("language,word").
    # Print each row as: [x] language — word (translation) when learned,
    # or [ ] language — word (translation) when not learned.


def mark_learned() -> None:
    """Ask for a word and set learned = True."""
    word = input("word to mark as learned: ").strip()
    # TODO 3: update {"learned": True} where word matches; print confirmation


def delete_word() -> None:
    """Ask for a word and delete it."""
    word = input("word to delete: ").strip()
    # TODO 4: delete where .eq("word", ...); print confirmation


def show_stats() -> None:
    """Call the word_stats() Postgres function and print per-language rows."""
    # TODO 5: use supabase.rpc("word_stats") and print each row


def main() -> None:
    actions = {
        "1": add_word,
        "2": list_words,
        "3": mark_learned,
        "4": delete_word,
        "5": show_stats,
    }
    while True:
        print(MENU)
        choice = input("> ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action()


if __name__ == "__main__":
    main()

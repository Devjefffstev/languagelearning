"""Starter for Exercise 02 — Grade Classifier.

Fill in the TODO sections. Run with: python3 starter.py
"""


def classify(score: int) -> str:
    """TODO: return the letter grade for the given numeric score.

    Use the scale:
        90-100 -> 'A'
        80-89  -> 'B'
        70-79  -> 'C'
        60-69  -> 'D'
         0-59  -> 'F'
    """
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def main() -> None:
    raw = input("Enter a score (0-100): ")

    # TODO: convert `raw` to an int safely. If the user typed something
    #       non-numeric, print a friendly error and return.
    try: 
        score = int(raw)
    except ValueError: 
        print("Error: Please enter a valid numeric score.")
    
    # TODO: check the score is in the 0-100 range. If not, print an error
    #       and return.
    if score < 0 or score > 100: 
        print("Error: Score must be between 0 and 100.")
    else:     
    # TODO: call classify(score) and print "Score <score> -> <letter>".
        letter_grade = classify(score)
        print(f"Score {score} -> {letter_grade}")

if __name__ == "__main__":
    main()
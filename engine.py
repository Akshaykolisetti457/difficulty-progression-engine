"""
Difficulty Progression Engine
==============================
Determines the next question's difficulty level based on a user's
answered question history.

Progression Rule:
    Easy -> Easy -> Medium -> Medium -> Hard

Author : Akshay
Python : 3.13+
"""

from typing import Optional


# ------------------------------------------------------------------
# Configuration — change this to update progression rules easily
# ------------------------------------------------------------------
PROGRESSION: dict[int, str] = {
    0: "Easy",
    1: "Easy",
    2: "Medium",
    3: "Medium",
}
DEFAULT_DIFFICULTY: str = "Hard"   # applied when answered count >= 4


# ------------------------------------------------------------------
# Core functions
# ------------------------------------------------------------------

def is_valid_answer(question: dict) -> bool:
    """
    Returns True only if a question was genuinely answered.

    Skipped  (answered=False) -> invalid
    Missing  (answered=None)  -> invalid
    Answered (answered=True)  -> valid

    Args:
        question (dict): A single question record.

    Returns:
        bool
    """
    return question.get("answered") is True


def count_valid_answers(question_history: list) -> int:
    """
    Counts questions that were actually answered (not skipped or missing).

    Args:
        question_history (list): List of question dicts.

    Returns:
        int: Number of valid answered questions.
    """
    return sum(1 for q in question_history if is_valid_answer(q))


def get_next_difficulty(question_history: Optional[list] = None) -> dict:
    """
    Determines the difficulty level for the next question.

    Args:
        question_history (list | None): List of question dicts. Each dict:
            {
                "question_id" : int,
                "difficulty"  : "Easy" | "Medium" | "Hard",
                "answered"    : True | False | None
            }

    Returns:
        dict: { "next_question_level": "Easy" | "Medium" | "Hard" }

    Examples:
        >>> get_next_difficulty([])
        {'next_question_level': 'Easy'}

        >>> get_next_difficulty([
        ...     {"question_id": 1, "difficulty": "Easy", "answered": True},
        ...     {"question_id": 2, "difficulty": "Easy", "answered": True},
        ... ])
        {'next_question_level': 'Medium'}
    """
    if not question_history:
        return {"next_question_level": PROGRESSION[0]}

    valid_count = count_valid_answers(question_history)
    next_level  = PROGRESSION.get(valid_count, DEFAULT_DIFFICULTY)

    return {"next_question_level": next_level}


# ------------------------------------------------------------------
# CLI demo  (python engine.py)
# ------------------------------------------------------------------
if __name__ == "__main__":
    import json

    scenarios = [
        {
            "label"  : "No history — very first question",
            "history": [],
        },
        {
            "label"  : "1 answered -> still Easy",
            "history": [
                {"question_id": 1, "difficulty": "Easy", "answered": True},
            ],
        },
        {
            "label"  : "2 answered -> Medium unlocked",
            "history": [
                {"question_id": 1, "difficulty": "Easy", "answered": True},
                {"question_id": 2, "difficulty": "Easy", "answered": True},
            ],
        },
        {
            "label"  : "3 answered -> still Medium",
            "history": [
                {"question_id": 1, "difficulty": "Easy",   "answered": True},
                {"question_id": 2, "difficulty": "Easy",   "answered": True},
                {"question_id": 3, "difficulty": "Medium", "answered": True},
            ],
        },
        {
            "label"  : "4 answered -> Hard unlocked",
            "history": [
                {"question_id": 1, "difficulty": "Easy",   "answered": True},
                {"question_id": 2, "difficulty": "Easy",   "answered": True},
                {"question_id": 3, "difficulty": "Medium", "answered": True},
                {"question_id": 4, "difficulty": "Medium", "answered": True},
            ],
        },
        {
            "label"  : "1 answered + 1 SKIPPED -> still Easy",
            "history": [
                {"question_id": 1, "difficulty": "Easy", "answered": True},
                {"question_id": 2, "difficulty": "Easy", "answered": False},
            ],
        },
        {
            "label"  : "1 answered + 1 MISSING -> still Easy",
            "history": [
                {"question_id": 1, "difficulty": "Easy", "answered": True},
                {"question_id": 2, "difficulty": "Easy", "answered": None},
            ],
        },
        {
            "label"  : "All skipped -> stays Easy",
            "history": [
                {"question_id": 1, "difficulty": "Easy", "answered": False},
                {"question_id": 2, "difficulty": "Easy", "answered": False},
            ],
        },
        {
            "label"  : "Mixed: 2 answered + 3 skipped/missing -> Medium",
            "history": [
                {"question_id": 1, "answered": True},
                {"question_id": 2, "answered": False},
                {"question_id": 3, "answered": None},
                {"question_id": 4, "answered": True},
                {"question_id": 5, "answered": None},
            ],
        },
    ]

    ICONS = {"Easy": "[EASY]", "Medium": "[MED] ", "Hard": "[HARD]"}

    print("\n" + "=" * 62)
    print("   DIFFICULTY PROGRESSION ENGINE - Demo Run")
    print("=" * 62)

    for s in scenarios:
        result = get_next_difficulty(s["history"])
        level  = result["next_question_level"]
        print(f"\n  {ICONS[level]} Next: {level:8s} | {s['label']}")

    print("\n" + "-" * 62)
    print("  Sample JSON output:")
    sample = get_next_difficulty([
        {"question_id": 1, "difficulty": "Easy", "answered": True},
        {"question_id": 2, "difficulty": "Easy", "answered": True},
    ])
    print(f"  {json.dumps(sample, indent=2)}")
    print("=" * 62 + "\n")

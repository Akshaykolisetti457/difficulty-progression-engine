# Difficulty Progression Engine

A lightweight Python engine that determines the next question's difficulty level
based on a user's answered question history — handling skipped and missing answers cleanly.

**Author:** Akshay  
**Python:** 3.13+  
**Project:** B11 — Difficulty Progression Engine

---

## Progression Rule

```
Easy → Easy → Medium → Medium → Hard
```

| Answered Questions | Next Difficulty |
|--------------------|-----------------|
| 0                  | Easy            |
| 1                  | Easy            |
| 2                  | Medium          |
| 3                  | Medium          |
| 4+                 | Hard            |

> Skipped (`answered: False`) and missing (`answered: None`) questions
> are **excluded** from the count and do not advance the progression.

---

## Project Structure

```
difficulty_progression_engine/
├── engine.py          # Core engine logic
├── test_engine.py     # Unit tests (23 test cases)
├── requirements.txt   # Dependencies
└── README.md          # This file
```

---

## Setup & Installation

```bash
# 1. Clone or download the project
cd difficulty_progression_engine

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```python
from engine import get_next_difficulty

history = [
    {"question_id": 1, "difficulty": "Easy", "answered": True},
    {"question_id": 2, "difficulty": "Easy", "answered": True},
]

result = get_next_difficulty(history)
print(result)
# Output: {"next_question_level": "Medium"}
```

### Input Format

Each question in the history is a dict:

```python
{
    "question_id" : int,          # unique identifier
    "difficulty"  : str,          # "Easy" | "Medium" | "Hard"
    "answered"    : bool | None   # True = answered, False = skipped, None = missing
}
```

### Output Format

```json
{ "next_question_level": "Medium" }
```

---

## Edge Cases Handled

| Scenario | Behaviour |
|----------|-----------|
| Empty history | Returns `Easy` (first question) |
| `None` input | Returns `Easy` (treated as empty) |
| Skipped questions (`answered: False`) | Excluded from count, do not advance progression |
| Missing answers (`answered: None`) | Excluded from count, do not advance progression |
| All questions skipped | Returns `Easy` |
| Mixed answered + skipped | Only counts genuinely answered questions |

---

## Run the Demo

```bash
python engine.py
```

Sample output:

```
[EASY]  Next: Easy     | No history — very first question
[EASY]  Next: Easy     | 1 answered -> still Easy
[MED]   Next: Medium   | 2 answered -> Medium unlocked
[HARD]  Next: Hard     | 4 answered -> Hard unlocked
[EASY]  Next: Easy     | 1 answered + 1 SKIPPED -> still Easy
```

---

## Run the Tests

```bash
pytest test_engine.py -v
```

```
PASSED  TestIsValidAnswer::test_true_is_valid
PASSED  TestIsValidAnswer::test_false_is_not_valid
PASSED  TestIsValidAnswer::test_none_is_not_valid
PASSED  TestIsValidAnswer::test_missing_key_is_not_valid
PASSED  TestCountValidAnswers::test_empty_history_returns_zero
...
23 passed in 0.XXs
```

---

## Design Decisions

- **Dict-based progression map** — makes rules easy to read and modify without touching logic
- **`.get()` with default** — handles Hard (4+) automatically without extra if-else
- **Bottom-up design** — three focused functions, each testable independently
- **Skipped ≠ Missing** — both are invalid but distinguished at input level for clarity

---

## License

MIT

"""
Unit Tests — Difficulty Progression Engine
===========================================
Run with:  pytest test_engine.py -v

Author : Akshay
Python : 3.13+
"""

import pytest
from engine import get_next_difficulty, count_valid_answers, is_valid_answer


# ══════════════════════════════════════════════════════════════════
# is_valid_answer
# ══════════════════════════════════════════════════════════════════

class TestIsValidAnswer:
    """Tests for the low-level answer validator."""

    def test_true_is_valid(self):
        # Arrange
        question = {"answered": True}
        # Act + Assert
        assert is_valid_answer(question) is True

    def test_false_is_not_valid(self):
        # Arrange
        question = {"answered": False}
        # Act + Assert
        assert is_valid_answer(question) is False

    def test_none_is_not_valid(self):
        # Arrange
        question = {"answered": None}
        # Act + Assert
        assert is_valid_answer(question) is False

    def test_missing_key_is_not_valid(self):
        # Arrange
        question = {}
        # Act + Assert
        assert is_valid_answer(question) is False


# ══════════════════════════════════════════════════════════════════
# count_valid_answers
# ══════════════════════════════════════════════════════════════════

class TestCountValidAnswers:
    """Tests for the valid-answer counter."""

    def test_empty_history_returns_zero(self):
        assert count_valid_answers([]) == 0

    def test_all_answered(self):
        history = [{"answered": True}, {"answered": True}, {"answered": True}]
        assert count_valid_answers(history) == 3

    def test_all_skipped_returns_zero(self):
        history = [{"answered": False}, {"answered": False}]
        assert count_valid_answers(history) == 0

    def test_all_missing_returns_zero(self):
        history = [{"answered": None}, {"answered": None}]
        assert count_valid_answers(history) == 0

    def test_mixed_counts_only_answered(self):
        history = [
            {"answered": True},
            {"answered": False},
            {"answered": None},
            {"answered": True},
        ]
        assert count_valid_answers(history) == 2


# ══════════════════════════════════════════════════════════════════
# get_next_difficulty — happy path
# ══════════════════════════════════════════════════════════════════

class TestProgressionHappyPath:
    """Tests for the standard Easy -> Medium -> Hard progression."""

    def test_no_history_returns_easy(self):
        assert get_next_difficulty([]) == {"next_question_level": "Easy"}

    def test_none_input_returns_easy(self):
        assert get_next_difficulty(None) == {"next_question_level": "Easy"}

    def test_after_1_answered_returns_easy(self):
        # Arrange
        history = [{"question_id": 1, "difficulty": "Easy", "answered": True}]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Easy"}

    def test_after_2_answered_returns_medium(self):
        # Arrange
        history = [
            {"question_id": 1, "difficulty": "Easy", "answered": True},
            {"question_id": 2, "difficulty": "Easy", "answered": True},
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Medium"}

    def test_after_3_answered_returns_medium(self):
        # Arrange
        history = [
            {"question_id": 1, "difficulty": "Easy",   "answered": True},
            {"question_id": 2, "difficulty": "Easy",   "answered": True},
            {"question_id": 3, "difficulty": "Medium", "answered": True},
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Medium"}

    def test_after_4_answered_returns_hard(self):
        # Arrange
        history = [
            {"question_id": 1, "difficulty": "Easy",   "answered": True},
            {"question_id": 2, "difficulty": "Easy",   "answered": True},
            {"question_id": 3, "difficulty": "Medium", "answered": True},
            {"question_id": 4, "difficulty": "Medium", "answered": True},
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Hard"}

    def test_after_10_answered_stays_hard(self):
        history = [{"answered": True}] * 10
        assert get_next_difficulty(history) == {"next_question_level": "Hard"}


# ══════════════════════════════════════════════════════════════════
# get_next_difficulty — skipped questions
# ══════════════════════════════════════════════════════════════════

class TestSkippedQuestions:
    """Skipped questions must NOT advance the progression."""

    def test_one_answered_one_skipped_stays_easy(self):
        # Arrange
        history = [
            {"question_id": 1, "difficulty": "Easy", "answered": True},
            {"question_id": 2, "difficulty": "Easy", "answered": False},  # skipped
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Easy"}

    def test_all_skipped_stays_easy(self):
        # Arrange
        history = [
            {"question_id": 1, "answered": False},
            {"question_id": 2, "answered": False},
            {"question_id": 3, "answered": False},
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Easy"}

    def test_skipped_does_not_push_to_medium(self):
        # Arrange — 1 answered + many skipped; should still be Easy
        history = [
            {"question_id": 1, "answered": True},
            {"question_id": 2, "answered": False},
            {"question_id": 3, "answered": False},
            {"question_id": 4, "answered": False},
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Easy"}


# ══════════════════════════════════════════════════════════════════
# get_next_difficulty — missing answers
# ══════════════════════════════════════════════════════════════════

class TestMissingAnswers:
    """Missing (None) answers must NOT advance the progression."""

    def test_one_answered_one_missing_stays_easy(self):
        # Arrange
        history = [
            {"question_id": 1, "difficulty": "Easy", "answered": True},
            {"question_id": 2, "difficulty": "Easy", "answered": None},  # missing
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Easy"}

    def test_all_missing_stays_easy(self):
        # Arrange
        history = [{"answered": None}] * 5
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Easy"}


# ══════════════════════════════════════════════════════════════════
# get_next_difficulty — mixed edge cases
# ══════════════════════════════════════════════════════════════════

class TestMixedEdgeCases:
    """Mixed combinations of answered, skipped, and missing."""

    def test_2_answered_3_skipped_returns_medium(self):
        # Arrange
        history = [
            {"question_id": 1, "answered": True},
            {"question_id": 2, "answered": False},
            {"question_id": 3, "answered": None},
            {"question_id": 4, "answered": True},
            {"question_id": 5, "answered": None},
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Medium"}

    def test_4_answered_with_gaps_returns_hard(self):
        # Arrange — 4 valid answers scattered among skipped
        history = [
            {"question_id": 1, "answered": True},
            {"question_id": 2, "answered": False},
            {"question_id": 3, "answered": True},
            {"question_id": 4, "answered": None},
            {"question_id": 5, "answered": True},
            {"question_id": 6, "answered": False},
            {"question_id": 7, "answered": True},
        ]
        # Act
        result = get_next_difficulty(history)
        # Assert
        assert result == {"next_question_level": "Hard"}


# ══════════════════════════════════════════════════════════════════
# Output contract
# ══════════════════════════════════════════════════════════════════

class TestOutputContract:
    """Ensures the output always matches the required JSON structure."""

    def test_output_has_correct_key(self):
        result = get_next_difficulty([])
        assert "next_question_level" in result

    def test_output_value_is_always_valid_difficulty(self):
        valid_levels = {"Easy", "Medium", "Hard"}
        for n in range(8):
            history = [{"answered": True}] * n
            result = get_next_difficulty(history)
            assert result["next_question_level"] in valid_levels

    def test_output_is_dict(self):
        result = get_next_difficulty([])
        assert isinstance(result, dict)

    def test_output_has_exactly_one_key(self):
        result = get_next_difficulty([])
        assert len(result) == 1

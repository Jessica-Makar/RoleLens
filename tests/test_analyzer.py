
import pytest

from src.claude_analyzer import validate_analysis


def create_valid_analysis():
    return {
        "match_score": 75,
        "score_breakdown": {
            "technical_skills": 30,
            "experience": 20,
            "education": 15,
            "other_requirements": 10
        }
    }


def test_valid_analysis():

    analysis = create_valid_analysis()

    result = validate_analysis(analysis)

    assert result["match_score"] == 75


def test_invalid_technical_score():

    analysis = create_valid_analysis()

    analysis["score_breakdown"]["technical_skills"] = 45

    with pytest.raises(ValueError):
        validate_analysis(analysis)


def test_invalid_total_score():

    """Verify that Python calculates the overall score."""

    analysis = {
        "score_breakdown": {
            "technical_skills": 20,
            "experience": 15,
            "education": 10,
            "other_requirements": 5
        }
    }

    result = validate_analysis(analysis)

    assert result["match_score"] == 50


def test_invalid_negative_score():

    analysis = create_valid_analysis()

    analysis["score_breakdown"]["experience"] = -5

    with pytest.raises(ValueError):
        validate_analysis(analysis)


from src.claude_analyzer import validate_skill_classifications


def create_analysis():
    """Create a sample analysis for validation tests."""

    return {
        "matching_skills": ["Python", "SQL"],
        "verified_skills": [
            {
                "skill": "Python",
                "evidence": "Used Python in a data pipeline project."
            }
        ],
        "unverified_skills": [
            {
                "skill": "SQL",
                "explanation": "Listed in skills but not demonstrated."
            }
        ],
        "missing_skills": ["AWS"]
    }


def test_valid_skill_classifications():
    """Verify that consistent classifications produce no warnings."""

    analysis = create_analysis()

    warnings = validate_skill_classifications(analysis)

    assert warnings == []


def test_overlapping_skill_classifications():
    """Verify that a skill cannot be both verified and unverified."""

    analysis = create_analysis()

    analysis["unverified_skills"].append({
        "skill": "Python",
        "explanation": "Listed without supporting evidence."
    })

    warnings = validate_skill_classifications(analysis)

    assert any("both verified and unverified" in warning for warning in warnings)


def test_unclassified_matching_skill():
    """Verify that matching skills must have a classification."""

    analysis = create_analysis()

    analysis["matching_skills"].append("PostgreSQL")

    warnings = validate_skill_classifications(analysis)

    assert any("missing from verified_skills" in warning for warning in warnings)


def test_matching_and_missing_conflict():
    """Verify that a skill cannot be both matching and missing."""

    analysis = create_analysis()

    analysis["missing_skills"].append("Python")

    warnings = validate_skill_classifications(analysis)

    assert any("both matching_skills and missing_skills" in warning for warning in warnings)


def test_duplicate_verified_skills():
    """Verify that duplicate verified skills are detected."""

    analysis = create_analysis()

    analysis["verified_skills"].append({
        "skill": "Python",
        "evidence": "Used Python in another project."
    })

    warnings = validate_skill_classifications(analysis)

    assert any("Duplicate skills found in verified_skills" in warning for warning in warnings)

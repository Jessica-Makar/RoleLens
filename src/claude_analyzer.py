
import os
import json

from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic, APIError


# Load environment variables
PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


# Define the expected JSON structure
ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        
        "score_breakdown": {
            "type": "object",
            "properties": {
                "technical_skills": {"type": "integer"},
                "experience": {"type": "integer"},
                "education": {"type": "integer"},
                "other_requirements": {"type": "integer"}
            },
            "required": [
                "technical_skills",
                "experience",
                "education",
                "other_requirements"
            ],
            "additionalProperties": False
        },

        "matching_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "verified_skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "skill": {"type": "string"},
                    "evidence": {"type": "string"}
                },
                "required": ["skill", "evidence"],
                "additionalProperties": False
            }
        },
        "unverified_skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "skill": {"type": "string"},
                    "explanation": {"type": "string"}
                },
                "required": ["skill", "explanation"],
                "additionalProperties": False
            }
        },
        "missing_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "relevant_experience": {
            "type": "array",
            "items": {"type": "string"}
        },
        "strengths": {
            "type": "array",
            "items": {"type": "string"}
        },
        "areas_for_improvement": {
            "type": "array",
            "items": {"type": "string"}
        },
        "recommendations": {
            "type": "array",
            "items": {"type": "string"}
        },
        "score_explanation": {
            "type": "string"
        }
    },
    "required": [
        "score_breakdown",
        "matching_skills",
        "verified_skills",
        "unverified_skills",
        "missing_skills",
        "relevant_experience",
        "strengths",
        "areas_for_improvement",
        "recommendations",
        "score_explanation"
    ],
    "additionalProperties": False
}

def normalize_skill_name(skill):
    """Normalize skill names for consistency comparisons."""
    return " ".join(skill.lower().strip().split())


def validate_skill_classifications(analysis):
    """
    Check consistency between matching, verified,
    and unverified skills.

    Returns warnings instead of raising errors so that
    a minor classification inconsistency does not
    prevent the user from receiving an analysis.
    """

    warnings = []

    matching_skills = analysis["matching_skills"]
    verified_skills = analysis["verified_skills"]
    unverified_skills = analysis["unverified_skills"]

    # Extract skill names from the structured objects.
    verified_names = [
        item["skill"] for item in verified_skills
    ]

    unverified_names = [
        item["skill"] for item in unverified_skills
    ]

    # Normalize names for comparisons.
    matching_set = {
        normalize_skill_name(skill)
        for skill in matching_skills
    }

    verified_set = {
        normalize_skill_name(skill)
        for skill in verified_names
    }

    unverified_set = {
        normalize_skill_name(skill)
        for skill in unverified_names
    }

    # Check whether a skill appears in both classifications.
    overlapping_skills = verified_set.intersection(
        unverified_set
    )

    if overlapping_skills:
        warnings.append(
            "Some skills appear in both verified and "
            f"unverified lists: {sorted(overlapping_skills)}"
        )

    # Check for duplicate entries.
    if len(verified_set) != len(verified_names):
        warnings.append(
            "Duplicate skills found in verified_skills."
        )

    if len(unverified_set) != len(unverified_names):
        warnings.append(
            "Duplicate skills found in unverified_skills."
        )

    if len(matching_set) != len(matching_skills):
        warnings.append(
            "Duplicate skills found in matching_skills."
        )

    # Every matching skill should also have a classification.
    classified_set = verified_set.union(unverified_set)

    unclassified_matching = matching_set - classified_set

    if unclassified_matching:
        warnings.append(
            "Matching skills missing from verified_skills "
            "and unverified_skills: "
            f"{sorted(unclassified_matching)}"
        )

    # A skill should not be both matching and missing
    # from the resume.
    missing_set = {
        normalize_skill_name(skill)
        for skill in analysis["missing_skills"]
    }

    conflicting_skills = matching_set.intersection(missing_set)

    if conflicting_skills:
        warnings.append(
            "Some skills appear in both matching_skills "
            "and missing_skills: "
            f"{sorted(conflicting_skills)}"
        )

    return warnings

def validate_analysis(analysis):
    """
    Validate category scores, calculate the overall
    match score, and check skill classification consistency.
    """

    score_breakdown = analysis["score_breakdown"]

    score_limits = {
        "technical_skills": 40,
        "experience": 30,
        "education": 15,
        "other_requirements": 15
    }

    for category, maximum in score_limits.items():

        score = score_breakdown[category]

        if type(score) is not int or not 0 <= score <= maximum:
            raise ValueError(
                f"Invalid score for {category}: {score}. "
                f"Expected a value between 0 and {maximum}."
            )

    # Calculate the overall match score.
    analysis["match_score"] = sum(score_breakdown.values())

    # Check skill classifications only when skill fields exist.
    required_skill_fields = [
        "matching_skills",
        "verified_skills",
        "unverified_skills",
        "missing_skills"
    ]

    if all(field in analysis for field in required_skill_fields):

        analysis["skill_validation_warnings"] = (
            validate_skill_classifications(analysis)
        )

    return analysis

def analyze_resume(resume_text, job_description):
    """Analyze a resume against a job description using Claude."""

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("Anthropic API key not found.")

    # Load analysis instructions
    prompt_path = PROJECT_ROOT / "prompts" / "resume_analysis.txt"

    with open(prompt_path, "r", encoding="utf-8") as file:
        system_prompt = file.read()

    client = Anthropic(api_key=api_key)

    user_prompt = f"""
    Analyze the following resume against the job description.

    RESUME:
    <resume>
    {resume_text}
    </resume>

    JOB DESCRIPTION:
    <job_description>
    {job_description}
    </job_description>

    Follow the analysis instructions and return the
    requested structured results.
    """

    try:
        message = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=5000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": ANALYSIS_SCHEMA
                }
            }
        )

        # Check whether Claude completed its response.
        if message.stop_reason == "max_tokens":
            raise RuntimeError(
                "Claude reached its output token limit. "
                "Try increasing max_tokens."
            )

        # Extract the response text.
        response_text = "".join(
            block.text
            for block in message.content
            if block.type == "text"
        )

        if not response_text:
            raise RuntimeError(
                "Claude returned an empty response."
            )

        # Parse Claude's JSON response.
        try:
            analysis = json.loads(response_text)

        except json.JSONDecodeError as error:
            raise RuntimeError(
                "Claude returned invalid JSON. "
                f"Error at line {error.lineno}, "
                f"column {error.colno}. "
                f"Stop reason: {message.stop_reason}."
            ) from error

        analysis = validate_analysis(analysis)

        return analysis

    except APIError as error:
        raise RuntimeError(
            f"Claude API request failed: {error}"
        ) from error

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "JSON decoding failed outside the response parsing block. "
            f"Error at line {error.lineno}, "
            f"column {error.colno}. "
            f"Details: {error.msg}"
        ) from error

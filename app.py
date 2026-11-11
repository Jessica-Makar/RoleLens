import json
import streamlit as st

from src.resume_parser import extract_resume_text
from src.claude_analyzer import analyze_resume
from src.report_generator import generate_pdf_report
from src.branding import (
    BRAND_NAME,
    BRAND_TAGLINE,
    BRAND_DESCRIPTION,
)


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="RoleLens | AI Career Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=swap'
        );

        .stApp {
            background-color: #080D1A;
            color: #F8FAFC;
        }

        .block-container {
            max-width: 1150px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        html, body, [class*="css"] {
            font-family: 'Sora', sans-serif;
        }

        h1, h2, h3, h4 {
            color: #F8FAFC !important;
            font-family: 'Sora', sans-serif !important;
            font-weight: 700 !important;
        }

        p, label, li {
            color: #E2E8F0;
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 18px;
            width: 100%;
            min-height: 85px;
            padding: 12px 0;
            margin-bottom: 8px;
            overflow: visible;
        }

        .brand-icon {
            width: 65px;
            height: 65px;
            min-width: 65px;
            flex: 0 0 65px;
            border-radius: 18px;
            background: linear-gradient(135deg, #2563EB, #8B5CF6);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-family: 'Sora', sans-serif;
            font-size: 34px;
            font-weight: 800;
        }

        .brand {
            display: block;
            font-family: 'Sora', sans-serif;
            font-size: 54px;
            font-weight: 800;
            color: #F8FAFC;
            letter-spacing: -2px;
            line-height: 1.4;
            padding: 3px 0 8px;
            white-space: nowrap;
            overflow: visible;
        }

        .subtitle {
            color: #94A3B8;
            font-size: 15px;
            font-weight: 400;
            margin-top: 5px;
            margin-bottom: 30px;
        }

        .info-card, .score-card {
            background: #111B2E;
            border: 1px solid #263449;
            border-radius: 14px;
            padding: 22px;
        }

        .stButton > button {
            background: linear-gradient(110deg, #2563EB, #7C3AED);
            color: #FFFFFF;
            border: none;
            border-radius: 9px;
            font-weight: 700;
            padding: 12px 20px;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(110deg, #3B82F6, #8B5CF6);
            color: #FFFFFF;
            border: none;
            box-shadow: 0 4px 18px rgba(37, 99, 235, 0.3);
        }

        .stTextArea textarea {
            background-color: #111B2E;
            color: #F8FAFC;
            border: 1px solid #334155;
            border-radius: 9px;
        }

        .stTextArea textarea:focus {
            border-color: #3B82F6;
        }

        .stTextArea textarea::placeholder {
            color: #94A3B8;
        }

        [data-testid="stFileUploader"] {
            background-color: #111B2E;
            border: 1px solid #263449;
            border-radius: 12px;
            padding: 12px;
        }

        [data-testid="stMetric"] {
            background-color: #111B2E;
            border: 1px solid #263449;
            border-radius: 12px;
            padding: 18px;
        }

        [data-testid="stMetricValue"] {
            color: #60A5FA;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            color: #94A3B8;
        }

        .stTabs [aria-selected="true"] {
            color: #60A5FA !important;
        }

        .stProgress > div > div > div {
            background: linear-gradient(90deg, #2563EB, #8B5CF6);
        }

        hr {
            border-color: #263449;
        }

        .score-ring {
            width: 190px;
            height: 190px;
            min-width: 190px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 15px auto;
        }

        .score-ring-inner {
            width: 155px;
            height: 155px;
            border-radius: 50%;
            background: #111B2E;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        .score-ring-value {
            font-family: 'Sora', sans-serif;
            font-size: 38px;
            font-weight: 800;
            color: #F8FAFC;
        }

        .score-ring-label {
            font-size: 11px;
            color: #94A3B8;
            letter-spacing: 1px;
            margin-top: 4px;
        }

        .skill-evidence {
            color: #CBD5E1;
            font-size: 0.9rem;
            line-height: 1.5;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def display_skill_details(items, detail_key, empty_message):
    """
    Display skill objects returned by Claude.

    Supports the current object format and older string
    values so previously saved analyses remain displayable.
    """

    if not items:
        st.info(empty_message)
        return

    for item in items:
        if isinstance(item, dict):
            skill_name = item.get("skill", "Unspecified skill")
            detail = item.get(detail_key, "")
        else:
            skill_name = str(item)
            detail = ""

        with st.container(border=True):
            st.markdown(f"**{skill_name}**")

            if detail:
                st.markdown(
                    f'<div class="skill-evidence">{detail}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.caption("No additional explanation was provided.")


def display_skill_list(items, heading, icon, empty_message):
    """Display a simple list of skill names."""

    st.markdown(f"#### {icon} {heading}")

    if not items:
        st.info(empty_message)
        return

    for item in items:
        if isinstance(item, dict):
            skill_name = item.get("skill", "Unspecified skill")
        else:
            skill_name = str(item)

        with st.container(border=True):
            st.markdown(f"• {skill_name}")


# ==========================================
# 4. APPLICATION HEADER
# ==========================================

st.markdown(
    f"""
    <div class="brand-container">
        <div class="brand-icon">R</div>
        <div class="brand">{BRAND_NAME}</div>
    </div>
    <div class="subtitle">{BRAND_TAGLINE}</div>
    """,
    unsafe_allow_html=True,
)

st.divider()


# ==========================================
# 5. RESUME UPLOAD
# ==========================================

st.markdown("## Analyze your resume")

st.write(
    "Upload your resume and provide a job description "
    "to discover how well your qualifications align."
)

# 01 - Resume upload
st.markdown("### 01 — Your Resume")

with st.container(border=True):
    st.markdown("**Upload your resume**")

    uploaded_file = st.file_uploader(
        "Drag and drop your resume here or browse files",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX.",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        st.success(f"Uploaded: {uploaded_file.name}")

        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.caption(f"File size: {file_size_mb:.2f} MB")


# 02 - Job description
st.markdown("### 02 — Job Description")

with st.container(border=True):
    st.markdown("**Paste the complete job description**")

    job_description = st.text_area(
        "Job Description",
        placeholder=(
            "Paste the job title, responsibilities, "
            "qualifications, required skills, and "
            "other relevant details here..."
        ),
        height=250,
        label_visibility="collapsed",
    )

    st.caption(
        "Include the complete job posting for a "
        "more comprehensive analysis."
    )


# Analyze button
analyze_button = st.button(
    "🔎 Analyze My Resume →",
    use_container_width=True,
)


# ==========================================
# 6. ANALYZE RESUME
# ==========================================

if analyze_button:
    # Clear previous results before starting a new analysis.
    st.session_state.pop("analysis", None)
    st.session_state.pop("resume_filename", None)

    if uploaded_file is None:
        st.error("Please upload a resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    elif uploaded_file.size > 10 * 1024 * 1024:
        st.error("Your resume exceeds the 10 MB file limit.")

    else:
        file_type = uploaded_file.name.rsplit(".", 1)[-1].lower()

        try:
            with st.spinner(
                "Extracting resume information and analyzing with Claude..."
            ):
                uploaded_file.seek(0)

                resume_text = extract_resume_text(
                    uploaded_file,
                    file_type,
                )

                analysis = analyze_resume(
                    resume_text,
                    job_description,
                )

                st.session_state["analysis"] = analysis
                st.session_state["resume_filename"] = uploaded_file.name

            st.success("Resume analysis completed!")

        except (ValueError, RuntimeError) as error:
            st.error(str(error))

        except Exception as error:
            st.error(
                "An unexpected error occurred. "
                "Please try again. "
                f"Error details: {error}"
            )


# ==========================================
# 7. DISPLAY ANALYSIS RESULTS
# ==========================================

if "analysis" in st.session_state:
    analysis = st.session_state["analysis"]

    st.divider()
    st.header("Your Analysis Results")

    st.caption(
        f"Resume analyzed: {st.session_state['resume_filename']}"
    )

    # --------------------------------------
    # OVERVIEW METRICS
    # --------------------------------------

    match_score = int(analysis.get("match_score", 0))

    matching_skills = analysis.get("matching_skills", [])
    verified_skills = analysis.get("verified_skills", [])
    unverified_skills = analysis.get("unverified_skills", [])
    missing_skills = analysis.get("missing_skills", [])

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric("Resume Match Score", f"{match_score}/100")

    with metric2:
        st.metric("Matching Skills", len(matching_skills))

    with metric3:
        st.metric("Verified Skills", len(verified_skills))

    with metric4:
        st.metric("Skill Gaps", len(missing_skills))


    # --------------------------------------
    # CIRCULAR RESUME SCORE
    # --------------------------------------

    st.subheader("Overall Resume Alignment")

    score_col1, score_col2 = st.columns([1, 2])

    with score_col1:
        safe_score = max(0, min(100, match_score))

        score_color = (
            "#22C55E" if safe_score >= 75
            else "#F59E0B" if safe_score >= 50
            else "#EF4444"
        )

        score_html = (
            f'<div class="score-ring" '
            f'style="background: conic-gradient('
            f'{score_color} {safe_score}%, '
            f'#263449 {safe_score}% 100%);">'
            f'<div class="score-ring-inner">'
            f'<div class="score-ring-value">{safe_score}/100</div>'
            f'<div class="score-ring-label">MATCH SCORE</div>'
            f'</div></div>'
        )

        st.markdown(score_html, unsafe_allow_html=True)

    with score_col2:
        st.markdown("### Resume Match Score")
        st.markdown(f"## {safe_score}/100")

        st.write(
            "Your estimated resume alignment based on "
            "the skills, experience, education, and "
            "other requirements in the job description."
        )

        st.caption(
            "This score is not a probability of receiving "
            "an interview or job offer."
        )


    # --------------------------------------
    # SCORE BREAKDOWN
    # --------------------------------------

    st.subheader("Score Breakdown")

    score_breakdown = analysis.get("score_breakdown", {})

    score_limits = {
        "technical_skills": 40,
        "experience": 30,
        "education": 15,
        "other_requirements": 15,
    }

    score_labels = {
        "technical_skills": "Technical Skills",
        "experience": "Relevant Experience",
        "education": "Education",
        "other_requirements": "Other Requirements",
    }

    breakdown_cols = st.columns(2)

    for index, (category, score) in enumerate(score_breakdown.items()):
        maximum = score_limits.get(category)

        if maximum is None:
            continue

        label = score_labels.get(category, category.replace("_", " ").title())
        percentage = max(0.0, min(1.0, score / maximum))

        with breakdown_cols[index % 2]:
            with st.container(border=True):
                st.markdown(f"**{label}**")
                st.markdown(f"### {score}/{maximum} points")
                st.progress(percentage)
                st.caption(f"{percentage:.0%} of available points")


    # --------------------------------------
    # DETAILED ANALYSIS TABS
    # --------------------------------------

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Skills Analysis",
            "Experience & Education",
            "Resume Feedback",
            "Recommendations",
        ]
    )

    # TAB 1: SKILLS ANALYSIS
    with tab1:

        st.header("Skills Analysis")

        st.write(
            "Review which skills are supported by resume evidence, "
            "which are listed without evidence, and which job "
            "requirements are not found in the resume."
        )

        # Skill summary metrics
        skill_col1, skill_col2, skill_col3 = st.columns(3)

        with skill_col1:
            st.metric("Verified", len(verified_skills))

        with skill_col2:
            st.metric("Unverified", len(unverified_skills))

        with skill_col3:
            st.metric("Missing", len(missing_skills))

        st.divider()

        # Verified and unverified skill sections
        verified_col, unverified_col = st.columns(2, gap="large")

        with verified_col:

            st.markdown("### 🟢 Verified Skills")

            st.caption(
                "Skills supported by specific examples in the resume."
            )

            display_skill_details(
                verified_skills,
                "evidence",
                "No verified skills were identified."
            )

        with unverified_col:

            st.markdown("### 🟠 Unverified Skills")

            st.caption(
                "Skills listed in the resume without enough evidence "
                "of practical use."
            )

            display_skill_details(
                unverified_skills,
                "explanation",
                "No unverified skills were identified."
            )

        st.divider()

        # Matching skills
        display_skill_list(
            matching_skills,
            "Matching Skills",
            "🎯",
            "No matching skills were identified."
        )

        st.divider()

        # Missing requirements
        display_skill_list(
            missing_skills,
            "Missing Job Requirements",
            "🔴",
            "No missing job requirements were identified."
        )

        # Skill validation warnings
        validation_warnings = analysis.get(
            "skill_validation_warnings", []
        )

        if validation_warnings:

            st.warning(
                "RoleLens detected possible inconsistencies "
                "in the skill classifications."
            )

            for warning in validation_warnings:
                st.write(f"• {warning}")

        else:

            st.success(
                "Skill classification consistency checks passed."
            )



    # TAB 2: EXPERIENCE AND EDUCATION
    with tab2:
        st.subheader("Relevant Experience")

        experiences = analysis.get("relevant_experience", [])

        if experiences:
            for experience in experiences:
                st.write(f"• {experience}")
        else:
            st.info("No relevant experience findings were returned.")

        st.subheader("Education and Qualifications")

        st.write(
            "Review the education-related findings in the "
            "score explanation and recommendations."
        )

        st.info(
            "Only qualifications documented in the resume "
            "are considered."
        )


    # TAB 3: RESUME FEEDBACK
    with tab3:
        st.subheader("Your Resume Strengths")

        strengths = analysis.get("strengths", [])

        if strengths:
            for strength in strengths:
                st.success(strength)
        else:
            st.info("No strengths were returned.")

        st.subheader("Areas for Improvement")

        improvements = analysis.get("areas_for_improvement", [])

        if improvements:
            for improvement in improvements:
                st.warning(improvement)
        else:
            st.info("No areas for improvement were returned.")

        with st.expander("View Detailed Score Explanation"):
            st.write(
                analysis.get(
                    "score_explanation",
                    "No score explanation was provided.",
                )
            )


    # TAB 4: RECOMMENDATIONS
    with tab4:
        st.subheader("Personalized Recommendations")

        recommendations = analysis.get("recommendations", [])

        if recommendations:
            for index, recommendation in enumerate(
                recommendations,
                start=1,
            ):
                st.markdown(f"**{index}. {recommendation}**")
        else:
            st.info("No recommendations were returned.")


    # --------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------

    st.divider()
    st.subheader("Download Your Analysis")

    json_report = json.dumps(analysis, indent=4)

    download_col1, download_col2 = st.columns(2)

    with download_col1:
        st.download_button(
            label="⬇ Download RoleLens JSON Report",
            data=json_report,
            file_name="rolelens_analysis.json",
            mime="application/json",
            use_container_width=True,
        )

    with download_col2:
        try:
            pdf_report = generate_pdf_report(
                analysis,
                st.session_state["resume_filename"],
            )

            st.download_button(
                label="⬇ Download RoleLens PDF Report",
                data=pdf_report,
                file_name="rolelens_career_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as error:
            st.error(
                "The PDF report could not be generated. "
                "The JSON report is still available."
            )
            st.caption(f"PDF error: {error}")


# ==========================================
# 8. FOOTER
# ==========================================

st.divider()

st.markdown(
    f"""
    <div style="text-align:center; padding:15px 0;">
        <div style="font-size:18px; font-weight:700; color:#F8FAFC;">
            {BRAND_NAME}
        </div>
        <div style="font-size:12px; color:#94A3B8; margin-top:5px;">
            {BRAND_DESCRIPTION}
        </div>
        <div style="font-size:11px; color:#64748B; margin-top:10px;">
            Built with Python, Streamlit, and Claude
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

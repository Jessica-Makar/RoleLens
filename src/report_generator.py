
from io import BytesIO
from xml.sax.saxutils import escape

from src.branding import BRAND_NAME, BRAND_TAGLINE, PDF_COLORS

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)


def generate_pdf_report(analysis, resume_filename):
    """Generate a PDF report from resume analysis results."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch
    )

    document.title = f"{BRAND_NAME} - Career Alignment Report"
    document.author = BRAND_NAME

    styles = getSampleStyleSheet()

    # ----------------------------------
    # CUSTOM STYLES
    # ----------------------------------

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=30,
        textColor=colors.HexColor(PDF_COLORS["heading"]),
        alignment=TA_CENTER,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=colors.HexColor(PDF_COLORS["primary"]),
        spaceBefore=16,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name="SkillTitle",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        spaceBefore=5,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        name="SkillDetail",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=12,
        leftIndent=10,
        spaceAfter=8,
        textColor=colors.HexColor(PDF_COLORS["secondary_text"])
    ))

    styles.add(ParagraphStyle(
        name="SmallText",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor(PDF_COLORS["secondary_text"])
    ))

    story = []

    # ----------------------------------
    # HEADER
    # ----------------------------------

    story.append(Paragraph(
        BRAND_NAME,
        styles["ReportTitle"]
    ))

    story.append(Paragraph(
        BRAND_TAGLINE,
        ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            textColor=colors.HexColor(PDF_COLORS["secondary_text"]),
            fontSize=10
        )
    ))

    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "CAREER ALIGNMENT REPORT",
        ParagraphStyle(
            "ReportLabel",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=9,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor(PDF_COLORS["primary"]),
            spaceAfter=8
        )
    ))

    story.append(Spacer(1, 15))

    story.append(HRFlowable(
        width="100%",
        color=colors.HexColor(PDF_COLORS["border"]),
        thickness=1.5
    ))

    story.append(Spacer(1, 12))

    # Resume filename
    story.append(Paragraph(
        f"<b>Resume analyzed:</b> {escape(str(resume_filename))}",
        styles["ReportBody"]
    ))

    # ----------------------------------
    # MATCH SCORE
    # ----------------------------------

    match_score = analysis["match_score"]

    story.append(Paragraph(
        "Overall Resume Match Score",
        styles["SectionHeading"]
    ))

    score_color = (
        "#16A34A" if match_score >= 75
        else "#D97706" if match_score >= 50
        else "#DC2626"
    )

    score_table = Table(
        [[f"{match_score}/100"]],
        colWidths=[2.5 * inch],
        rowHeights=[0.75 * inch]
    )

    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1),
         colors.HexColor("#EFF6FF")),

        ("BOX", (0, 0), (-1, -1), 1,
         colors.HexColor(PDF_COLORS["border"])),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 28),

        ("TEXTCOLOR", (0, 0), (-1, -1),
         colors.HexColor(score_color)),

        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    story.append(score_table)
    story.append(Spacer(1, 12))

    # ----------------------------------
    # SCORE BREAKDOWN
    # ----------------------------------

    story.append(Paragraph(
        "Score Breakdown",
        styles["SectionHeading"]
    ))

    score_limits = {
        "technical_skills": 40,
        "experience": 30,
        "education": 15,
        "other_requirements": 15
    }

    score_labels = {
        "technical_skills": "Technical Skills",
        "experience": "Relevant Experience",
        "education": "Education",
        "other_requirements": "Other Requirements"
    }

    breakdown_data = [
        ["Category", "Points Earned", "Maximum Points"]
    ]

    for category, score in analysis["score_breakdown"].items():

        breakdown_data.append([
            score_labels[category],
            str(score),
            str(score_limits[category])
        ])

    breakdown_table = Table(
        breakdown_data,
        colWidths=[3.2 * inch, 1.5 * inch, 1.5 * inch]
    )

    breakdown_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor(PDF_COLORS["heading"])),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("BACKGROUND", (0, 1), (-1, -1),
         colors.HexColor("#F8FAFC")),

        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#CBD5E1")),

        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(breakdown_table)

    # ----------------------------------
    # HELPER: GENERAL LIST SECTIONS
    # ----------------------------------

    def add_list_section(title, items):

        story.append(Paragraph(
            escape(title),
            styles["SectionHeading"]
        ))

        if not items:

            story.append(Paragraph(
                "No information available.",
                styles["ReportBody"]
            ))

            return

        for item in items:

            story.append(Paragraph(
                f"&bull; {escape(str(item))}",
                styles["ReportBody"]
            ))

    # ----------------------------------
    # HELPER: VERIFIED / UNVERIFIED SKILLS
    # ----------------------------------

    
    def add_skill_section(title, skills, detail_key, empty_message):

        is_verified = title == "Verified Skills"

        if is_verified:
            accent_color = colors.HexColor("#15803D")
            background_color = colors.HexColor("#F0FDF4")
            border_color = colors.HexColor("#BBF7D0")
        else:
            accent_color = colors.HexColor("#B45309")
            background_color = colors.HexColor("#FFFBEB")
            border_color = colors.HexColor("#FDE68A")

        story.append(Paragraph(
            escape(title),
            styles["SectionHeading"]
        ))

        if not skills:
            story.append(Paragraph(
                escape(empty_message),
                styles["ReportBody"]
            ))
            return

        for item in skills:

            if isinstance(item, dict):
                skill_name = item.get("skill", "Unnamed skill")
                detail = item.get(detail_key, "")
            else:
                skill_name = str(item)
                detail = ""

            # Create the skill name.
            skill_title = Paragraph(
                f'<font color="{accent_color.hexval()}">'
                f'<b>{escape(skill_name)}</b></font>',
                styles["SkillTitle"]
            )

            # Create the supporting evidence or explanation.
            if detail:
                skill_detail = Paragraph(
                    escape(str(detail)),
                    styles["SkillDetail"]
                )
            else:
                skill_detail = Paragraph(
                    "No additional explanation provided.",
                    styles["SkillDetail"]
                )

            # Place the skill title and explanation inside a card.
            skill_card = Table(
                [[skill_title], [skill_detail]],
                colWidths=[6.8 * inch]
            )

            skill_card.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), background_color),
                ("BOX", (0, 0), (-1, -1), 0.7, border_color),
                ("LINEBEFORE", (0, 0), (0, -1), 3, accent_color),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))

            # Keep the skill and its explanation together.
            story.append(
                KeepTogether([
                    skill_card,
                    Spacer(1, 7)
                ])
            )


    # ----------------------------------
    # SKILLS ANALYSIS
    # ----------------------------------

    add_list_section(
        "Matching Skills",
        analysis.get("matching_skills", [])
    )

    add_skill_section(
        "Verified Skills",
        analysis.get("verified_skills", []),
        "evidence",
        "No verified skills identified."
    )

    add_skill_section(
        "Unverified Skills",
        analysis.get("unverified_skills", []),
        "explanation",
        "No unverified skills identified."
    )

    add_list_section(
        "Missing Job Requirements",
        analysis.get("missing_skills", [])
    )

    # ----------------------------------
    # RELEVANT EXPERIENCE
    # ----------------------------------

    add_list_section(
        "Relevant Experience",
        analysis.get("relevant_experience", [])
    )

    # ----------------------------------
    # RESUME STRENGTHS
    # ----------------------------------

    add_list_section(
        "Resume Strengths",
        analysis.get("strengths", [])
    )

    # ----------------------------------
    # AREAS FOR IMPROVEMENT
    # ----------------------------------

    add_list_section(
        "Areas for Improvement",
        analysis.get("areas_for_improvement", [])
    )

    # ----------------------------------
    # RECOMMENDATIONS
    # ----------------------------------

    add_list_section(
        "Recommendations",
        analysis.get("recommendations", [])
    )

    # ----------------------------------
    # SCORE EXPLANATION
    # ----------------------------------

    story.append(Paragraph(
        "Score Explanation",
        styles["SectionHeading"]
    ))

    story.append(Paragraph(
        escape(str(analysis.get("score_explanation", ""))),
        styles["ReportBody"]
    ))

    # ----------------------------------
    # DISCLAIMER
    # ----------------------------------

    story.append(Spacer(1, 15))

    story.append(HRFlowable(
        width="100%",
        color=colors.HexColor("#CBD5E1")
    ))

    story.append(Spacer(1, 8))

    story.append(Paragraph(
        f"{escape(BRAND_NAME)} provides AI-generated estimates "
        "of resume alignment based on the information supplied. "
        "These insights are informational and do not guarantee "
        "an interview, employment, or hiring outcome.",
        styles["SmallText"]
    ))

    # ----------------------------------
    # GENERATE PDF
    # ----------------------------------

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()

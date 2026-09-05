import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# --- Color Palette ---
DARK_BG      = colors.HexColor("#0a0f1e")
CARD_BG      = colors.HexColor("#1e293b")
ACCENT_BLUE  = colors.HexColor("#6366f1")
GREEN        = colors.HexColor("#10b981")
RED          = colors.HexColor("#ef4444")
AMBER        = colors.HexColor("#f59e0b")
TEXT_LIGHT   = colors.HexColor("#f1f5f9")
TEXT_MUTED   = colors.HexColor("#94a3b8")
WHITE        = colors.white


def get_score_color(score: int):
    if score >= 75:
        return GREEN
    elif score >= 50:
        return AMBER
    return RED


def generate_report(score: int, feedback: str, matched_skills: list, missing_skills: list, filename: str = "Resume") -> bytes:
    """
    Generates a styled PDF analysis report and returns it as bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    score_color = get_score_color(score)

    # --- Custom Styles ---
    title_style = ParagraphStyle(
        "Title", parent=styles["Title"],
        fontSize=26, textColor=TEXT_LIGHT,
        spaceAfter=4, fontName="Helvetica-Bold", alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        fontSize=11, textColor=TEXT_MUTED, alignment=TA_CENTER, spaceAfter=2
    )
    section_heading = ParagraphStyle(
        "SectionHeading", parent=styles["Heading2"],
        fontSize=13, textColor=ACCENT_BLUE,
        fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=10, textColor=TEXT_LIGHT,
        leading=16, spaceAfter=6
    )
    muted_style = ParagraphStyle(
        "Muted", parent=styles["Normal"],
        fontSize=9, textColor=TEXT_MUTED, spaceAfter=4
    )
    score_style = ParagraphStyle(
        "Score", parent=styles["Normal"],
        fontSize=52, textColor=score_color,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4
    )

    story = []

    # ── Header ──────────────────────────────────────────────────────────────
    story.append(Paragraph("⚡ AI Resume Intelligence", title_style))
    story.append(Paragraph("ATS Optimization Analysis Report", subtitle_style))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}  •  File: {filename}",
        muted_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE, spaceAfter=16))

    # ── Score Block ──────────────────────────────────────────────────────────
    story.append(Paragraph("ATS Match Score", section_heading))
    story.append(Paragraph(f"{score}%", score_style))

    # Score interpretation
    if score >= 75:
        interpretation = "✅ Strong Match — Your resume is well-aligned with this job description."
    elif score >= 50:
        interpretation = "⚠️ Moderate Match — Some improvements recommended for better ATS performance."
    else:
        interpretation = "❌ Weak Match — Significant keyword gaps detected. Review missing skills."

    story.append(Paragraph(interpretation, body_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=CARD_BG, spaceAfter=8))

    # ── AI Feedback ──────────────────────────────────────────────────────────
    story.append(Paragraph("💡 AI Structural Strategy Roadmap", section_heading))
    story.append(Paragraph(feedback or "No feedback available.", body_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=CARD_BG, spaceAfter=8))

    # ── Skills Table ─────────────────────────────────────────────────────────
    story.append(Paragraph("🔍 Skills Analysis", section_heading))

    max_rows = max(len(matched_skills), len(missing_skills), 1)
    table_data = [
        [
            Paragraph("✅ Matched Capabilities", ParagraphStyle("th", fontSize=10, textColor=GREEN, fontName="Helvetica-Bold")),
            Paragraph("❌ Critical Skill Gaps", ParagraphStyle("th", fontSize=10, textColor=RED, fontName="Helvetica-Bold")),
        ]
    ]

    for i in range(max_rows):
        matched_cell = Paragraph(
            f"• {matched_skills[i]}" if i < len(matched_skills) else "",
            ParagraphStyle("td_green", fontSize=9, textColor=GREEN, leading=14)
        )
        missing_cell = Paragraph(
            f"• {missing_skills[i]}" if i < len(missing_skills) else "",
            ParagraphStyle("td_red", fontSize=9, textColor=RED, leading=14)
        )
        table_data.append([matched_cell, missing_cell])

    col_width = (A4[0] - 40 * mm) / 2
    skills_table = Table(table_data, colWidths=[col_width, col_width])
    skills_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#1e293b"), colors.HexColor("#162032")]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#334155")),
        ("TOPPADDING",  (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",(0, 0), (-1, -1), 10),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 16))

    # ── Footer ───────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE, spaceBefore=10, spaceAfter=8))
    story.append(Paragraph(
        "Generated by AI Resume Intelligence Dashboard — Powered by Groq LLaMA 3.3 70B",
        ParagraphStyle("footer", fontSize=8, textColor=TEXT_MUTED, alignment=TA_CENTER)
    ))

    # ── Build PDF ─────────────────────────────────────────────────────────────
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(DARK_BG)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    buffer.seek(0)
    return buffer.read()

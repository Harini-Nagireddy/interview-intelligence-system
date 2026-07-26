from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from modules.scoring import get_grade, get_performance_level


# Color palette
PRIMARY = colors.HexColor("#4F46E5")
SECONDARY = colors.HexColor("#7C3AED")
SUCCESS = colors.HexColor("#059669")
WARNING = colors.HexColor("#D97706")
DANGER = colors.HexColor("#DC2626")
LIGHT_BG = colors.HexColor("#F5F3FF")
DARK_TEXT = colors.HexColor("#1F2937")
GRAY = colors.HexColor("#6B7280")
LIGHT_GRAY = colors.HexColor("#E5E7EB")


def score_color(score):
    if score >= 8:
        return SUCCESS
    elif score >= 6:
        return WARNING
    else:
        return DANGER


def generate_pdf_report(output_path: str, candidate_name: str, role: str,
                         session_id: str, results: list, overall: dict):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle("Title", parent=styles["Normal"],
        fontSize=22, textColor=PRIMARY, alignment=TA_CENTER,
        spaceAfter=4, fontName="Helvetica-Bold")
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"],
        fontSize=11, textColor=GRAY, alignment=TA_CENTER, spaceAfter=2)
    section_header = ParagraphStyle("SectionHeader", parent=styles["Normal"],
        fontSize=13, textColor=PRIMARY, fontName="Helvetica-Bold",
        spaceBefore=12, spaceAfter=6, borderPadding=(0, 0, 4, 0))
    body_style = ParagraphStyle("Body", parent=styles["Normal"],
        fontSize=9.5, textColor=DARK_TEXT, spaceAfter=4, leading=14)
    small_style = ParagraphStyle("Small", parent=styles["Normal"],
        fontSize=8.5, textColor=GRAY, spaceAfter=2, leading=12)
    label_style = ParagraphStyle("Label", parent=styles["Normal"],
        fontSize=9, textColor=GRAY, fontName="Helvetica")
    value_style = ParagraphStyle("Value", parent=styles["Normal"],
        fontSize=10, textColor=DARK_TEXT, fontName="Helvetica-Bold")
    q_style = ParagraphStyle("Question", parent=styles["Normal"],
        fontSize=10, textColor=PRIMARY, fontName="Helvetica-Bold",
        spaceBefore=8, spaceAfter=3)

    story = []
    now = datetime.now()

    # ─── HEADER ───────────────────────────────────────────────────────────────
    header_data = [[
        Paragraph("🎤 Interview Intelligence System", title_style),
    ]]
    header_table = Table(header_data, colWidths=[17*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("ROUNDEDCORNERS", [8]),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Performance Evaluation Report", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=LIGHT_GRAY))
    story.append(Spacer(1, 8))

    # ─── CANDIDATE INFO ────────────────────────────────────────────────────────
    info_data = [
        [
            Paragraph("Candidate", label_style), Paragraph(candidate_name, value_style),
            Paragraph("Role Applied", label_style), Paragraph(role, value_style),
        ],
        [
            Paragraph("Date", label_style), Paragraph(now.strftime("%B %d, %Y"), value_style),
            Paragraph("Time", label_style), Paragraph(now.strftime("%I:%M %p"), value_style),
        ],
        [
            Paragraph("Session ID", label_style), Paragraph(session_id.upper(), value_style),
            Paragraph("Questions", label_style), Paragraph(str(len(results)), value_style),
        ],
    ]
    info_table = Table(info_data, colWidths=[3*cm, 5.5*cm, 3*cm, 5.5*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#FAFAFA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 14))

    # ─── OVERALL SCORES ────────────────────────────────────────────────────────
    story.append(Paragraph("📊 Overall Performance Summary", section_header))

    total = overall.get("total", 5)
    perf_level = get_performance_level(total)
    grade = get_grade(total)

    # Big score box
    score_data = [[
        Paragraph(f"{total}/10", ParagraphStyle("BigScore", parent=styles["Normal"],
            fontSize=32, textColor=PRIMARY, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(f"Grade: {grade}\n{perf_level}", ParagraphStyle("Grade", parent=styles["Normal"],
            fontSize=14, textColor=score_color(total), fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ]]
    score_box = Table(score_data, colWidths=[8*cm, 9*cm])
    score_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), LIGHT_BG),
        ("BACKGROUND", (1, 0), (1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 1, PRIMARY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(score_box)
    story.append(Spacer(1, 10))

    # Score breakdown table
    score_categories = [
        ("🎯 Confidence", overall.get("confidence", 0)),
        ("💬 Communication", overall.get("communication", 0)),
        ("👁 Engagement", overall.get("engagement", 0)),
        ("🗣 Fluency", overall.get("fluency", 0)),
        ("📝 Content Quality", overall.get("content", 0)),
    ]

    score_rows = [["Category", "Score", "Grade", "Status", "Progress"]]
    for cat, sc in score_categories:
        bar = "█" * int(sc) + "░" * (10 - int(sc))
        score_rows.append([
            Paragraph(cat, body_style),
            Paragraph(f"{sc}/10", ParagraphStyle("Sc", parent=styles["Normal"],
                fontSize=10, fontName="Helvetica-Bold", textColor=score_color(sc))),
            Paragraph(get_grade(sc), body_style),
            Paragraph(get_performance_level(sc), small_style),
            Paragraph(bar, ParagraphStyle("Bar", parent=styles["Normal"],
                fontSize=7, textColor=score_color(sc))),
        ])

    score_table = Table(score_rows, colWidths=[4.5*cm, 2*cm, 1.8*cm, 3.5*cm, 5.2*cm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9FF")]),
        ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHT_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 14))

    # ─── STRENGTHS & IMPROVEMENTS ─────────────────────────────────────────────
    story.append(Paragraph("💪 Strengths & Areas for Improvement", section_header))

    strengths = _get_strengths(overall, results)
    improvements = _get_improvements(overall, results)

    si_data = [
        [
            Paragraph("✅ Strengths", ParagraphStyle("SH", parent=styles["Normal"],
                fontSize=10, fontName="Helvetica-Bold", textColor=SUCCESS)),
            Paragraph("🔧 Areas to Improve", ParagraphStyle("IH", parent=styles["Normal"],
                fontSize=10, fontName="Helvetica-Bold", textColor=DANGER)),
        ],
        [
            Paragraph("\n".join(f"• {s}" for s in strengths), body_style),
            Paragraph("\n".join(f"• {i}" for i in improvements), body_style),
        ]
    ]
    si_table = Table(si_data, colWidths=[8.5*cm, 8.5*cm])
    si_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#ECFDF5")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FEF2F2")),
        ("BACKGROUND", (0, 1), (0, 1), colors.white),
        ("BACKGROUND", (1, 1), (1, 1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(si_table)
    story.append(Spacer(1, 14))

    # ─── PER-QUESTION BREAKDOWN ───────────────────────────────────────────────
    story.append(Paragraph("📋 Question-by-Question Analysis", section_header))

    for i, result in enumerate(results):
        q_num = i + 1
        scores = result.get("scores", {})
        sm = result.get("speech_metrics", {})
        am = result.get("audio_metrics", {})
        vm = result.get("video_metrics", {})
        answer = result.get("answer", "")
        q_total = round(sum(scores.values()) / max(len(scores), 1), 1)

        q_items = [
            Paragraph(f"Q{q_num}. {result.get('question', '')}", q_style),
        ]

        # Answer preview
        answer_preview = answer[:200] + "..." if len(answer) > 200 else answer
        if answer_preview:
            q_items.append(Paragraph(f'<i>"{answer_preview}"</i>', small_style))

        # Metrics row
        metrics_data = [[
            _metric_cell("Words", sm.get("word_count", 0), ""),
            _metric_cell("Fillers", sm.get("filler_count", 0), ""),
            _metric_cell("Silence", f"{int(am.get('silence_ratio', 0)*100)}%", ""),
            _metric_cell("Eye Contact", f"{vm.get('eye_contact_score', 0)}/10", ""),
            _metric_cell("Score", f"{q_total}/10", ""),
        ]]
        metrics_table = Table(metrics_data, colWidths=[3.4*cm]*5)
        metrics_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#C4B5FD")),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#DDD6FE")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        q_items.append(metrics_table)

        # Assessment
        assessment = sm.get("assessment", "")
        if assessment:
            q_items.append(Paragraph(f"💡 {assessment}", small_style))

        story.append(KeepTogether(q_items))
        story.append(Spacer(1, 4))
        if i < len(results) - 1:
            story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY))

    story.append(Spacer(1, 14))

    # ─── RECOMMENDATIONS ──────────────────────────────────────────────────────
    story.append(Paragraph("🚀 Personalized Recommendations", section_header))
    recs = _get_recommendations(overall, results)
    for rec in recs:
        story.append(Paragraph(f"➤ {rec}", body_style))

    story.append(Spacer(1, 14))

    # ─── FOOTER ───────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=LIGHT_GRAY))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"Generated by Interview Intelligence System • {now.strftime('%B %d, %Y at %I:%M %p')}",
        ParagraphStyle("Footer", parent=styles["Normal"],
            fontSize=8, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)


def _metric_cell(label, value, unit):
    from reportlab.lib.styles import getSampleStyleSheet
    styles = getSampleStyleSheet()
    label_s = ParagraphStyle("ML", parent=styles["Normal"],
        fontSize=7.5, textColor=GRAY, alignment=TA_CENTER)
    value_s = ParagraphStyle("MV", parent=styles["Normal"],
        fontSize=11, fontName="Helvetica-Bold", textColor=PRIMARY, alignment=TA_CENTER)
    return [Paragraph(str(value) + str(unit), value_s), Paragraph(label, label_s)]


def _get_strengths(overall, results):
    strengths = []
    if overall.get("confidence", 0) >= 7:
        strengths.append("Strong confidence and camera presence throughout the interview")
    if overall.get("communication", 0) >= 7:
        strengths.append("Clear and articulate communication style")
    if overall.get("fluency", 0) >= 7:
        strengths.append("Good speech fluency with minimal pauses")
    if overall.get("content", 0) >= 7:
        strengths.append("Detailed and well-structured answers with relevant content")
    if overall.get("engagement", 0) >= 7:
        strengths.append("Strong engagement and eye contact with the camera")

    total_words = sum(r.get("speech_metrics", {}).get("word_count", 0) for r in results)
    if total_words >= 300:
        strengths.append("Comprehensive answers demonstrating depth of knowledge")

    avg_fillers = sum(r.get("speech_metrics", {}).get("filler_count", 0) for r in results) / max(len(results), 1)
    if avg_fillers < 3:
        strengths.append("Minimal use of filler words — very clean speech pattern")

    if not strengths:
        strengths.append("Participated in the full mock interview — great practice!")

    return strengths[:5]


def _get_improvements(overall, results):
    improvements = []
    if overall.get("confidence", 0) < 6:
        improvements.append("Work on maintaining consistent eye contact with the camera")
    if overall.get("communication", 0) < 6:
        improvements.append("Practice structuring answers using the STAR method")
    if overall.get("fluency", 0) < 6:
        improvements.append("Reduce long pauses — try thinking before speaking rather than mid-sentence")
    if overall.get("content", 0) < 6:
        improvements.append("Add specific examples and metrics to support your answers")
    if overall.get("engagement", 0) < 6:
        improvements.append("Improve posture and camera alignment for better presence")

    avg_fillers = sum(r.get("speech_metrics", {}).get("filler_count", 0) for r in results) / max(len(results), 1)
    if avg_fillers >= 5:
        improvements.append("Significantly reduce filler words (um, uh, like) — practice pausing instead")

    avg_words = sum(r.get("speech_metrics", {}).get("word_count", 0) for r in results) / max(len(results), 1)
    if avg_words < 50:
        improvements.append("Give more detailed answers — aim for 2-3 minute responses per question")

    if not improvements:
        improvements.append("Continue practicing regularly to maintain and improve your performance")

    return improvements[:5]


def _get_recommendations(overall, results):
    recs = []
    total = overall.get("total", 5)

    if total >= 8:
        recs.append("You are interview-ready! Focus on practicing for company-specific technical rounds.")
        recs.append("Consider mock interviews for FAANG/top-tier companies to further sharpen your skills.")
    elif total >= 6:
        recs.append("You have a solid foundation. Practice 2-3 mock interviews per week for the next month.")
        recs.append("Record yourself answering questions and watch the recordings critically.")
    else:
        recs.append("Start with daily 15-minute practice sessions — focus on one skill at a time.")
        recs.append("Join a peer interview practice group or find a mentor for guided feedback.")

    if overall.get("fluency", 0) < 7:
        recs.append("Practice the 'pause instead of filler' technique: when you feel an 'um' coming, just pause silently.")

    if overall.get("content", 0) < 7:
        recs.append("Prepare 5-10 strong STAR stories from your experience covering leadership, problem-solving, and teamwork.")

    if overall.get("confidence", 0) < 7:
        recs.append("Practice power posing before interviews and maintain an upright posture throughout.")

    recs.append("Review common interview questions for your target role and practice them out loud daily.")
    recs.append("Use resources like Pramp, Interviewing.io, or LeetCode for technical practice.")

    return recs[:6]

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_report(candidate_name, topic, results):
    os.makedirs("reports", exist_ok=True)

    filename = f"reports/Interview_Report_{candidate_name}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Interview Intelligence System Report")

    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Candidate Name: {candidate_name}")
    y -= 20
    c.drawString(50, y, f"Interview Topic: {topic}")
    y -= 20
    c.drawString(50, y, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

    y -= 40
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Evaluation Summary")

    y -= 25
    c.setFont("Helvetica", 11)
    for key, value in results.items():
        score, label = value
        c.drawString(60, y, f"{key}: {score} ({label})")
        y -= 20

    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Improvement Tips")

    y -= 25
    c.setFont("Helvetica", 11)

    if results["Voice & Pace"][1] == "Weak":
        c.drawString(60, y, "- Reduce long pauses and speak more continuously.")
        y -= 15

    if results["Communication"][1] != "Strong":
        c.drawString(60, y, "- Structure answers as Problem → Solution → Impact.")
        y -= 15

    if results["Camera Presence"][1] != "Strong":
        c.drawString(60, y, "- Maintain eye contact and proper camera alignment.")

    c.showPage()
    c.save()

    return filename

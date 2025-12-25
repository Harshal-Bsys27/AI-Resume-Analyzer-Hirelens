from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_report_pdf(analysis_result, output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, filename)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # HireLens Logo/Heading
    y = height - 40
    c.setFont("Helvetica-Bold", 28)
    c.setFillColorRGB(1, 0.7, 0.2)
    c.drawCentredString(width / 2, y, "HireLens")
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    y -= 30
    c.drawCentredString(width / 2, y, "AI Resume Analyzer Report")
    c.setFillColorRGB(0, 0, 0)
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Role Selected: {analysis_result.get('selected_role', 'N/A')}")
    y -= 20
    c.drawString(40, y, f"Role Detected: {analysis_result.get('role_detected', 'N/A')}")
    y -= 20
    c.drawString(40, y, f"Profile Type: {analysis_result.get('profile_type', 'N/A')}")
    y -= 20
    c.drawString(40, y, f"Overall ATS Score: {analysis_result.get('overall_score', 0)}%")
    y -= 20
    c.drawString(40, y, f"Tech Stack Coverage: {analysis_result.get('techstack_coverage', 0)}%")
    y -= 20
    breakdown = analysis_result.get("score_breakdown", {})
    c.drawString(40, y, f"Skills Match: {breakdown.get('skills_match', 0)}%")
    y -= 15
    c.drawString(40, y, f"Experience Match: {breakdown.get('experience_match', 0)}%")
    y -= 15
    c.drawString(40, y, f"Education Match: {breakdown.get('education_match', 0)}%")
    y -= 25

    def draw_section(title, items):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(1, 0.7, 0.2)
        c.drawString(40, y, f"{title}:")
        c.setFillColorRGB(0, 0, 0)
        y -= 18
        c.setFont("Helvetica", 12)
        if items:
            for item in items:
                if y < 60:
                    c.showPage()
                    y = height - 40
                c.drawString(60, y, f"- {item}")
                y -= 15
        else:
            c.drawString(60, y, "None")
            y -= 15
        y -= 5

    skills = analysis_result.get("skills", {})
    draw_section("Matched Technical Skills", skills.get("matched_skills", []))
    draw_section("Missing Technical Skills", skills.get("missing_skills", []))
    draw_section("Matched Soft Skills", skills.get("matched_soft_skills", []))
    draw_section("Missing Soft Skills", skills.get("missing_soft_skills", []))
    draw_section("Matched Certifications", skills.get("matched_certifications", []))
    draw_section("Missing Certifications", skills.get("missing_certifications", []))
    draw_section("Matched Role Tech Stack", skills.get("matched_role_skills", []))
    draw_section("Missing Role Tech Stack", skills.get("missing_role_skills", []))
    draw_section("Strengths", analysis_result.get("strengths", []))
    draw_section("Weaknesses", analysis_result.get("weaknesses", []))
    draw_section("Suggestions", analysis_result.get("suggestions", []))
    draw_section("Feedback", analysis_result.get("feedback", []))
    draw_section("Detected Flaws", analysis_result.get("flaws", []))
    draw_section("Key Responsibilities for this Role", analysis_result.get("key_responsibilities", []))
    draw_section("Recommended Keywords for this Role", analysis_result.get("recommended_keywords", []))

    # Chart Data
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(1, 0.7, 0.2)
    c.drawString(40, y, "Chart Data (for frontend visualization):")
    c.setFillColorRGB(0, 0, 0)
    y -= 18
    c.setFont("Helvetica", 12)
    chart_data = analysis_result.get("chart_data", {})
    for k, v in chart_data.items():
        c.drawString(60, y, f"{k}: {v}%")
        y -= 15

    c.save()
    return pdf_path

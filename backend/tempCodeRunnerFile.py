from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid

from services.pdf_extractor import extract_text_from_pdf
from services.nlp_analyzer import analyze_resume
from services.report_generator import generate_report_pdf

# ---------------- App Config ----------------
app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------- Health Check ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "AI Resume Analyzer Backend Running"
    })

# ---------------- Analyze Resume ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        resume = request.files.get("resume")
        job_description = request.form.get("job_description")

        if not resume or not job_description:
            print("❌ Missing resume or job description in request")
            return jsonify({
                "error": "Resume file or Job Description missing"
            }), 400

        # Only allow PDF files
        if not resume.filename.lower().endswith('.pdf'):
            print("❌ Uploaded file is not a PDF")
            return jsonify({
                "error": "Only PDF files are supported"
            }), 400

        # Extract resume text
        resume_text = extract_text_from_pdf(resume)
        print("Extracted resume text:", resume_text[:500])  # Log first 500 chars

        if not resume_text or not resume_text.strip():
            print("❌ No text extracted from PDF")
            return jsonify({
                "error": "Unable to extract text from resume PDF"
            }), 400

        # NLP Analysis
        analysis_result = analyze_resume(resume_text, job_description)
        print("Analysis result:", analysis_result)  # Log analysis result

        if not analysis_result or not isinstance(analysis_result, dict):
            print("❌ Analysis result is invalid")
            return jsonify({
                "error": "Resume analysis failed. Try again."
            }), 500

        # Generate unique report
        report_id = str(uuid.uuid4())
        pdf_path = generate_report_pdf(
            analysis_result=analysis_result,
            output_dir=OUTPUT_FOLDER,
            filename=f"{report_id}.pdf"
        )

        download_url = f"{request.url_root.rstrip('/')}/download-report/{report_id}"

        return jsonify({
            "status": "success",
            "analysis": analysis_result,
            "report_id": report_id,
            "download_url": download_url
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500


# ---------------- Download Report ----------------
@app.route("/download-report/<report_id>", methods=["GET"])
def download_report(report_id):
    file_path = os.path.join(OUTPUT_FOLDER, f"{report_id}.pdf")

    if not os.path.exists(file_path):
        return jsonify({
            "error": "Report not found"
        }), 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name="resume_analysis_report.pdf"
    )


# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(debug=True)

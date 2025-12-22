from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)
CORS(app)

# ---------------- Load Models ----------------
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- Skill Database ----------------
SKILLS_DB = [
    "python", "java", "c++", "flask", "django", "react", "node",
    "sql", "mongodb", "machine learning", "deep learning",
    "nlp", "opencv", "data analysis", "tensorflow", "pytorch",
    "aws", "docker", "git", "linux"
]

# ---------------- Helper Functions ----------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text.lower()

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills(text):
    extracted_skills = set()
    for skill in SKILLS_DB:
        if skill in text:
            extracted_skills.add(skill)
    return list(extracted_skills)

def semantic_similarity(text1, text2):
    embeddings = model.encode([text1, text2])
    score = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]
    return round(score * 100, 2)

# ---------------- Analysis Logic ----------------
def analyze_resume(resume_text, jd_text):
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    overall_score = semantic_similarity(resume_text, jd_text)

    # Section-wise scoring (simple but explainable)
    skills_score = (
        (len(matched_skills) / max(len(jd_skills), 1)) * 100
    )

    experience_score = semantic_similarity(
        resume_text[:1500], jd_text[:1500]
    )

    education_score = 70  # baseline (can improve later)

    # Strengths & Weaknesses
    strengths = []
    weaknesses = []

    if skills_score >= 70:
        strengths.append("Strong technical skill match with job requirements")
    else:
        weaknesses.append("Skills mismatch with job requirements")

    if experience_score >= 65:
        strengths.append("Relevant experience aligned with job description")
    else:
        weaknesses.append("Experience section needs improvement")

    if missing_skills:
        weaknesses.append(
            f"Missing important skills: {', '.join(missing_skills)}"
        )

    suggestions = [
        "Add quantified achievements in experience section",
        "Include missing skills relevant to the job role",
        "Optimize resume keywords for ATS systems"
    ]

    return {
        "overall_score": overall_score,
        "score_breakdown": {
            "skills_match": round(skills_score, 2),
            "experience_match": round(experience_score, 2),
            "education_match": education_score
        },
        "skills": {
            "resume_skills": resume_skills,
            "job_skills": jd_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }

# ---------------- API Route ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files.get("resume")
    jd = request.form.get("job_description")

    if not resume or not jd:
        return jsonify({"error": "Resume or Job Description missing"}), 400

    resume_text = extract_text_from_pdf(resume)
    analysis_result = analyze_resume(resume_text, jd)

    return jsonify({
        "status": "success",
        "analysis": analysis_result
    })

# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_similarity_score(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(score * 100, 2)

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    resume = request.files.get("resume")
    jd = request.form.get("job_description")

    if not resume or not jd:
        return jsonify({"error": "Resume or Job Description missing"}), 400

    resume_text = extract_text_from_pdf(resume)
    score = get_similarity_score(resume_text, jd)

    return jsonify({
        "match_score": score,
        "message": "Resume analyzed successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)

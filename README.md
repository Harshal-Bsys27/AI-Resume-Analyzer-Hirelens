
# HireLens: AI Resume Analyzer

**AI-powered ATS Resume Analyzer**

Simulate how real Applicant Tracking Systems (ATS) scan, filter, and score your resume. Get actionable feedback, keyword gaps, and role-based insights to improve your chances before you apply.

---

## 🚀 Features
- **PDF Resume Upload**: Upload your resume in PDF format.
- **Role & JD Matching**: Select a target role or paste a job description for best accuracy.
- **AI Analysis**: Extracts skills, soft skills, certifications, and matches them to the role/JD using advanced NLP.
- **ATS Score**: See your overall ATS score and detailed breakdown (skills, experience, education).
- **Skill Tags**: Instantly see matched, missing, and extra skills.
- **Strengths & Weaknesses**: Get personalized strengths, weaknesses, and improvement suggestions.
- **Role-Specific Insights**: View key responsibilities and keywords for your target role.
- **Downloadable PDF Report**: Download a detailed, human-readable report.
- **Modern UI**: Built with React, Tailwind CSS, and Recharts for a clean, interactive experience.
- **No Login Required**: Open to use, no authentication needed.

---

## 📸 Screenshots

| Screen                | Example Image                          |
|-----------------------|----------------------------------------|
| Home/Landing Page     | ![Home](screenshots/home.png)          |
| Resume Upload         | ![Upload](screenshots/upload.png)      |
| JD/Role Selection     | ![Role](screenshots/role.png)          |
| Analysis Result       | ![Result](screenshots/result.png)      |
| Scorecard/Chart       | ![Chart](screenshots/chart.png)        |
| Download Report       | ![Download](screenshots/download.png)  |

> Place your screenshots in the `screenshots/` folder and update the file names above as needed.

---

## 🛠️ How It Works
1. **Upload Resume**: Click the upload area and select your PDF resume.
2. **Enter Job Description or Select Role**: Paste a job description or pick a role from the dropdown.
3. **Analyze**: Click the analyze button. The app extracts text, analyzes skills, and matches them to the JD/role using AI.
4. **View Results**: See your ATS score, matched/missing skills, strengths, weaknesses, and suggestions.
5. **Download Report**: Download a detailed PDF report for your records.

---

## 🏗️ Tech Stack
- **Frontend**: React, Tailwind CSS, Recharts, Vite
- **Backend**: Flask, Python, PyPDF2, Sentence Transformers, ReportLab
- **AI/NLP**: Sentence Transformers for semantic similarity, custom skill extraction
- **PDF Parsing**: PyPDF2
- **PDF Report Generation**: ReportLab

---

## ⚡ Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Harshal-Bsys27/AI-Resume-Analyzer-Hirelens.git
   cd AI-Resume-Analyzer-Hirelens
   ```
2. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. **Install Backend Dependencies**
   ```bash
   cd ../backend
   pip install -r requirements.txt
   python app.py
   ```
4. **Open in Browser**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

---

## ⚠️ Limitations & Notes
- This project requires more than 512MB RAM to run online due to AI/NLP dependencies (torch, spacy, etc.).
- Free hosting platforms may not support the full-featured app. For a live demo, use a paid plan or run locally.
- All processing is done locally; no data is sent to third parties.

---

## 🙏 Credits
- Built by Harshal-Bsys27
- Inspired by real-world ATS and resume optimization tools

---

## 📬 Contact
For questions or feedback, open an issue or contact via GitHub.

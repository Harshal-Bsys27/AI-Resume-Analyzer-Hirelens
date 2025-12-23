import re
from utils.scoring import semantic_similarity, calculate_skills_score

SKILLS_DB = [
    "python", "java", "c++", "flask", "django", "react", "node",
    "sql", "mongodb", "machine learning", "deep learning",
    "nlp", "opencv", "data analysis", "tensorflow", "pytorch",
    "aws", "docker", "git", "linux"
]

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills(text):
    found = set()
    for skill in SKILLS_DB:
        if skill in text:
            found.add(skill)
    return list(found)

def analyze_resume(resume_text, jd_text):
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    overall_score = semantic_similarity(resume_text, jd_text)
    skills_score = calculate_skills_score(matched_skills, len(jd_skills))
    experience_score = semantic_similarity(
        resume_text[:1500], jd_text[:1500]
    )
    education_score = 70  # baseline

    strengths = []
    weaknesses = []

    if skills_score >= 70:
        strengths.append("Strong technical skill alignment")
    else:
        weaknesses.append("Skill match is below expected level")

    if experience_score >= 65:
        strengths.append("Relevant experience matches job needs")
    else:
        weaknesses.append("Experience needs improvement")

    if missing_skills:
        weaknesses.append(
            f"Missing important skills: {', '.join(missing_skills)}"
        )

    suggestions = [
        "Add quantified achievements in experience",
        "Include missing job-specific skills",
        "Optimize keywords for ATS systems"
    ]

    return {
        "overall_score": overall_score,
        "score_breakdown": {
            "skills_match": skills_score,
            "experience_match": experience_score,
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

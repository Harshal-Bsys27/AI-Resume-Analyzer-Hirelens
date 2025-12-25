import re
from utils.skills import (
    extract_skills, infer_role, extract_soft_skills, extract_certifications, get_role_responsibilities, ROLE_SKILLS
)

# ---------------- Helpers ----------------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def detect_fresher(resume_text):
    fresher_keywords = [
        "fresher", "student", "intern", "internship",
        "final year", "undergraduate", "graduate"
    ]
    return any(word in resume_text for word in fresher_keywords)


def has_degree(resume_text):
    degree_keywords = [
        "bachelor", "b.tech", "b.e", "bsc",
        "master", "m.tech", "msc", "mba", "phd"
    ]
    return any(word in resume_text for word in degree_keywords)


# ---------------- Main Analyzer ----------------
def analyze_resume(resume_text, jd_text, selected_role=None):
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)
    role_detected = selected_role if selected_role else infer_role(jd_text)
    role_keywords = set(ROLE_SKILLS.get(role_detected, []))

    resume_skills = extract_skills(resume_text)
    # If job description is empty, use role keywords as job_skills
    if jd_text.strip():
        jd_skills = extract_skills(jd_text)
    else:
        jd_skills = list(role_keywords)

    resume_soft_skills = extract_soft_skills(resume_text)
    resume_certs = extract_certifications(resume_text)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))
    extra_skills = list(set(resume_skills) - set(jd_skills))

    matched_role_skills = list(set(resume_skills) & role_keywords)
    missing_role_skills = list(role_keywords - set(resume_skills))
    techstack_coverage = round((len(matched_role_skills) / len(role_keywords)) * 100, 2) if role_keywords else 0.0

    soft_skills_needed = extract_soft_skills(jd_text)
    matched_soft_skills = list(set(resume_soft_skills) & set(soft_skills_needed))
    missing_soft_skills = list(set(soft_skills_needed) - set(resume_soft_skills))

    certs_needed = extract_certifications(jd_text)
    matched_certs = list(set(resume_certs) & set(certs_needed))
    missing_certs = list(set(certs_needed) - set(resume_certs))

    skills_score = (len(matched_skills) / len(jd_skills)) * 100 if jd_skills else 50.0
    is_fresher = detect_fresher(resume_text)
    experience_score = 65.0 if is_fresher else min(90.0, skills_score + 10)
    education_score = 85.0 if has_degree(resume_text) else 55.0
    overall_score = (
        (skills_score * 0.5) +
        (experience_score * 0.3) +
        (education_score * 0.2)
    )

    strengths, weaknesses, suggestions = [], [], []

    # Skills section
    if matched_skills:
        strengths.append(f"Matched technical skills: {', '.join(matched_skills)}.")
    else:
        weaknesses.append("No matched technical skills found.")
        suggestions.append(f"Add more technical skills relevant for {role_detected}.")

    if missing_skills:
        weaknesses.append(f"Missing key technical skills: {', '.join(missing_skills)}.")
        suggestions.append("Include missing skills from the job description or role requirements.")

    # Role tech stack section
    if matched_role_skills:
        strengths.append(f"Matched {role_detected} tech stack: {', '.join(matched_role_skills)}.")
    else:
        weaknesses.append(f"No matched tech stack keywords for {role_detected}.")
        suggestions.append(f"Add more {role_detected} tech stack keywords.")

    if missing_role_skills:
        weaknesses.append(f"Missing important tech stack keywords for {role_detected}: {', '.join(missing_role_skills)}.")
        suggestions.append(f"Include missing tech stack keywords for {role_detected}.")

    # Soft skills section
    if matched_soft_skills:
        strengths.append(f"Demonstrated soft skills: {', '.join(matched_soft_skills)}.")
    else:
        weaknesses.append("No matched soft skills found.")
        suggestions.append("Highlight soft skills such as teamwork, communication, and adaptability.")

    if missing_soft_skills:
        weaknesses.append(f"Missing soft skills: {', '.join(missing_soft_skills)}.")

    # Certifications section
    if matched_certs:
        strengths.append(f"Relevant certifications: {', '.join(matched_certs)}.")
    else:
        weaknesses.append("No matched certifications found.")
        suggestions.append("List certifications relevant to the job description.")

    if missing_certs:
        weaknesses.append(f"Missing certifications: {', '.join(missing_certs)}.")

    # Experience/Education
    if is_fresher:
        strengths.append("Fresher profile evaluated without experience penalty.")
    elif experience_score < 60:
        weaknesses.append("Experience section lacks role-specific keywords or quantifiable achievements.")
        suggestions.append("Add quantifiable achievements and role-specific keywords in experience section.")

    # General suggestions
    suggestions += [
        "Use job description keywords naturally in your resume.",
        "Add measurable achievements and project outcomes.",
        "Explicitly list tools, technologies, and frameworks.",
        "Tailor your summary and experience to the target role."
    ]

    feedback = []
    feedback.append(strengths[-1] if strengths else "No strengths found.")
    feedback.append(weaknesses[-1] if weaknesses else "No weaknesses found.")

    flaws = []
    if len(resume_text.split()) < 200:
        flaws.append("Resume is too short; consider adding more details about your experience, projects, and achievements.")
    if not matched_skills:
        flaws.append("No required technical skills from the job description found in the resume.")
    if not matched_soft_skills and soft_skills_needed:
        flaws.append("No required soft skills from the job description found in the resume.")

    chart_data = {
        "Tech Stack Coverage": techstack_coverage,
        "Skills Match": round(float(skills_score), 2),
        "Experience Match": round(float(experience_score), 2),
        "Education Match": round(float(education_score), 2),
        "Overall ATS Score": round(float(overall_score), 2)
    }

    # Detailed analysis report
    analysis = {
        "overall_score": round(float(overall_score), 2),
        "score_breakdown": {
            "skills_match": round(float(skills_score), 2),
            "experience_match": round(float(experience_score), 2),
            "education_match": round(float(education_score), 2)
        },
        "techstack_coverage": techstack_coverage,
        "skills": {
            "matched_skills": matched_skills if matched_skills else [],
            "missing_skills": missing_skills if missing_skills else ["All required skills present"],
            "soft_skills": resume_soft_skills,
            "matched_soft_skills": matched_soft_skills if matched_soft_skills else [],
            "missing_soft_skills": missing_soft_skills if missing_soft_skills else ["All required soft skills present"],
            "certifications": resume_certs,
            "matched_certifications": matched_certs if matched_certs else [],
            "missing_certifications": missing_certs if missing_certs else ["All required certifications present"],
            "matched_role_skills": matched_role_skills if matched_role_skills else [],
            "missing_role_skills": missing_role_skills if missing_role_skills else ["All important tech stack keywords present"]
        },
        "strengths": strengths if strengths else ["No strengths found."],
        "weaknesses": weaknesses if weaknesses else ["No weaknesses found."],
        "suggestions": suggestions if suggestions else ["No suggestions found."],
        "feedback": feedback,
        "flaws": flaws if flaws else ["No major flaws detected."],
        "chart_data": chart_data,
        "summary": f"Resume matches {round(float(skills_score), 2)}% of the required technical skills for the {role_detected} role. Tech stack coverage: {techstack_coverage}%."
    }

    return analysis

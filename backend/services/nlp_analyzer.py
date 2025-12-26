import re
from utils.skills import (
    extract_skills, infer_role, extract_soft_skills, extract_certifications,
    get_role_responsibilities, ROLE_SKILLS, get_role_keywords
)
from utils.scoring import semantic_similarity, calculate_skills_score

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
    key_responsibilities = get_role_responsibilities(role_detected)
    recommended_keywords = get_role_keywords(role_detected)

    resume_skills = extract_skills(resume_text)
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

    # Use semantic similarity for overall match if job description is provided
    if jd_text.strip():
        semantic_score = semantic_similarity(resume_text, jd_text)
    else:
        semantic_score = None

    # Improved scoring logic
    # Give extra credit for presence of projects, education, experience
    has_projects = "project" in resume_text or "projects" in resume_text
    has_experience = "experience" in resume_text or "work" in resume_text or "internship" in resume_text
    has_education = "education" in resume_text or "degree" in resume_text or has_degree(resume_text)

    skills_score = calculate_skills_score(matched_skills, len(jd_skills))
    # Experience score: more dynamic and higher if experience/projects found
    experience_score = 65.0
    if has_experience:
        experience_score += 15
    if has_projects:
        experience_score += 10
    experience_score = min(100.0, experience_score)

    # Education score: higher if education/degree found
    education_score = 55.0
    if has_education:
        education_score = 85.0

    # Overall score: weighted, includes semantic similarity if available
    overall_score = (
        (skills_score * 0.4) +
        (experience_score * 0.3) +
        (education_score * 0.2) +
        ((semantic_score or 0) * 0.1)
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

    # Soft skills section (improved)
    if matched_soft_skills:
        strengths.append(f"Demonstrated soft skills: {', '.join(matched_soft_skills)}.")
    else:
        weaknesses.append("No matched soft skills found.")
        suggestions.append("Highlight soft skills such as teamwork, communication, adaptability, and leadership in your resume.")

    if missing_soft_skills:
        weaknesses.append(f"Missing soft skills: {', '.join(missing_soft_skills)}.")
        suggestions.append("Add examples or achievements that demonstrate these soft skills.")

    # Certifications section
    if matched_certs:
        strengths.append(f"Relevant certifications: {', '.join(matched_certs)}.")
    else:
        weaknesses.append("No matched certifications found.")
        suggestions.append("List certifications relevant to the job description.")

    if missing_certs:
        weaknesses.append(f"Missing certifications: {', '.join(missing_certs)}.")
        suggestions.append("Consider pursuing certifications that match the job requirements.")

    # Experience/Education
    if has_experience:
        strengths.append("Experience section found and evaluated.")
    else:
        weaknesses.append("Experience section is missing or lacks detail.")
        suggestions.append("Add a dedicated experience section with quantifiable achievements.")

    if has_projects:
        strengths.append("Projects section found and evaluated.")
    else:
        weaknesses.append("Projects section is missing or lacks detail.")
        suggestions.append("Add a projects section to showcase relevant work.")

    if has_education:
        strengths.append("Education section found and evaluated.")
    else:
        weaknesses.append("Education section is missing or lacks detail.")
        suggestions.append("Add an education section with your degrees and relevant coursework.")

    # General suggestions
    suggestions += [
        "Use job description keywords naturally in your resume.",
        "Add measurable achievements and project outcomes.",
        "Explicitly list tools, technologies, and frameworks.",
        "Tailor your summary and experience to the target role.",
        "Highlight leadership, teamwork, and communication in your experience.",
        "Include certifications and training relevant to the job.",
        "Make sure your resume is easy to read and well-formatted.",
        "Add links to your portfolio, GitHub, or LinkedIn if relevant.",
        "Quantify your impact (e.g., 'Improved efficiency by 30%').",
        "Keep your resume concise but detailed (1-2 pages recommended).",
        "Check for spelling and grammar errors before submitting.",
        "Use bullet points for clarity and readability.",
        "Customize your resume for each application.",
        "Show results and outcomes for your projects and roles.",
        "Include relevant extracurriculars, volunteering, or leadership."
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
        "Semantic Similarity": round(float(semantic_score or 0), 2),
        "Overall ATS Score": round(float(overall_score), 2)
    }

    # Fallbacks for empty sections
    def fallback_matched(section_name):
        return [f"No {section_name} detected in your resume. Consider adding relevant {section_name.lower()} to improve your ATS score."]

    def fallback_missing(section_name):
        return [f"Review the job description and add missing {section_name.lower()} for better matching."]

    # Prepare skills sections with fallbacks
    matched_skills = matched_skills if matched_skills else fallback_matched("Technical Skills")
    missing_skills = missing_skills if missing_skills else fallback_missing("Technical Skills")
    matched_role_skills = matched_role_skills if matched_role_skills else fallback_matched("Role Tech Stack")
    missing_role_skills = missing_role_skills if missing_role_skills else fallback_missing("Role Tech Stack")
    matched_soft_skills = matched_soft_skills if matched_soft_skills else fallback_matched("Soft Skills")
    missing_soft_skills = missing_soft_skills if missing_soft_skills else fallback_missing("Soft Skills")
    matched_certs = matched_certs if matched_certs else fallback_matched("Certifications")
    missing_certs = missing_certs if missing_certs else fallback_missing("Certifications")

    # If scores are 0.0%, add explanation to weaknesses
    if skills_score == 0.0:
        weaknesses.append("No technical skills matched. Your resume may lack keywords from the job description or role requirements.")
    if techstack_coverage == 0.0:
        weaknesses.append("No tech stack keywords detected. Add relevant technologies and tools for your target role.")
    if semantic_score is not None and semantic_score < 20.0:
        weaknesses.append("Low semantic similarity to job description. Tailor your resume content to better match the job requirements.")

    # Section-by-section analysis
    detailed_sections = [
        {
            "section": "Technical Skills",
            "matched": matched_skills,
            "missing": missing_skills,
            "feedback": f"Matched {len([s for s in matched_skills if 'No technical skills' not in s])} out of {len(role_keywords)} required technical skills for {role_detected}.",
            "suggestions": [
                "Add missing technical skills from the job description.",
                "Use exact keywords from the role requirements."
            ]
        },
        {
            "section": "Role Tech Stack",
            "matched": matched_role_skills,
            "missing": missing_role_skills,
            "feedback": f"Tech stack coverage: {techstack_coverage}%.",
            "suggestions": [
                "Highlight your experience with the missing tech stack keywords.",
                "Mention tools and frameworks relevant to the role."
            ]
        },
        {
            "section": "Soft Skills",
            "matched": matched_soft_skills,
            "missing": missing_soft_skills,
            "feedback": "Soft skills are important for team fit and leadership.",
            "suggestions": [
                "Add examples of achievements that demonstrate these soft skills.",
                "Include teamwork, communication, and adaptability in your resume."
            ]
        },
        {
            "section": "Certifications",
            "matched": matched_certs,
            "missing": missing_certs,
            "feedback": "Certifications can boost your ATS score and credibility.",
            "suggestions": [
                "List certifications relevant to the job description.",
                "Consider pursuing certifications that match the job requirements."
            ]
        },
        {
            "section": "Experience",
            "matched": ["Experience section found"] if has_experience else [],
            "missing": [] if has_experience else ["No experience section found"],
            "feedback": "Experience section should use role-specific keywords and quantify achievements.",
            "suggestions": [
                "Add quantifiable results and role-specific keywords to your experience section.",
                "Include job titles, dates, and achievements."
            ]
        },
        {
            "section": "Projects",
            "matched": ["Projects section found"] if has_projects else [],
            "missing": [] if has_projects else ["No projects section found"],
            "feedback": "Projects show hands-on skills and initiative.",
            "suggestions": [
                "Describe your projects with context, technologies, and results.",
                "Showcase relevant work and skills."
            ]
        },
        {
            "section": "Education",
            "matched": ["Education section found"] if has_education else [],
            "missing": [] if has_education else ["No education section found"],
            "feedback": "Education section should list degrees, institutions, and relevant coursework.",
            "suggestions": [
                "Add relevant coursework and academic achievements.",
                "Include your degrees and institutions."
            ]
        }
    ]

    # Ensure key_responsibilities and recommended_keywords are always non-empty lists
    if not key_responsibilities or not isinstance(key_responsibilities, list) or not any(key_responsibilities):
        key_responsibilities = get_role_responsibilities("general")
    if not recommended_keywords or not isinstance(recommended_keywords, list) or not any(recommended_keywords):
        recommended_keywords = get_role_keywords("general")


    # --- Professional, actionable, role-specific summary ---
    summary_lines = []
    summary_lines.append(f"This resume was analyzed for the role of '{role_detected}'.")
    if strengths:
        summary_lines.append(f"Key strengths: {', '.join(strengths)}")
    if weaknesses:
        summary_lines.append(f"Areas to improve: {', '.join(weaknesses)}")
    if suggestions:
        summary_lines.append(f"Actionable next steps: {', '.join(suggestions[:3])}")
    summary_lines.append(f"Key responsibilities for this role: {', '.join(key_responsibilities[:3])}")
    summary_lines.append(f"Recommended keywords: {', '.join(recommended_keywords[:5])}")
    summary_lines.append(f"Overall ATS Score: {round(float(overall_score), 2)}% | Tech Stack Coverage: {techstack_coverage}% | Skills Match: {round(float(skills_score), 2)}%")
    summary = "\n".join(summary_lines)

    analysis = {
        "selected_role": selected_role or "",
        "role_detected": role_detected or "",
        "profile_type": "Fresher" if detect_fresher(resume_text) else "Experienced",
        "overall_score": round(float(overall_score), 2),
        "score_breakdown": {
            "skills_match": round(float(skills_score), 2),
            "experience_match": round(float(experience_score), 2),
            "education_match": round(float(education_score), 2)
        },
        "techstack_coverage": techstack_coverage,
        "skills": {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "soft_skills": resume_soft_skills,
            "matched_soft_skills": matched_soft_skills,
            "missing_soft_skills": missing_soft_skills,
            "certifications": resume_certs,
            "matched_certifications": matched_certs,
            "missing_certifications": missing_certs,
            "matched_role_skills": matched_role_skills,
            "missing_role_skills": missing_role_skills
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "feedback": feedback,
        "flaws": flaws if flaws else ["No major flaws detected."],
        "key_responsibilities": key_responsibilities,
        "recommended_keywords": recommended_keywords,
        "detailed_sections": detailed_sections,
        "summary": summary
    }

    return analysis

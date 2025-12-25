# backend/utils/skills.py

import re

ROLE_SKILLS = {
    "data scientist": [
        "python", "pandas", "numpy", "machine learning", "deep learning",
        "statistics", "sql", "tensorflow", "pytorch", "data visualization",
        "scikit-learn", "matplotlib", "seaborn", "data mining", "feature engineering",
        "jupyter", "spark", "hadoop", "big data", "data wrangling", "data preprocessing",
        "regression", "classification", "clustering", "nlp", "natural language processing",
        "model deployment", "mlops", "cloud", "aws", "azure", "gcp"
    ],
    "backend developer": [
        "python", "java", "node", "node.js", "flask", "django", "api", "sql", "mongodb",
        "docker", "aws", "microservices", "rest", "graphql", "postgresql", "redis",
        "spring", "express", "oop", "oop concepts", "unit testing", "integration testing",
        "linux", "nginx", "c#", ".net", "kafka", "rabbitmq", "ci/cd", "azure", "gcp"
    ],
    "frontend developer": [
        "html", "css", "javascript", "react", "tailwind", "ui", "ux",
        "responsive design", "redux", "typescript", "next.js", "vue", "sass",
        "bootstrap", "material ui", "webpack", "babel", "figma", "adobe xd",
        "cross-browser", "accessibility", "testing library", "jest", "cypress"
    ],
    "ai engineer": [
        "machine learning", "deep learning", "nlp", "opencv", "tensorflow",
        "pytorch", "python", "model deployment", "mlops", "huggingface",
        "transformers", "bert", "gpt", "computer vision", "speech recognition",
        "reinforcement learning", "cloud", "aws", "azure", "gcp"
    ],
    "full stack developer": [
        "javascript", "react", "node", "express", "mongodb", "sql", "python",
        "django", "flask", "html", "css", "aws", "docker", "typescript",
        "graphql", "rest", "redux", "sass", "unit testing", "ci/cd", "azure", "gcp"
    ],
    "devops engineer": [
        "docker", "kubernetes", "aws", "azure", "ci/cd", "jenkins", "linux",
        "terraform", "ansible", "monitoring", "prometheus", "grafana",
        "cloudformation", "gcp", "scripting", "bash", "python", "helm", "gitlab ci"
    ],
    "product manager": [
        "roadmap", "agile", "scrum", "stakeholder", "user stories", "jira",
        "market research", "product strategy", "ux", "analytics", "a/b testing",
        "wireframing", "prototyping", "kpi", "go-to-market", "requirements gathering"
    ],
    "data analyst": [
        "sql", "excel", "tableau", "power bi", "python", "data visualization",
        "statistics", "data cleaning", "reporting", "dashboards", "business intelligence",
        "data mining", "pivot tables", "vba", "access", "r", "lookml", "qlik"
    ],
    "machine learning engineer": [
        "python", "machine learning", "deep learning", "tensorflow", "pytorch",
        "model deployment", "mlops", "feature engineering", "scikit-learn",
        "cloud", "aws", "azure", "gcp", "docker", "kubernetes", "data pipelines"
    ],
    "android developer": [
        "java", "kotlin", "android studio", "xml", "jetpack", "firebase",
        "mvvm", "retrofit", "dagger", "material design", "unit testing", "gradle"
    ],
    "ios developer": [
        "swift", "objective-c", "xcode", "cocoa", "cocoapods", "swiftui",
        "core data", "mvvm", "alamofire", "autolayout", "unit testing"
    ]
}

ROLE_RESPONSIBILITIES = {
    "data scientist": [
        "Build and deploy machine learning models",
        "Data cleaning and preprocessing",
        "Statistical analysis and hypothesis testing",
        "Data visualization and reporting",
        "Feature engineering and selection"
    ],
    "backend developer": [
        "Design and implement RESTful APIs",
        "Database schema design and optimization",
        "Server-side logic and integration",
        "Unit and integration testing",
        "Cloud deployment and scaling"
    ],
    "frontend developer": [
        "Develop responsive web interfaces",
        "Implement UI/UX designs",
        "Cross-browser compatibility",
        "State management (Redux, Context API)",
        "Accessibility and performance optimization"
    ],
    # ...add more for each role as needed...
}

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving", "adaptability",
    "critical thinking", "time management", "creativity", "collaboration", "attention to detail"
]

CERTIFICATIONS = [
    "aws certified", "azure certified", "google cloud certified", "pmp", "scrum master",
    "oracle certified", "microsoft certified", "cfa", "cissp", "ccna", "ocp", "ocjp"
]

GENERAL_SKILLS = set(sum(ROLE_SKILLS.values(), []))

def infer_role(job_description: str):
    jd = job_description.lower()
    for role in ROLE_SKILLS:
        if role in jd:
            return role
    # Fallback: keyword match
    for role, skills in ROLE_SKILLS.items():
        for skill in skills:
            if skill in jd:
                return role
    return "general"

def extract_skills(text: str):
    text = text.lower()
    found = set()
    for skill in GENERAL_SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.add(skill)
    return list(found)

def extract_soft_skills(text: str):
    text = text.lower()
    found = set()
    for skill in SOFT_SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.add(skill)
    return list(found)

def extract_certifications(text: str):
    text = text.lower()
    found = set()
    for cert in CERTIFICATIONS:
        if cert in text:
            found.add(cert)
    return list(found)

def get_role_responsibilities(role: str):
    return ROLE_RESPONSIBILITIES.get(role, [])

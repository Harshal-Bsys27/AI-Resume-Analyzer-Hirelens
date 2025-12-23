from sklearn.metrics.pairwise import cosine_similarity
from models.embeddings import embedding_model

def semantic_similarity(text1, text2):
    embeddings = embedding_model.encode([text1, text2])
    score = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]
    return round(score * 100, 2)

def calculate_skills_score(matched, total):
    if total == 0:
        return 0
    return round((len(matched) / total) * 100, 2)

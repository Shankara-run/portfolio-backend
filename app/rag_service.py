import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from . import models

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
faiss_index = None
corpus_map = []
corpus_embeddings = None  # store embeddings for filtering

def build_rag_index(db: Session):
    global faiss_index, corpus_map, corpus_embeddings
    rows = []

    for obj in db.query(models.Objective).all():
        rows.append(f"Objective: {obj.summary}")
    for skill in db.query(models.Skill).all():
        rows.append(f"Skill: {skill.category} - {skill.tools}")
    for exp in db.query(models.Experience).all():
        rows.append(f"Experience: {exp.title} at {exp.company} - {exp.work_description}")
    for edu in db.query(models.Education).all():
        rows.append(f"Education: {edu.institute}, {edu.year}, {edu.category}")
    for proj in db.query(models.Project).all():
        rows.append(f"Project: {proj.title} - {proj.project_description}")

    corpus_map = rows
    if not rows:
        faiss_index = None
        return

    embeddings = embed_model.encode(rows)
    corpus_embeddings = np.array(embeddings, dtype=np.float32)

    dim = corpus_embeddings.shape[1]
    faiss_index = faiss.IndexFlatIP(dim)  # use Inner Product for cosine similarity
    # normalize for cosine similarity
    faiss.normalize_L2(corpus_embeddings)
    faiss_index.add(corpus_embeddings)

    print(f"[RAG] Built FAISS index with {len(rows)} entries")

def semantic_search(query: str, k: int = 1, score_threshold: float = 0.3):
    """Return top-k relevant entries filtered by cosine similarity threshold"""
    global faiss_index, corpus_map

    if faiss_index is None or not corpus_map:
        return []

    # Encode and normalize for cosine similarity
    q_emb = embed_model.encode([query])
    q_emb = np.array(q_emb, dtype=np.float32)
    faiss.normalize_L2(q_emb)

    k = min(k, len(corpus_map))
    distances, indices = faiss_index.search(q_emb, k)  # ✅ Correct call

    results = []
    for score, idx in zip(distances[0], indices[0]):
        if score >= score_threshold:  # ✅ Filter irrelevant rows
            results.append(corpus_map[idx])

    return results

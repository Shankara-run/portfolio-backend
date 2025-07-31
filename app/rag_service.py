import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from . import models

# Load small, fast embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Store FAISS index and corpus map
faiss_index = None
corpus_map = []  # list of strings

def build_rag_index(db: Session):
    """Load all portfolio data into FAISS index"""
    global faiss_index, corpus_map
    rows = []

    # Combine all portfolio info as text for embeddings
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
        print("[RAG] No portfolio data found. FAISS index not built.")
        return

    # ✅ Encode and convert to float32 2D array
    embeddings = embed_model.encode(rows)
    embeddings = np.array(embeddings, dtype=np.float32)

    # ✅ Create FAISS index
    dim = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dim)
    faiss_index.add(embeddings)
    print(f"[RAG] Built FAISS index with {len(rows)} entries, dim={dim}")

def semantic_search(query: str, k: int = 3):
    """Return top-k relevant portfolio entries"""
    if faiss_index is None or not corpus_map:
        return []
    q_emb = embed_model.encode([query])
    q_emb = np.array(q_emb, dtype=np.float32).reshape(1, -1)  # ✅ 2D float32

    # ✅ Ensure k does not exceed corpus size
    k = min(k, len(corpus_map))
    distances, indices = faiss_index.search(q_emb, k)

    return [corpus_map[i] for i in indices[0]]

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from typing import List
from contextlib import asynccontextmanager
import os
import logging
from .database import get_db

from . import models, schemas, chat_routes
from .database import SessionLocal, engine
from .rag_service import build_rag_index

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Build RAG on startup
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info("🔹 Building RAG FAISS index on startup...")
    db = SessionLocal()
    build_rag_index(db)
    db.close()
    yield
    logger.info("🔹 Backend shutting down...")

app = FastAPI(lifespan=app_lifespan)

# DB initialization
models.Base.metadata.create_all(bind=engine)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("✅ FastAPI is loading...")  


# Basic routes
@app.get("/")
def root():
    return {"message": "Portfolio API with RAG is Live!"}

@app.get("/objectives", response_model=list[schemas.Objective])
def get_objectives(db: Session = Depends(get_db)):
    return db.query(models.Objective).all()

@app.get("/skills", response_model=list[schemas.Skill])
def get_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()

@app.get("/experiences", response_model=list[schemas.Experience])
def get_experiences(db: Session = Depends(get_db)):
    return db.query(models.Experience).all()

@app.get("/educations", response_model=list[schemas.Education])
def get_educations(db: Session = Depends(get_db)):
    return db.query(models.Education).all()

@app.get("/projects", response_model=list[schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@app.get("/profile", response_model=list[schemas.Profile])
def get_profile(db: Session = Depends(get_db)):
    return db.query(models.Profile).all()

# Include chat routes
app.include_router(chat_routes.router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "colab_llm_url_set": bool(os.getenv("COLAB_LLM_URL")),
        "message": "Portfolio API is running with Colab LLM"
    }

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
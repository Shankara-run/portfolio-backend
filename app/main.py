from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models,schemas
from .database import SessionLocal, engine

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✅ FastAPI is loading...")  

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message":"Portfolio API is Live!"}

@app.get("/objectives",response_model=list[schemas.Objective])
def get_objectives(db: Session = Depends(get_db)):
    return db.query(models.Objective).all()

@app.get("/Skills",response_model=list[schemas.Skill])
def get_skills(db: Session= Depends(get_db)):
    return db.query(models.Skill).all()

@app.get("/Experiences",response_model=list[schemas.Experience])
def get_Experiences(db: Session=Depends(get_db)):
    return db.query(models.Experience).all()

@app.get("/Education", response_model=list[schemas.Education])
def get_Education(db:Session=Depends(get_db)):
    return db.query(models.Education).all()

@app.get("/Projects",response_model=list[schemas.Project])
def get_projects(db:Session=Depends(get_db)):
    return db.query(models.Project).all()
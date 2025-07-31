from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models,schemas
from .database import SessionLocal, engine
import requests
from typing import List
from . import models, schemas
import time
from .llm_service import initialize_llm_service
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager


from .rag_service import build_rag_index
from .database import SessionLocal
from . import chat_routes

# Initialize LLM service on startup
llm_service = initialize_llm_service()

# Local model configuration
LOCAL_MODEL_PATH = "portfolio-llm-final"  # Model name from trained_models directory
LOCAL_MODEL_URL = "http://localhost:8000"  # URL from your inference server
# ✅ Define lifespan function first
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🔹 Building RAG FAISS index on startup...")
    db = SessionLocal()
    build_rag_index(db)
    db.close()
    yield
    # Shutdown logic (optional)
    print("🔹 Backend shutting down...")

# ✅ Pass lifespan to FastAPI here
app = FastAPI(lifespan=lifespan)

# ✅ Include routers
app.include_router(chat_routes.router)

models.Base.metadata.create_all(bind=SessionLocal().bind)

@app.get("/")
def root():
    return {"message": "Portfolio API with RAG is Live!"}

# Include chat routes
app.include_router(chat_routes.router)


models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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

@app.get("/skills",response_model=list[schemas.Skill])
def get_skills(db: Session= Depends(get_db)):
    return db.query(models.Skill).all()

@app.get("/experiences",response_model=list[schemas.Experience])
def get_Experiences(db: Session=Depends(get_db)):
    return db.query(models.Experience).all()

@app.get("/educations", response_model=list[schemas.Education])
def get_Education(db:Session=Depends(get_db)):
    return db.query(models.Education).all()

@app.get("/projects",response_model=list[schemas.Project])
def get_projects(db:Session=Depends(get_db)):
    return db.query(models.Project).all()

@app.get("/profile", response_model=list[schemas.Profile])
def get_profile(db: Session = Depends(get_db)):
    return db.query(models.Profile).all()
@app.post("/chat/send", response_model=schemas.ChatMessageResponse)
def send_chat_message(chat_data: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    """Send message to local portfolio model and get response"""
    try:
        # Use local LLM service if available
        if llm_service:
            ai_response = llm_service.generate_response(chat_data.message)
        else:
            # Fallback to external API
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": LOCAL_MODEL_PATH,
                "messages": [{"role": "user", "content": chat_data.message}],
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(f"{LOCAL_MODEL_URL}/v1/chat/completions", 
                                   headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
            else:
                return schemas.ChatMessageResponse(success=False, error=f"API Error: {response.status_code}")
        
        # Save to database
        db_message = models.ChatMessage(
            user_message=chat_data.message,
            ai_response=ai_response
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)  # This is critical

        if db_message.id is None:
            raise HTTPException(status_code=500, detail="Failed to save message to database")

        return schemas.ChatMessageResponse(
            success=True,
            response=ai_response,
            message_id=db_message.id  # Now guaranteed to be int
        )
        
    except Exception as e:
        return schemas.ChatMessageResponse(success=False, error=f"Server error: {str(e)}")

@app.get("/chat/history", response_model=List[schemas.ChatHistory])
def get_chat_history(limit: int = 50, db: Session = Depends(get_db)):
    """Get chat history"""
    messages = db.query(models.ChatMessage)\
                .order_by(models.ChatMessage.timestamp.desc())\
                .limit(limit)\
                .all()
    return messages



@app.post("/chat/generate", response_model=schemas.ChatMessageResponse)
def generate_chat_response(request: dict, db: Session = Depends(get_db)):
    """Generate chat response using local LLM server"""
    try:
        instruction = request.get("instruction", "")
        user_input = request.get("input", "")
        max_tokens = request.get("max_tokens", 200)
        temperature = request.get("temperature", 0.7)
        
        # Try local LLM service first
        if llm_service:
            ai_response = llm_service.generate_response(user_input, max_tokens, temperature)
        else:
            # Fallback to LLM server
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "question": user_input,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post("http://localhost:8000/query", 
                                   headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["response"]
            else:
                return {"success": False, "error": f"LLM Server Error: {response.status_code}"}
        
        # Save to database
        db_message = models.ChatMessage(
            user_message=user_input,
            ai_response=ai_response
        )
        db.add(db_message)
        db.commit()
        
        return {"success": True, "output": ai_response}
        
    except Exception as e:
        return {"success": False, "error": f"Server error: {str(e)}"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "model_loaded": llm_service is not None,
        "message": "Portfolio API is running"
    }

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

from sqlalchemy.orm import Session

from contextlib import asynccontextmanager


@app.delete("/chat/history")
async def clear_chat_history(db: Session = Depends(get_db)):
    """Delete all chat messages"""
    try:
        num_deleted = db.query(models.ChatMessage).delete()
        db.commit()
        return {"success": True, "deleted": num_deleted}
    except Exception as e:
        return {"success": False, "error": str(e)}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

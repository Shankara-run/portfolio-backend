# chat_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal
from .llm_service import get_llm_response
from .rag_service import semantic_search

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat/send", response_model=schemas.ChatMessageResponse)
def send_chat_message(chat_data: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    try:
        # Step 1: Get semantic context from DB
        context_list = semantic_search(chat_data.message, k=3)
        context_text = " ".join(context_list) if context_list else "No relevant data found."
        
        # Step 2: Build RAG prompt
        prompt = f"""
You are Arun Shankar's personal AI assistant. 
Answer as if you are Arun himself speaking to an interviewer. 
Speak in first-person, like "I have experience in..." or "I built...".
Only use this portfolio data to answer:
{context_text}
If the answer is not in the data, say: "I don't know based on my profile."

Question from interviewer: {chat_data.message}
Answer as Arun:
"""


        # Step 3: Generate response using local LLM
        ai_response = get_llm_response(prompt)

        # Step 4: Save chat to DB
        db_message = models.ChatMessage(
            user_message=chat_data.message,
            ai_response=ai_response
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return schemas.ChatMessageResponse(
            success=True,
            response=ai_response,
            message_id=db_message.id
        )

    except Exception as e:
        return schemas.ChatMessageResponse(success=False, error=f"Server error: {str(e)}")

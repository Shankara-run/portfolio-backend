# chat_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from .rag_service import semantic_search
from typing import List
import logging

# Hugging Face Transformers
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Chat routes initialized with local FLAN-T5-small LLM and memory support")

router = APIRouter()

# ✅ Load local lightweight LLM once at startup
MODEL_NAME = "google/flan-t5-small"
logger.info(f"Loading local model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# =========================
# Helper: Generate Response
# =========================
def generate_response(user_message: str, context_list: list, memory: str) -> str:
    """Generate a first-person response using flan-t5-small with memory-enabled prompt."""
    # Build context text
    context_text = " ".join(context_list) if context_list else ""
    memory_text = f"Previous conversation: {memory}\n" if memory else ""

    # Simple, memory-aware prompt
    if context_text:
        prompt = (
            f"{memory_text}"
            f"Respond in first person in reference to: {context_text}. "
            f"For the question: {user_message}"
        )
    else:
        # If no context, only rely on memory
        prompt = (
            f"{memory_text}"
            f"Respond in first person. "
            f"For the question: {user_message}"
        )

    # Tokenize and generate
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=128)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Fallback if empty or nonsense
    if not response or response.lower() in ["i don't know", "unknown"]:
        return "I don't have that information in my profile."

    return response

# ======================
# Chat Send Endpoint
# ======================
@router.post("/chat/send", response_model=schemas.ChatMessageResponse)
def send_chat_message(chat_data: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    """Handles a user message, performs semantic search, and generates an AI response with memory."""
    logger.debug(f"Received chat message: {chat_data.message}")
    try:
        # Step 1: Fetch last 2 messages for memory
        history = (
            db.query(models.ChatMessage)
            .order_by(models.ChatMessage.timestamp.desc())
            .limit(2)
            .all()
        )
        # Convert to "User: ... AI: ..." format
        memory = " ".join(
            [f"User: {row.user_message} AI: {row.ai_response}" for row in reversed(history)]
        )
        logger.debug(f"Memory context: {memory}")

        # Step 2: Semantic search in DB (small DB -> k=1)
        context_list = semantic_search(chat_data.message, k=1)
        logger.debug(f"Context from semantic search: {context_list}")

        # Step 3: Generate response locally with memory
        ai_response = generate_response(chat_data.message, context_list, memory)
        logger.debug(f"Generated AI response: {ai_response}")

        # Step 4: Save chat to DB
        db_message = models.ChatMessage(
            user_message=chat_data.message,
            ai_response=ai_response
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        logger.debug(f"Saved message to DB with ID: {db_message.id}")

        # ✅ Return only the AI response
        return schemas.ChatMessageResponse(
            success=True,
            response=ai_response,
            message_id=db_message.id
        )

    except Exception as e:
        logger.exception(f"Error in send_chat_message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ======================
# Chat History Endpoints
# ======================
@router.get("/chat/history", response_model=List[schemas.ChatHistory])
def get_chat_history(limit: int = 50, db: Session = Depends(get_db)):
    """Fetch last N messages from the chat history."""
    rows = (
        db.query(models.ChatMessage)
        .order_by(models.ChatMessage.timestamp.asc())
        .limit(limit)
        .all()
    )
    return [schemas.ChatHistory.from_orm(row) for row in rows]

@router.delete("/chat/history")
def clear_chat_history(db: Session = Depends(get_db)):
    """Clear all chat messages from history."""
    try:
        num_deleted = db.query(models.ChatMessage).delete()
        db.commit()
        return {"success": True, "deleted": num_deleted}
    except Exception as e:
        logger.exception(f"Error in clear_chat_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

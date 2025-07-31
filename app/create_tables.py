from app.database import engine
from app.models import ChatMessage

print("🔹 Dropping old chat_messages table...")
ChatMessage.__table__.drop(engine, checkfirst=True)

print("🔹 Creating new chat_messages table...")
ChatMessage.__table__.create(engine, checkfirst=True)

print("✅ chat_messages table recreated successfully with new columns.")
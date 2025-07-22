
from .database import Base, engine
from . import models  # Make sure all models are imported

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")
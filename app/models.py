from sqlalchemy import Column,Integer, String, Boolean
from app.database import Base

class Objective(Base):
    __tablename__="Objectives"

    id= Column (Integer,primary_key=True,index=True)
    summary= Column(String)
    hidden_summary =  Column(String)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    email = Column(String)
    image = Column(String)
    project_website = Column(String)
    contact = Column(String)
    linkedin = Column(String)
    instagram = Column(String)
    is_hidden = Column(Boolean)


class Skill(Base):
    __tablename__= "Skills"

    id = Column (Integer, primary_key=True, index=True)
    category= Column(String, nullable=False)
    tools= Column(String, nullable=False)
    is_hidden_skill= Column( Boolean , default=False)

class Experience(Base):
    __tablename__= "Experiences"

    id= Column(Integer,primary_key=True, index=True)
    title= Column(String, nullable=False)
    company= Column(String, nullable=False)
    time= Column(String,nullable=False)
    location=Column(String,nullable=False)
    work_description= Column(String, nullable=False)
    is_hidden= Column(Boolean, default=False)

class Education(Base):
    __tablename__= "Educations"

    id = Column(Integer,primary_key=True,index=True)
    institute= Column(String, nullable=False)
    year= Column(String, nullable=False)
    marks= Column(String, nullable=False)
    category= Column(String, nullable=False)
    is_hidden= Column(String, nullable=False)

class Project (Base):
    __tablename__= "Projects"

    id = Column(Integer,primary_key=True, index=True)
    title= Column(String, nullable=False)
    time= Column(String, nullable=False)
    tech_stack= Column (String, nullable=False) 
    project_description= Column(String, nullable=False)
    is_hidden= Column(Boolean, default=False)



from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    user_role = Column(String, default="user")        # interviewer
    ai_role = Column(String, default="assistant")     # Arun AI
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ChatMessageCreate(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    message_id: Optional[int] = None


class ChatHistory(BaseModel):
    id: int
    user_message: str
    ai_response: str
    timestamp: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class Objective(BaseModel):
    id: int
    summary: str
    hidden_summary: str
    
    model_config = ConfigDict(from_attributes=True)

class Profile(BaseModel):
    id: int
    name: str
    title: str
    email: str
    image: str
    project_website: str
    contact: str
    linkedin: str
    instagram: str
    is_hidden: bool
    
    model_config = ConfigDict(from_attributes=True)

class SkillBase(BaseModel):
    category : str
    tools : str
    is_hidden_skill: bool =False

class Skill(SkillBase):
    id:int
    model_config = ConfigDict(from_attributes=True)

class ExperienceBase(BaseModel):
    title : str
    company : str
    time : str
    location : str
    work_description : str
    is_hidden : bool = False

class Experience(ExperienceBase):
    id : int
    model_config = ConfigDict(from_attributes=True)

class EducationBase(BaseModel):
    institute: str
    year: str
    marks: str
    category: str
    is_hidden: bool = False

class Education(EducationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    title:str
    time:str
    tech_stack: str
    project_description:str
    is_hidden: bool = False

class Project(ProjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



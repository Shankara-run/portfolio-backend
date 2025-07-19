from pydantic import BaseModel,ConfigDict

class ObejectiveBase(BaseModel):
    summary: str
    hidden_summary: str

class Objective(ObejectiveBase):
    id: int
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



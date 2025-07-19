from pydantic import BaseModel

class ObejectiveBase(BaseModel):
    summary: str
    hidden_summary: str

class Objective(ObejectiveBase):
    id: int

    class config:
        orm_mode = True
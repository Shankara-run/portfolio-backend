from sqlalchemy import Column,Integer, String
from app.database import Base

class Objective(Base):
    __tablename__="Objectives"

    id= Column (Integer,primary_key=True,index=True)
    summary= Column(String)
    hidden_summary =  Column(String)


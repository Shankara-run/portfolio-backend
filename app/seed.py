from .database import SessionLocal
from .models import Objective

db= SessionLocal()

obj1 = Objective(summary="Building Full-Stack Web Apps",hidden_summary= "Creating Fully-Built Ramen")
obj2 = Objective(summary="Building designing the front End ",hidden_summary= "Creating the serving image")


db.add_all([obj1,obj2])
db.commit()
db.close()
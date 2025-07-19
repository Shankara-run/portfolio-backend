from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Objective
from .models import Skill, Education, Experience, Project

db: Session = SessionLocal()

obj1 = Objective(summary="Building Full-Stack Web Apps",hidden_summary= "Creating Fully-Built Ramen")
obj2 = Objective(summary="Building designing the front End ",hidden_summary= "Creating the serving image")

sample_skills= [
    Skill(category="Frontend", tools="HTML, CSS, JavaScript", is_hidden_skill=False),
    Skill(category="Backend", tools="Java (Spring MVC), Python", is_hidden_skill=False),
    Skill(category= "Creative Tools", tools="Photoshop, Illustrator", is_hidden_skill=False)
]

experience = [
    Experience(
        title= "Senior Resolution Coordinator",
        company= "walmart",
        time="2023-2025",
        location= "Chennai, Tamil Nadu",
        work_description= "Invertigated fraud cases",
        is_hidden= False
    ),
    Experience(
        title= "Volunteer Chef",
        company= "South Indian & French Bakery",
        time= "2022-2023",
        location= "Kullu, Himachal Pradesh",
        work_description= "Managed kitchen and guided tourists",
        is_hidden= True
    )
]
education = [
    Education(
        institute= "Sri Venteshwara College of Engineering",
        year="2016",
        marks="CGPA: 6.62",
        category="B.Tech Information Technology",
        is_hidden= False
    ),
    Education(
        institute= "Image institute of Graphic Design",
        year="2020",
        marks="First Class",
        category= "Graphic Design",
        is_hidden= True
    )
]

projects= [
    Project(
        title="Spend & Matter Management Web App",
        time= "2016",
        tech_stack= "Java (Spring MVC), JavaScript, SQL Server",
        project_description= "Build prototype with login, sprend tracking ",
        is_hidden= False
    ),
    Project(
        title="Save Mother Earth",
        time= "2019",
        tech_stack= "Adobe After Effects, Adobe Premiere Pro",
        project_description= "A project to show and experience a Music beats mapped video",
        is_hidden= True
    )
]
db.add_all([obj1,obj2])
db.add_all(sample_skills)
db.add_all(experience)
db.add_all(education)
db.add_all(projects)
db.commit()
db.close()
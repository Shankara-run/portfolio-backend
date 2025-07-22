from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Objective
from app.models import Skill, Education, Experience, Project
from app.models import Profile 

db: Session = SessionLocal()

obj1 = Objective(summary="I am a Dedicated and adaptable developer with a foundation in backend systems, enterprise-grade software support, and technical operations. With over 4 years of hands-on experience across software engineering, fraud systems, and platform support, I aim to contribute to reliable, scalable backend solutions. My broader experience running real-world operations also helps me support teams with ownership, clarity, and coordination.",
                 hidden_summary= "Hands-on experience in food service, business operations, and creative projects. Managed daily operations, supported kitchen teams, and worked on customer experience. Also contributed to branding and marketing efforts for small businesses. Skilled in coordination, problem-solving, and delivering practical solutions across diverse work environments.")

sample_skills= [
    Skill(category="Styling", tools="HTML, CSS, Tailwind", is_hidden_skill=False),
    Skill(category="Backend", tools="Spring MVC, FastApi", is_hidden_skill=False),
    Skill(category="Languages", tools="Java, Python, C++", is_hidden_skill=False),
    Skill(category= "Design Tools", tools="Photoshop, Illustrator, After effects", is_hidden_skill=True),
    Skill(category= "Cusines ", tools="Continental, Japanese, Chettinad, Baking", is_hidden_skill=True),
    Skill(category= "Travel & Tourism", tools=" Customer Service, Cultural awarness, Camping, Biker", is_hidden_skill=True),

]

experience = [
    Experience(
        title= "Associate Software Developer ",
        company= "Wolters Kluwer",
        time="Jul 2016 – Mar 2018 ",
        location= "Chennai, Tamil Nadu",
        work_description= "Worked on Java Spring MVC apps and debugged JavaScript errors. Created detailed documentation, resolved backend issues, provided updated packages, supported live users, and improved workflows by identifying and fixing system inefficiencies.",
        is_hidden= False
    ),
    Experience(
        title= "Software Development Intern ",
        company= "Wolters Kluwer",
        time="Dec 2016 – Mar 2016",
        location= "Chennai, Tamil Nadu",
        work_description= "Completed training in Java (Spring MVC) and .NET during internship. Assisted in debugging code, writing test cases, and learning corporate workflows. Gained exposure to software delivery processes, document management systems, and version control tools.",
        is_hidden= False
    ),
      Experience(
        title= "Senior Resolution Coordinator",
        company= "Walmart",
        time="Nov 2023 – Mar 2025",
        location= "Chennai, Tamil Nadu",
        work_description= "Supervised backend fraud detection workflows, investigated fraud patterns using order databases, and ensured SLA compliance. Collaborated across teams and systems, using SQL and internal tools to verify data integrity and support secure operations.",
        is_hidden= False
    ),
     Experience(
        title= "Technical Support Associate",
        company= "Prompt ",
        time="Apr 2023 – Oct 2023 ",
        location= "Chennai, Tamil Nadu",
        work_description= "Provided real-time support for Kindle and Alexa systems, analyzing logs and firmware behavior. Followed technical SOPs to troubleshoot issues and ensure consistent customer resolution through clear debugging and escalation practices.",
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
        year="2012 - 2016",
        marks="CGPA: 6.62",
        category="B.Tech Information Technology",
        is_hidden= False
    ),
     Education(
        institute= "Sita Devi Garodia Hindu Vidyalaya (State Board), Chennai",
        year="2010 - 2012",
        marks="1132 / 1200 (94.3%)",
        category="Computer Science",
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
        tech_stack= "Eclipse IDE | Java (Spring MVC) | Microsoft SQL Server | Tomcat | 2016",
        project_description= "Designed a basic web app with user login and data entry features, fully connected to a backend database. Built interactive front-end forms with input checks using JavaScript. Developed and tested the project using Eclipse IDE and deployed it locally on Apache Tomcat for demonstration.",
        is_hidden= False
    ),
    Project(
        title="Digital Products ECart – Desktop Application",
        time= "2015",
        tech_stack= "Visual Basic | .NET | Microsoft Access | XML ",
        project_description= "Created a simple e-commerce prototype using Microsoft Access and Visual Basic. Designed linked database tables for users, products, and orders. Built a user interface with login, product listing, and checkout features. Used XML to load products and save cart data for flexible data handling with the Access database.",
        is_hidden= False
    ),
   
    Project(
        title="Personal Portfolio Website ",
        time= "2025",
        tech_stack= "VS Code | FastAPI (Python) | SQLite | React | Tailwind CSS ",
        project_description= "Created a portfolio website with a FastAPI backend and SQLite for storing content. Built a responsive React frontend using Tailwind CSS for clean UI components. Connected backend APIs to dynamically display project details, skills, and timeline data throughout the site.",
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


profiles = [
    Profile(
        name="Arun Shankar",
        title="Full-Stack Developer",
        email="shankararunofficial@gmail.com",
        linkedin="https://www.linkedin.com/in/arun-shankar-t-s",
        instagram="https://www.instagram.com/arun_shankar04/",
        project_website="https://github.com/Shankara-run",
        image="/images/main_profile.jpg",
        contact="915-048-6527",
        is_hidden=False
    ),
    Profile(
        name="Shankara",
        title="Freelance Bussiness Operations",
        email="tsarunshankar@email.com",
        linkedin="https://www.linkedin.com/in/arun-shankar-t-s",
        instagram="https://www.instagram.com/shankara_in_kasol",
        project_website="https://www.behance.net/arunshankarts",
        image="/images/hidden_profile.jpg",
        contact="915-048-6527",
        is_hidden=True
    )
]

db.add_all(profiles)

db.add_all([obj1])
db.add_all(sample_skills)
db.add_all(experience)
db.add_all(education)
db.add_all(projects)
db.commit()
db.close()


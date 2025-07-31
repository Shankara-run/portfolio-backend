from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Objective
from app.models import Skill, Education, Experience, Project
from app.models import Profile 

from app import models
from app.rag_service import build_rag_index

# Start DB session
db: Session = SessionLocal()

# Step 1: Clear old data
print("Clearing old data...")
for table in [models.Objective, models.Skill, models.Education, models.Experience, models.Project, models.Profile]:
    db.query(table).delete()
db.commit()

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
        title= "Manager (Operations & Guest Experience)",
        company= "Himalayan Vegan Café",
        time= "Mar 2022 – Aug 2022 ",
        location= "Kullu, Himachal Pradesh",
        work_description= "Oversaw customer satisfaction, curated seasonal menus, and organized logistics for trekking groups.",
        is_hidden= True
    ),
    Experience(
        title= "Volunteer Production assistant and Social Marketer",
        company= "Chotus French Bakery",
        time= "Mar 2022 – Aug 2022 ",
        location= "Pushkar, Rajasthan",
        work_description= "Supported artisanal French baking under a European-trained master baker.",
        is_hidden= True
    ),
    Experience(
        title= "Junior Sous Chef ",
        company= "Sorissa Fine Dining Restaurant",
        time= "Sep 2021 – Feb 2022 ",
        location= "Pernem, Goa",
        work_description= "Worked under a Marriott-experienced head chef preparing continental, seafood, and gourmet cuisines.",
        is_hidden= True
    ),
    Experience(
        title= "Kitchen Operations Intern ",
        company= "Diff42 Restro Bar",
        time= "Mar 2021 – Aug 2021 ",
        location= "Chennai, Tamil Nadu",
        work_description= "Developed speed and precision in knife work, pan techniques, and kitchen coordination.",
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
        title="Personal Portfolio Chat Agent",
        time= "2025",
        tech_stack= "VS Code | AI | ML | LLM | RAG ",
        project_description= "Added Seperate additional component for chat in Portfolio, with a pre-trained llm and a RAG defined from the datasets in the website",
        is_hidden= False
    ),
    Project(
        title="Personal Portfolio Website Backend",
        time= "2025",
        tech_stack= "VS Code | FastAPI | Python | SQLite ",
        project_description= "Created a portfolio backend with proper modules schemas and API endpoints",
        is_hidden= False
    ),
    Project(
        title="Personal Portfolio Website Frontend",
        time= "2025",
        tech_stack= "VS Code | React | Tailwind CSS ",
        project_description= "Built a responsive React frontend using Tailwind CSS for clean UI components. Connected backend APIs to dynamically display project details, skills, and timeline data throughout the site.",
        is_hidden= False
    ),
     Project(
        title="CPU Temp",
        time= "2025",
        tech_stack= "VS Code | Python | WMI interface | CLI | Python ",
        project_description= "Created a CLI app to check the CPU temperature from WMI a core component of Windows that provides a standardized interface for accessing and managing system information and operations",
        is_hidden= False
    ),

    Project(
        title="Save Mother Earth",
        time= "2019",
        tech_stack= "Adobe After Effects, Adobe Premiere Pro",
        project_description= "A project experiment to display waves in 360* mapped to the music beats in a video",
        is_hidden= True
    ),
      Project(
        title="Personal Portait depicted in the Future",
        time= "2019",
        tech_stack= "Adobe Photoshop, Adobe Illustrator",
        project_description= "A project experiment to trace my image to a vector format",
        is_hidden= True
    ),
    Project(
        title="Food & Travel Research Project",
        time= "Jan 2021 – Feb 2021 ",
        tech_stack= "Solo Ride, 4000kms in single strech, Rode acros 8 Indian states ",
        project_description= "Collected documentation for potential brand content development and experiential tourism mapping.",
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
        linkedin="https://www.instagram.com/shankara_in_kasol",
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


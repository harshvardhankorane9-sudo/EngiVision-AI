"""
Career Intelligence Engine — Database Models & Seed Data
SQLAlchemy ORM for SQLite (dev) / PostgreSQL (prod)
Branches: CSE | CSE AIML | Mechanical | Electronics
"""

import os
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    JSON, Text, ForeignKey, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# ---------------------------------------------------------------------------
# ORM Models
# ---------------------------------------------------------------------------

class Student(Base):
    __tablename__ = "students"
    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(255), nullable=False)
    email        = Column(String(255), unique=True, index=True, nullable=False)
    college      = Column(String(255), default="")
    branch_year  = Column(Integer, default=1)
    created_at   = Column(DateTime, default=datetime.utcnow)

    assessments  = relationship("Assessment", back_populates="student", cascade="all, delete-orphan")
    simulations  = relationship("SimulationRecord", back_populates="student", cascade="all, delete-orphan")
    chats        = relationship("ChatSession", back_populates="student", cascade="all, delete-orphan")


class Branch(Base):
    __tablename__ = "branches"
    id               = Column(Integer, primary_key=True, index=True)
    code             = Column(String(30), unique=True, nullable=False)   # CSE | CSE-AIML | MECH | ECE
    name             = Column(String(255), nullable=False)
    tagline          = Column(String(255))
    description      = Column(Text)
    core_subjects    = Column(JSON)   # list[str]
    core_skills      = Column(JSON)   # list[str]
    skill_weights    = Column(JSON)   # {dimension: weight 0-1}
    career_paths     = Column(JSON)   # list[str]
    top_recruiters   = Column(JSON)   # list[str]
    certifications   = Column(JSON)   # list[str]
    higher_studies   = Column(JSON)   # list[str]
    future_scope     = Column(Text)
    entry_salary     = Column(String(50))
    mid_salary       = Column(String(50))
    senior_salary    = Column(String(50))
    growth_rate      = Column(String(30))
    job_openings     = Column(String(30))
    color            = Column(String(20), default="#667eea")  # for UI


class Assessment(Base):
    __tablename__ = "assessments"
    id                  = Column(Integer, primary_key=True, index=True)
    student_id          = Column(Integer, ForeignKey("students.id"), nullable=False)
    raw_answers         = Column(JSON)
    skill_scores        = Column(JSON)   # {dimension: score}
    recommended_branches= Column(JSON)   # [{code, name, match_pct, explanation}]
    confidence          = Column(Float, default=0.0)
    completed_at        = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="assessments")


class SimulationRecord(Base):
    __tablename__ = "simulation_records"
    id             = Column(Integer, primary_key=True, index=True)
    student_id     = Column(Integer, ForeignKey("students.id"), nullable=False)
    branch_code    = Column(String(30), nullable=False)
    decisions      = Column(JSON, default=list)   # [{scenario_id, choice, score}]
    total_score    = Column(Float, default=0.0)
    max_score      = Column(Float, default=0.0)
    percentage     = Column(Float, default=0.0)
    performance    = Column(String(50), default="")
    is_complete    = Column(Boolean, default=False)
    started_at     = Column(DateTime, default=datetime.utcnow)
    completed_at   = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="simulations")


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    student  = relationship("Student", back_populates="chats")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id         = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role       = Column(String(20), nullable=False)   # user | assistant
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


# ---------------------------------------------------------------------------
# DB engine / session
# ---------------------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./career_intelligence.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Seed the 4 branches
# ---------------------------------------------------------------------------

BRANCHES = [
    {
        "code": "CSE",
        "name": "Computer Science & Engineering",
        "tagline": "Build the software that runs the world",
        "color": "#4f46e5",
        "description": (
            "CSE is the foundation of modern technology. You'll master algorithms, "
            "data structures, operating systems, databases, and software engineering. "
            "Graduates build everything from mobile apps to cloud infrastructure."
        ),
        "core_subjects": [
            "Data Structures & Algorithms", "Operating Systems", "DBMS",
            "Computer Networks", "Software Engineering", "Compiler Design",
            "Theory of Computation", "Web Development"
        ],
        "core_skills": [
            "Python / Java / C++", "DSA & Problem Solving", "System Design",
            "Web / App Development", "Databases (SQL, NoSQL)", "Git & DevOps"
        ],
        "skill_weights": {
            "coding":           0.95,
            "mathematics":      0.70,
            "analytical":       0.85,
            "hardware":         0.20,
            "creativity":       0.60,
            "research":         0.50,
            "communication":    0.55,
            "entrepreneurship": 0.60
        },
        "career_paths": [
            "Software Development Engineer (SDE)",
            "Backend / Frontend / Full-Stack Developer",
            "DevOps & Cloud Engineer",
            "Database Administrator",
            "System Architect",
            "Technical Product Manager"
        ],
        "top_recruiters": [
            "Google", "Microsoft", "Amazon", "Flipkart",
            "Infosys", "TCS", "Wipro", "Atlassian", "Adobe"
        ],
        "certifications": [
            "AWS Solutions Architect", "Google Cloud Professional",
            "Meta Full-Stack Developer", "Oracle Java SE"
        ],
        "higher_studies": ["M.Tech CSE", "MS Abroad", "MBA (Tech)", "PhD CS"],
        "future_scope": (
            "Software demand is growing 25% YoY. Cloud, cybersecurity, and "
            "distributed systems are hot areas. CSE grads have the widest job market."
        ),
        "entry_salary":  "6–14 LPA",
        "mid_salary":    "18–40 LPA",
        "senior_salary": "50–120 LPA",
        "growth_rate":   "+25% YoY",
        "job_openings":  "~3.5 Lakh"
    },
    {
        "code": "CSE-AIML",
        "name": "CSE with AI & Machine Learning",
        "tagline": "Engineer the intelligence of tomorrow",
        "color": "#7c3aed",
        "description": (
            "CSE-AIML is CSE supercharged with deep learning, NLP, computer vision, "
            "and MLOps. You'll build intelligent systems that learn from data — "
            "from recommendation engines to autonomous systems."
        ),
        "core_subjects": [
            "Machine Learning", "Deep Learning", "Natural Language Processing",
            "Computer Vision", "Data Science & Analytics", "Reinforcement Learning",
            "Big Data Engineering", "Probability & Statistics"
        ],
        "core_skills": [
            "Python (NumPy, Pandas, Scikit-learn)", "TensorFlow / PyTorch",
            "Data Preprocessing & EDA", "Model Deployment (MLOps)",
            "Statistics & Probability", "SQL & NoSQL for Big Data"
        ],
        "skill_weights": {
            "coding":           0.90,
            "mathematics":      0.92,
            "analytical":       0.95,
            "hardware":         0.15,
            "creativity":       0.65,
            "research":         0.80,
            "communication":    0.55,
            "entrepreneurship": 0.55
        },
        "career_paths": [
            "Machine Learning Engineer",
            "Data Scientist",
            "AI Research Scientist",
            "NLP / Computer Vision Engineer",
            "MLOps / AI Platform Engineer",
            "Generative AI Engineer"
        ],
        "top_recruiters": [
            "Google DeepMind", "OpenAI", "Microsoft AI", "Amazon",
            "NVIDIA", "Zomato", "PhonePe", "Meesho", "Fractal Analytics"
        ],
        "certifications": [
            "TensorFlow Developer Certificate", "AWS ML Specialty",
            "Google Professional ML Engineer", "Coursera Deep Learning Specialization"
        ],
        "higher_studies": ["M.Tech AI/ML", "MS in CS (ML focus)", "PhD AI", "MBA (Data)"],
        "future_scope": (
            "AI is the fastest-growing tech field. Generative AI, LLMs, and autonomous "
            "systems are creating entirely new industries. This is the highest-paying "
            "tech specialisation globally."
        ),
        "entry_salary":  "8–18 LPA",
        "mid_salary":    "20–45 LPA",
        "senior_salary": "60–150 LPA",
        "growth_rate":   "+40% YoY",
        "job_openings":  "~1.8 Lakh"
    },
    {
        "code": "MECH",
        "name": "Mechanical Engineering",
        "tagline": "Design and build the physical world",
        "color": "#d97706",
        "description": (
            "Mechanical Engineering is the broadest engineering discipline — spanning "
            "thermodynamics, fluid mechanics, manufacturing, robotics, and product design. "
            "Mechs design everything from engines to spacecraft."
        ),
        "core_subjects": [
            "Engineering Mechanics (Statics & Dynamics)", "Thermodynamics",
            "Fluid Mechanics", "Strength of Materials",
            "Manufacturing Processes", "Theory of Machines",
            "Heat Transfer", "CAD / CAM / FEA"
        ],
        "core_skills": [
            "AutoCAD / SolidWorks / CATIA", "FEA (ANSYS, Abaqus)",
            "Manufacturing & Machining", "Thermodynamic Analysis",
            "Robotics & Automation (ROS)", "MATLAB / Python for simulation"
        ],
        "skill_weights": {
            "coding":           0.40,
            "mathematics":      0.80,
            "analytical":       0.75,
            "hardware":         0.85,
            "creativity":       0.80,
            "research":         0.55,
            "communication":    0.60,
            "entrepreneurship": 0.55
        },
        "career_paths": [
            "Design Engineer",
            "Manufacturing / Production Engineer",
            "Automotive / Aerospace Engineer",
            "Robotics & Automation Engineer",
            "HVAC / Thermal Systems Engineer",
            "R&D Scientist"
        ],
        "top_recruiters": [
            "Tata Motors", "Mahindra", "L&T", "ISRO", "DRDO",
            "Bosch", "Cummins India", "Siemens", "John Deere", "Eaton"
        ],
        "certifications": [
            "SolidWorks CSWA / CSWP", "AutoCAD Certified Professional",
            "Six Sigma Green Belt", "PMP (Project Management)"
        ],
        "higher_studies": [
            "M.Tech Manufacturing / Thermal", "MS Mechanical Engineering",
            "MBA Operations", "M.Tech Robotics"
        ],
        "future_scope": (
            "EV revolution, Industry 4.0, additive manufacturing (3D printing), "
            "and defense modernisation are driving huge demand. "
            "Mechs who learn coding + simulation are premium hires."
        ),
        "entry_salary":  "4–9 LPA",
        "mid_salary":    "12–22 LPA",
        "senior_salary": "25–55 LPA",
        "growth_rate":   "+12% YoY",
        "job_openings":  "~2.2 Lakh"
    },
    {
        "code": "ECE",
        "name": "Electronics & Communication Engineering",
        "tagline": "Power the signals that connect everything",
        "color": "#0891b2",
        "description": (
            "ECE blends electronics, signal processing, communication systems, "
            "and embedded programming. ECE engineers design chips, build wireless systems, "
            "create IoT devices, and work on 5G and satellite communication."
        ),
        "core_subjects": [
            "Analog & Digital Electronics", "Signals & Systems",
            "Digital Signal Processing", "Communication Systems",
            "Microprocessors & Embedded Systems", "VLSI Design",
            "Antenna & RF Engineering", "Control Systems"
        ],
        "core_skills": [
            "Circuit Design (Analog + Digital)", "Embedded C / RTOS",
            "MATLAB / Simulink", "PCB Design (KiCAD / Altium)",
            "FPGA / Verilog / VHDL", "Communication Protocols (SPI, I2C, UART)"
        ],
        "skill_weights": {
            "coding":           0.65,
            "mathematics":      0.80,
            "analytical":       0.80,
            "hardware":         0.95,
            "creativity":       0.55,
            "research":         0.60,
            "communication":    0.55,
            "entrepreneurship": 0.45
        },
        "career_paths": [
            "Embedded Systems Engineer",
            "VLSI / Chip Design Engineer",
            "RF / Communication Engineer",
            "IoT Solutions Architect",
            "Signal Processing Engineer",
            "Telecom Network Engineer"
        ],
        "top_recruiters": [
            "Intel", "Qualcomm", "Texas Instruments", "Samsung Semiconductor",
            "ISRO", "Airtel", "Jio", "STMicroelectronics", "NXP", "MediaTek"
        ],
        "certifications": [
            "ARM Certified Engineer", "Cisco CCNA",
            "Certified IoT Professional (CIoTP)", "Cadence PCB Design"
        ],
        "higher_studies": [
            "M.Tech VLSI", "M.Tech Signal Processing",
            "MS ECE Abroad", "M.Tech Embedded Systems"
        ],
        "future_scope": (
            "5G rollout, semiconductor self-reliance (India Chip Mission), "
            "IoT explosion, and space-tech boom are creating massive ECE demand. "
            "VLSI engineers are among the highest-paid hardware professionals."
        ),
        "entry_salary":  "5–11 LPA",
        "mid_salary":    "14–28 LPA",
        "senior_salary": "30–70 LPA",
        "growth_rate":   "+18% YoY",
        "job_openings":  "~1.5 Lakh"
    }
]


def seed_branches(db):
    if db.query(Branch).count() > 0:
        return
    for b in BRANCHES:
        db.add(Branch(**b))
    db.commit()
    print(f"✅ Seeded {len(BRANCHES)} branches")


# ---------------------------------------------------------------------------
# Run directly to initialise
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    init_database()
    db = SessionLocal()
    seed_branches(db)
    db.close()
    print("🎉 Database ready!")

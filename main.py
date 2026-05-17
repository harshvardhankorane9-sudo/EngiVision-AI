"""
Career Intelligence Engine — FastAPI Backend v3.1
KEY FIX: Simulator is now fully STATELESS — no in-memory session dict.
         All state lives in the Streamlit frontend. Backend is a pure function.
New:  /api/v1/simulator/decide  (stateless — replaces /simulator/decision)
New:  /api/v1/cutoffs/{branch_code}
New:  /api/v1/roadmap/{branch_code}
Run:  python main.py   or   uvicorn main:app --reload --port 8000
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import (
    Branch, ChatMessage, ChatSession, Assessment,
    SimulationRecord, Student,
    SessionLocal, get_db, init_database, seed_branches,
)
from skill_mapper import SkillMapper, run_assessment
from simulator import DayInLifeSimulator
from rag_engine import RAGEngine

# ─────────────────────────────────────────────────────────────────────────────
# App & singletons
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Career Intelligence Engine",
    description="CSE | CSE-AIML | Mechanical | Electronics counselling API",
    version="3.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"],
    allow_headers=["*"], allow_credentials=True,
)

_skill_mapper = SkillMapper()
_simulator    = DayInLifeSimulator()
_rag          = RAGEngine()


@app.on_event("startup")
async def on_startup():
    init_database()
    db = SessionLocal()
    try:
        seed_branches(db)
    finally:
        db.close()
    print("✅  Career Intelligence Engine v3.1 ready")
    print("📚  Swagger docs → http://localhost:8000/docs")


# ─────────────────────────────────────────────────────────────────────────────
# Pydantic models
# ─────────────────────────────────────────────────────────────────────────────

class StudentRegister(BaseModel):
    name:        str
    email:       str
    college:     Optional[str] = ""
    branch_year: Optional[int] = 1

class AssessmentAnswers(BaseModel):
    student_id: Optional[int] = None
    answers:    Dict[str, Any]

class ChatRequest(BaseModel):
    session_id: Optional[int] = None
    student_id: Optional[int] = None
    message:    str

class SimStartRequest(BaseModel):
    student_id:  Optional[int] = None
    branch_code: str

class SimDecideRequest(BaseModel):
    """
    Stateless — no session key needed.
    Frontend sends branch_code + scenario_index + choice_id every time.
    all_decisions is the accumulated list (used for final score on last scenario).
    """
    branch_code:    str
    scenario_index: int                        # 0-based
    choice_id:      str                        # "A" | "B" | "C"
    student_id:     Optional[int] = None
    all_decisions:  Optional[List[Dict]] = []  # [{scenario_index, choice_id, score}]


# ─────────────────────────────────────────────────────────────────────────────
# Health
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "service": "Career Intelligence Engine", "version": "3.1.0"}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {
        "status":   "healthy",
        "branches": db.query(Branch).count(),
        "students": db.query(Student).count(),
        "rag_docs": _rag.get_stats()["total_docs"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Students
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/v1/students/register")
def register_student(data: StudentRegister, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == data.email).first()
    if existing:
        return {"student": {"id": existing.id, "name": existing.name,
                            "email": existing.email}, "message": "Welcome back!"}
    s = Student(name=data.name, email=data.email,
                college=data.college or "", branch_year=data.branch_year or 1)
    db.add(s); db.commit(); db.refresh(s)
    return {"student": {"id": s.id, "name": s.name, "email": s.email},
            "message": "Registered successfully!"}

@app.get("/api/v1/students/{student_id}/dashboard")
def student_dashboard(student_id: int, db: Session = Depends(get_db)):
    s = db.query(Student).filter(Student.id == student_id).first()
    if not s:
        raise HTTPException(404, "Student not found")
    return {
        "total_assessments": db.query(Assessment).filter(Assessment.student_id == student_id).count(),
        "total_simulations": db.query(SimulationRecord).filter(SimulationRecord.student_id == student_id).count(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Branches
# ─────────────────────────────────────────────────────────────────────────────

def _bdict(b: Branch) -> Dict:
    return {
        "code": b.code, "name": b.name, "tagline": b.tagline,
        "description": b.description, "core_subjects": b.core_subjects,
        "core_skills": b.core_skills, "career_paths": b.career_paths,
        "top_recruiters": b.top_recruiters, "certifications": b.certifications,
        "higher_studies": b.higher_studies, "future_scope": b.future_scope,
        "entry_salary": b.entry_salary, "mid_salary": b.mid_salary,
        "senior_salary": b.senior_salary, "growth_rate": b.growth_rate,
        "job_openings": b.job_openings, "color": b.color,
    }

@app.get("/api/v1/branches")
def list_branches(db: Session = Depends(get_db)):
    return {"branches": [_bdict(b) for b in db.query(Branch).all()]}

@app.get("/api/v1/branches/{code}")
def get_branch(code: str, db: Session = Depends(get_db)):
    b = db.query(Branch).filter(Branch.code == code.upper()).first()
    if not b:
        raise HTTPException(404, f"Branch '{code}' not found")
    return _bdict(b)


# ─────────────────────────────────────────────────────────────────────────────
# Skill Assessment
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/v1/assessment/questions")
def get_questions():
    qs = _skill_mapper.get_questions()
    return {"questions": qs, "total_questions": len(qs)}

@app.post("/api/v1/assessment/submit")
def submit_assessment(data: AssessmentAnswers, db: Session = Depends(get_db)):
    result = run_assessment(data.answers)
    aid = None
    if data.student_id:
        s = db.query(Student).filter(Student.id == data.student_id).first()
        if s:
            rec = Assessment(
                student_id=data.student_id, raw_answers=data.answers,
                skill_scores=result["skill_scores"],
                recommended_branches=result["recommended_branches"],
                confidence=result["confidence"],
            )
            db.add(rec); db.commit(); db.refresh(rec)
            aid = rec.id
    return {
        "skill_scores":         result["skill_scores"],
        "recommended_branches": result["recommended_branches"],
        "confidence":           result["confidence"],
        "assessment_id":        aid,
    }

@app.get("/api/v1/assessment/history/{student_id}")
def assessment_history(student_id: int, db: Session = Depends(get_db)):
    recs = (db.query(Assessment)
              .filter(Assessment.student_id == student_id)
              .order_by(Assessment.completed_at.desc()).limit(10).all())
    return {"total": len(recs), "sessions": [{
        "id": r.id, "completed_at": r.completed_at.isoformat(),
        "confidence": r.confidence,
        "results": {"skill_scores": r.skill_scores,
                    "recommended_branches": r.recommended_branches,
                    "confidence_score": r.confidence},
    } for r in recs]}


# ─────────────────────────────────────────────────────────────────────────────
# Day-in-Life Simulator  — FULLY STATELESS
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/v1/simulator/branches")
def sim_branches():
    return {"branches": [_simulator.get_branch_info(c)
                         for c in _simulator.get_available_branches()]}

@app.get("/api/v1/simulator/intro/{branch_code}")
def sim_intro(branch_code: str):
    """Return the rich branch intro (daily tasks, tools, video ID) for the pre-sim screen."""
    intro = _simulator.get_intro(branch_code.upper())
    if not intro:
        raise HTTPException(404, f"Intro for '{branch_code}' not found")
    return intro

@app.post("/api/v1/simulator/start")
def sim_start(data: SimStartRequest):
    """Returns first scenario. Zero server-side state stored."""
    code = data.branch_code.upper()
    s = _simulator.get_scenario(code, 0)
    if not s:
        raise HTTPException(400, f"No scenarios for branch '{code}'")
    return {"branch_code": code, "branch_name": s["branch_name"],
            "total_scenarios": s["total"], "scenario": s}

@app.post("/api/v1/simulator/decide")
def sim_decide(data: SimDecideRequest, db: Session = Depends(get_db)):
    """
    Pure-function decision endpoint — no server session required.
    Evaluates choice, returns feedback + next scenario (or final).
    """
    code = data.branch_code.upper()
    fb = _simulator.evaluate_choice(code, data.scenario_index, data.choice_id)
    if "error" in fb:
        raise HTTPException(400, fb["error"])

    response: Dict[str, Any] = {"feedback": fb}

    if fb["is_last"]:
        decisions = list(data.all_decisions or [])
        decisions.append({"scenario_index": data.scenario_index,
                          "choice_id": data.choice_id, "score": fb["score"]})
        final = _simulator.calculate_final_score(decisions)
        response["final"] = final
        if data.student_id:
            try:
                rec = SimulationRecord(
                    student_id=data.student_id, branch_code=code,
                    decisions=decisions, total_score=final["total_score"],
                    max_score=final["max_score"], percentage=final["percentage"],
                    performance=final["level"], is_complete=True,
                    completed_at=datetime.now(),
                )
                db.add(rec); db.commit()
            except Exception:
                pass
    else:
        response["next_scenario"] = _simulator.get_scenario(code, fb["next_index"])

    return response

@app.get("/api/v1/simulator/history/{student_id}")
def sim_history(student_id: int, db: Session = Depends(get_db)):
    recs = (db.query(SimulationRecord)
              .filter(SimulationRecord.student_id == student_id)
              .order_by(SimulationRecord.started_at.desc()).limit(20).all())
    return {"total": len(recs), "records": [{
        "id": r.id, "branch_code": r.branch_code,
        "percentage": r.percentage, "performance": r.performance,
        "started_at": r.started_at.isoformat(),
    } for r in recs]}


# ─────────────────────────────────────────────────────────────────────────────
# RAG Chat
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/v1/chat/start")
def chat_start(student_id: Optional[int] = None, db: Session = Depends(get_db)):
    sess = ChatSession(student_id=student_id)
    db.add(sess); db.commit(); db.refresh(sess)
    return {
        "session_id": sess.id,
        "initial_message": (
            "Hi! 👋 I'm your Career Counsellor. Ask me anything about "
            "CSE, CSE-AIML, Mechanical, or Electronics — placements, "
            "salaries, GATE, Pune college cutoffs, or career paths!"
        ),
    }

@app.post("/api/v1/chat/message")
def chat_message(data: ChatRequest, db: Session = Depends(get_db)):
    sid = data.session_id
    if not sid:
        sess = ChatSession(student_id=data.student_id)
        db.add(sess); db.commit(); db.refresh(sess)
        sid = sess.id
    db.add(ChatMessage(session_id=sid, role="user", content=data.message))
    result = _rag.answer(data.message)
    db.add(ChatMessage(session_id=sid, role="assistant", content=result["answer"]))
    db.commit()
    return {"session_id": sid, "message": result["answer"],
            "sources": result.get("sources", []), "confidence": result.get("confidence", 0.75)}

@app.get("/api/v1/chat/history/{session_id}")
def chat_history(session_id: int, db: Session = Depends(get_db)):
    msgs = (db.query(ChatMessage).filter(ChatMessage.session_id == session_id)
              .order_by(ChatMessage.created_at).all())
    return {"session_id": session_id, "messages": [
        {"role": m.role, "content": m.content, "at": m.created_at.isoformat()}
        for m in msgs
    ]}


# ─────────────────────────────────────────────────────────────────────────────
# College Cutoffs  (Pune / Maharashtra SPPU)
# ─────────────────────────────────────────────────────────────────────────────

CUTOFFS: Dict[str, Dict] = {
    "CSE": {
        "branch": "Computer Science & Engineering",
        "note": "MHT-CET percentile ranges (General/Open category, 2023-24). These change every year.",
        "colleges": [
            {"name": "COEP Technological University",          "location": "Pune",   "percentile": "99.5+",     "fees": "~₹1.2 L/yr", "tier": "Tier 1"},
            {"name": "PICT (Pune Institute of Computer Tech)", "location": "Pune",   "percentile": "99.0–99.5", "fees": "~₹1.5 L/yr", "tier": "Tier 1"},
            {"name": "MIT College of Engineering",             "location": "Pune",   "percentile": "98.5–99.2", "fees": "~₹1.8 L/yr", "tier": "Tier 1"},
            {"name": "VIT Pune",                               "location": "Pune",   "percentile": "97.5–99.0", "fees": "~₹1.6 L/yr", "tier": "Tier 1"},
            {"name": "PCCOE (Pimpri Chinchwad College)",       "location": "Pune",   "percentile": "96.0–98.0", "fees": "~₹1.3 L/yr", "tier": "Tier 2"},
            {"name": "Symbiosis Institute of Technology",      "location": "Pune",   "percentile": "95.0–97.5", "fees": "~₹2.5 L/yr", "tier": "Tier 2"},
            {"name": "Sinhgad College of Engineering",         "location": "Pune",   "percentile": "88.0–93.0", "fees": "~₹1.2 L/yr", "tier": "Tier 2"},
            {"name": "PVPIT Sangli",                           "location": "Sangli", "percentile": "90.0–95.0", "fees": "~₹1.0 L/yr", "tier": "Tier 2"},
            {"name": "GCOE Karad",                             "location": "Karad",  "percentile": "82.0–90.0", "fees": "~₹0.8 L/yr", "tier": "Tier 3"},
        ],
    },
    "CSE-AIML": {
        "branch": "CSE with AI & Machine Learning",
        "note": "Newer branch — typically 0.3–0.5 percentile lower than core CSE at same college.",
        "colleges": [
            {"name": "COEP Technological University",          "location": "Pune", "percentile": "99.2+",     "fees": "~₹1.2 L/yr", "tier": "Tier 1"},
            {"name": "PICT Pune (AI & ML)",                    "location": "Pune", "percentile": "98.0–99.0", "fees": "~₹1.6 L/yr", "tier": "Tier 1"},
            {"name": "MIT College of Engineering (AIML)",      "location": "Pune", "percentile": "98.0–99.0", "fees": "~₹1.9 L/yr", "tier": "Tier 1"},
            {"name": "VIT Pune (AI & Data Science)",           "location": "Pune", "percentile": "97.0–98.5", "fees": "~₹1.8 L/yr", "tier": "Tier 1"},
            {"name": "PCCOE Pune (AI & ML)",                   "location": "Pune", "percentile": "94.0–97.0", "fees": "~₹1.4 L/yr", "tier": "Tier 2"},
            {"name": "Symbiosis Institute of Technology",      "location": "Pune", "percentile": "94.0–97.0", "fees": "~₹2.8 L/yr", "tier": "Tier 2"},
            {"name": "Sinhgad College (AI & ML)",              "location": "Pune", "percentile": "86.0–92.0", "fees": "~₹1.3 L/yr", "tier": "Tier 3"},
        ],
    },
    "MECH": {
        "branch": "Mechanical Engineering",
        "note": "Cutoffs lower than CS branches. Government colleges are highly recommended for placement ROI.",
        "colleges": [
            {"name": "COEP Technological University",  "location": "Pune",   "percentile": "98.5+",     "fees": "~₹1.0 L/yr",  "tier": "Tier 1"},
            {"name": "MIT College of Engineering",     "location": "Pune",   "percentile": "93.0–97.0", "fees": "~₹1.7 L/yr",  "tier": "Tier 1"},
            {"name": "VIT Pune",                       "location": "Pune",   "percentile": "91.0–95.0", "fees": "~₹1.5 L/yr",  "tier": "Tier 1"},
            {"name": "Sinhgad College of Engineering", "location": "Pune",   "percentile": "82.0–90.0", "fees": "~₹1.1 L/yr",  "tier": "Tier 2"},
            {"name": "PVPIT Sangli",                   "location": "Sangli", "percentile": "78.0–88.0", "fees": "~₹0.9 L/yr",  "tier": "Tier 2"},
            {"name": "GCOE Karad",                     "location": "Karad",  "percentile": "72.0–84.0", "fees": "~₹0.75 L/yr", "tier": "Tier 3"},
            {"name": "DPCOE Pune",                     "location": "Pune",   "percentile": "70.0–82.0", "fees": "~₹1.0 L/yr",  "tier": "Tier 3"},
        ],
    },
    "ECE": {
        "branch": "Electronics & Communication Engineering",
        "note": "Strong VLSI + embedded scope. ISRO/DRDO paths available via GATE.",
        "colleges": [
            {"name": "COEP Technological University",  "location": "Pune",   "percentile": "98.8+",     "fees": "~₹1.1 L/yr",  "tier": "Tier 1"},
            {"name": "MIT College of Engineering",     "location": "Pune",   "percentile": "94.0–97.5", "fees": "~₹1.8 L/yr",  "tier": "Tier 1"},
            {"name": "VIT Pune",                       "location": "Pune",   "percentile": "92.0–96.0", "fees": "~₹1.6 L/yr",  "tier": "Tier 1"},
            {"name": "PCCOE Pune",                     "location": "Pune",   "percentile": "88.0–93.0", "fees": "~₹1.3 L/yr",  "tier": "Tier 2"},
            {"name": "Sinhgad College of Engineering", "location": "Pune",   "percentile": "82.0–90.0", "fees": "~₹1.2 L/yr",  "tier": "Tier 2"},
            {"name": "PVPIT Sangli",                   "location": "Sangli", "percentile": "76.0–86.0", "fees": "~₹0.9 L/yr",  "tier": "Tier 2"},
            {"name": "GCOE Karad",                     "location": "Karad",  "percentile": "70.0–82.0", "fees": "~₹0.75 L/yr", "tier": "Tier 3"},
        ],
    },
}

@app.get("/api/v1/cutoffs/{branch_code}")
def get_cutoffs(branch_code: str):
    code = branch_code.upper()
    data = CUTOFFS.get(code)
    if not data:
        raise HTTPException(404, f"Cutoff data for '{code}' not found")
    return data


# ─────────────────────────────────────────────────────────────────────────────
# Semester-wise Study Roadmap
# ─────────────────────────────────────────────────────────────────────────────

ROADMAPS: Dict[str, Dict] = {
    "CSE": {
        "title": "CSE — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Physics", "Basic Electronics", "C Programming", "Engineering Drawing"], "focus": "Build C programming habit. Solve 1 problem daily.", "tip": "C is the foundation of everything. Master pointers now."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Data Structures (C)", "Digital Logic Design", "OOP with Java", "Environmental Science"], "focus": "Data Structures is your most important subject. Start NOW.", "tip": "Code every DS from scratch — don't just read theory."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Discrete Mathematics", "Computer Organisation", "Operating Systems", "Database Management Systems", "Design Patterns"], "focus": "OS + DBMS form the backbone of all tech interviews.", "tip": "Practice SQL queries daily on HackerRank. Understand process scheduling deeply."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Theory of Computation", "Computer Networks", "Microprocessors", "Software Engineering", "Algorithms Analysis"], "focus": "Algorithms + Networks — critical for placements.", "tip": "Solve 200+ LeetCode problems. Study OSI model thoroughly."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Compiler Design", "Advanced Algorithms", "Web Technologies (HTML/CSS/JS)", "System Software", "Mini Project"], "focus": "Build your first full-stack web project.", "tip": "Get your first internship this summer — even 1 month matters a lot."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Machine Learning Intro", "Cloud Computing (AWS/Azure)", "Information Security", "Mobile App Development", "Internship"], "focus": "Internship is the #1 priority in Sem 6.", "tip": "Apply to 50+ companies for internship. Off-campus > waiting for on-campus."},
            {"sem": 7, "label": "Semester 7", "subjects": ["System Design", "DevOps & CI/CD", "Elective (Blockchain / IoT / AI)", "Major Project Phase 1", "Soft Skills"], "focus": "System Design separates SDE from senior SDE.", "tip": "Read 'Designing Data-Intensive Applications'. Practice on Excalidraw."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "Placement Preparation", "Open Source Contribution", "Final Exams"], "focus": "Crack placements. Target product companies over service companies.", "tip": "5 quality LeetCode mediums per day. Mock interviews on Pramp."},
        ],
        "parallel_tracks": [
            "🏆 Competitive Programming: Codeforces / LeetCode (start Sem 2)",
            "🌐 Web Dev: HTML → CSS → JS → React → Node.js (Sem 3–5)",
            "☁️ Cloud Cert: AWS Cloud Practitioner → AWS SAA (Sem 6–7)",
            "🔓 Open Source: Contribute to GitHub projects (Sem 5 onwards)",
        ],
    },
    "CSE-AIML": {
        "title": "CSE-AIML — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Physics", "Python Programming", "C Programming", "Statistics Basics"], "focus": "Python fluency is your #1 goal.", "tip": "Learn Python, NumPy, Matplotlib. Complete Kaggle's free Python course."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Linear Algebra", "Probability & Statistics", "Data Structures", "OOP with Python", "Calculus"], "focus": "Maths is as important as coding for AIML.", "tip": "3Blue1Brown's Linear Algebra videos are better than any textbook."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Database Systems", "Operating Systems", "Machine Learning Fundamentals", "Data Wrangling with Pandas", "Visualisation (Matplotlib/Seaborn)"], "focus": "Your first ML project — do Titanic Survival on Kaggle.", "tip": "Understand bias-variance tradeoff deeply. It comes up in every ML interview."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Deep Learning Fundamentals", "Neural Networks (CNNs, RNNs)", "Computer Networks", "Computer Vision Basics", "Statistics for ML"], "focus": "Build a CNN image classifier project.", "tip": "Fast.ai's Practical Deep Learning course is worth 10x any college lecture."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Natural Language Processing", "Reinforcement Learning", "Big Data (Spark/Hadoop)", "MLOps Introduction", "Mini Project"], "focus": "Build an NLP project + start reading research papers.", "tip": "Read 'Attention Is All You Need' — transformers are the foundation of modern AI."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Generative AI & LLMs", "Data Engineering (dbt/Airflow)", "Cloud ML (AWS SageMaker / GCP Vertex)", "Advanced Computer Vision", "Internship"], "focus": "ML Engineer internship is gold. Kaggle competitions help get interviews.", "tip": "A Kaggle competition medal opens interview doors at top companies."},
            {"sem": 7, "label": "Semester 7", "subjects": ["Production ML Systems", "Responsible AI & Fairness", "Elective (Graph Neural Nets / Federated Learning)", "Major Project Phase 1"], "focus": "Build an end-to-end ML pipeline: data → model → deployed API.", "tip": "MLflow + FastAPI + Docker = production ML portfolio that impresses."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "Placement Prep / MS Applications", "Research Paper Writing", "Final Exams"], "focus": "Placements or MS/PhD applications.", "tip": "For MS abroad: GRE + strong SOP + 1 research publication = strong application."},
        ],
        "parallel_tracks": [
            "📊 Kaggle: Competitions + notebook sharing (start Sem 3)",
            "🤗 Hugging Face: Fine-tune LLMs on custom datasets (Sem 6+)",
            "📝 Research: Read 1 ML paper per week from arXiv (from Sem 5)",
            "☁️ Cloud ML Cert: AWS ML Specialty / GCP Professional ML (Sem 7)",
        ],
    },
    "MECH": {
        "title": "Mechanical Engineering — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Engineering Physics", "Engineering Drawing & CAD", "Workshop Practice", "Basic Electrical Engineering"], "focus": "Engineering Drawing is critical — take it very seriously.", "tip": "AutoCAD basics in Sem 1 gives you a 2-year head start on your peers."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Engineering Mechanics (Statics & Dynamics)", "Manufacturing Processes I", "Thermodynamics I", "Material Science"], "focus": "Thermodynamics + Engineering Mechanics are your two pillars.", "tip": "Visualise force diagrams for every problem. Engineering Mechanics needs spatial thinking."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Fluid Mechanics", "Strength of Materials", "Theory of Machines I", "Thermodynamics II", "Metrology & Quality Control"], "focus": "Strength of Materials + Fluid Mechanics — hardest but most important semesters.", "tip": "Practice SOM problems daily. Draw Free Body Diagrams every single time."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Heat Transfer", "Machine Design I", "Theory of Machines II", "Manufacturing Processes II", "Industrial Engineering"], "focus": "Machine Design: learn to select materials and calculate dimensions.", "tip": "Practice SolidWorks alongside Machine Design — visualise what you design."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Refrigeration & Air Conditioning", "CAD/CAM & CNC Programming", "Finite Element Analysis (FEA)", "Control Systems", "Mini Project"], "focus": "FEA project in ANSYS — extremely valuable for core mechanical jobs.", "tip": "A simple FEA simulation (stress analysis on a bracket) impresses interviewers."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Robotics & Automation", "Power Plant Engineering", "Automobile Engineering", "Operations Research", "Industrial Internship"], "focus": "Core sector internship (auto/HVAC/manufacturing). Skip IT internships.", "tip": "L&T, Tata Motors, Cummins, Bosch internships are 10x more valuable for Mech."},
            {"sem": 7, "label": "Semester 7", "subjects": ["Advanced Manufacturing Technology", "Mechatronics & PLC", "Product Lifecycle Management", "MATLAB/Simulink", "Major Project Phase 1"], "focus": "Major project must have real design + FEA simulation.", "tip": "GATE preparation starts here if you want M.Tech or a PSU job."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "GATE Prep / Core Placements", "Elective (EV Technology / Additive Manufacturing)", "Final Exams"], "focus": "GATE score or core company placement. Both need focused effort.", "tip": "GATE Mechanical: Thermodynamics + SOM + Fluid Mechanics carry the most marks."},
        ],
        "parallel_tracks": [
            "🖥️ CAD: AutoCAD → SolidWorks → CATIA (Sem 1–4, get CSWA cert by Sem 5)",
            "⚙️ Simulation: ANSYS Mechanical (FEA) + ANSYS Fluent (CFD) (Sem 5–7)",
            "🤖 Automation: MATLAB + Arduino + PLC programming basics (Sem 5+)",
            "📋 Certifications: SolidWorks CSWA by Sem 5, Six Sigma Green Belt by Sem 7",
        ],
    },
    "ECE": {
        "title": "Electronics & Communication — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Physics (Semiconductors)", "Basic Electronics", "Programming in C", "Engineering Drawing"], "focus": "Understand how a transistor works — it's the atom of electronics.", "tip": "Build simple LED + resistor circuits on a breadboard. Hands-on from Day 1."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Analog Electronics", "Digital Electronics", "Signals & Systems", "Data Structures"], "focus": "Analog circuits + Digital logic — the absolute heart of ECE.", "tip": "Simulate circuits in LTSpice before building them physically. Saves components."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Electronic Devices & Circuits", "Digital Signal Processing", "Microprocessors (8085/8086)", "Communication Theory", "Electromagnetic Theory"], "focus": "DSP + Communication theory — tough but essential for core jobs.", "tip": "Z-transforms and Fourier analysis: solve 20 problems per chapter minimum."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Analog Communication Systems", "Digital Communication Systems", "VLSI Design I (Verilog/VHDL)", "Microcontrollers (8051/ARM/STM32)", "Control Systems"], "focus": "Start Verilog now — VLSI jobs require 1+ year of HDL experience.", "tip": "Program an Arduino/STM32 project. Hardware + code = your first portfolio piece."},
            {"sem": 5, "label": "Semester 5", "subjects": ["RF & Antenna Design", "Embedded Systems & RTOS", "VLSI Design II (Physical Design)", "Wireless Communication (4G/5G)", "Mini Project (IoT / FPGA)"], "focus": "Embedded Systems project on STM32 or FPGA.", "tip": "STM32 + sensors (temperature, IMU) + display = compelling embedded portfolio."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Satellite & Radar Communication", "PCB Design (KiCAD / Altium)", "Internet of Things Architecture", "Signal Processing Applications", "Internship (Embedded/VLSI/Telecom)"], "focus": "Embedded / VLSI / telecom internship is career-defining.", "tip": "Qualcomm, Texas Instruments, STMicro, ISRO internships — apply 5 months early."},
            {"sem": 7, "label": "Semester 7", "subjects": ["5G NR & Next-Gen Networks", "ML for Signal Processing (Edge AI)", "Low-Power IC Design", "Elective (Image Processing / Radar)", "Major Project Phase 1"], "focus": "Combine ML with ECE — Edge AI on microcontrollers is extremely hot.", "tip": "TensorFlow Lite on STM32 or Raspberry Pi = rare and impressive skill combo."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "Placement Preparation", "GATE Preparation (M.Tech VLSI)", "Final Exams"], "focus": "Core ECE placements or IT roles. GATE for M.Tech VLSI at IITs.", "tip": "For VLSI roles: Verilog + one FPGA project + Cadence Virtuoso basics = interview ready."},
        ],
        "parallel_tracks": [
            "⚡ Electronics Sim: LTSpice → Proteus → KiCAD PCB Design (Sem 2–6)",
            "🔧 Embedded: Arduino → STM32 → FreeRTOS (Sem 4–7)",
            "🖥️ FPGA/VLSI: Verilog on ModelSim / Xilinx Vivado (Sem 4–7)",
            "📡 Networking: Cisco CCNA / Jio 5G certification (Sem 7+)",
        ],
    },
}

@app.get("/api/v1/roadmap/{branch_code}")
def get_roadmap(branch_code: str):
    code = branch_code.upper()
    data = ROADMAPS.get(code)
    if not data:
        raise HTTPException(404, f"Roadmap for '{code}' not found")
    return data


# ─────────────────────────────────────────────────────────────────────────────
# Career Tree
# ─────────────────────────────────────────────────────────────────────────────

CAREER_TREES: Dict[str, Dict] = {
    "CSE": {
        "title": "CSE Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",    "skills": ["C / Java / Python basics", "DSA fundamentals", "Mathematics"],      "goal": "Build coding habit, solve easy DSA problems daily"},
            {"label": "Year 3",   "milestone": "Specialise",    "skills": ["OS, DBMS, Networks", "Web Dev / App Dev", "System Design intro"],    "goal": "Build 2 projects, get an internship"},
            {"label": "Year 4",   "milestone": "Placement",     "skills": ["Advanced DSA (LeetCode medium)", "System Design", "Open source"],    "goal": "Crack SDE interviews at product companies"},
            {"label": "0–3 Yrs",  "milestone": "Junior SDE",    "skills": ["Codebase contribution", "Code reviews", "Agile/Scrum"],              "goal": "SDE-1 (6–14 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior SDE",    "skills": ["System architecture", "Team leadership", "Cloud & DevOps"],          "goal": "SDE-2 / Senior Engineer (18–40 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Staff/Principal","skills": ["Cross-team impact", "Technical strategy", "Mentoring"],              "goal": "Staff Engineer / EM / Architect (50–120 LPA)"},
        ],
        "branches_out": ["🎓 MS Abroad → Research Scientist", "🏢 Technical Product Manager", "🚀 Startup Founder / CTO", "🛡️ Cybersecurity Specialist", "☁️ Cloud Architect"],
    },
    "CSE-AIML": {
        "title": "CSE-AIML Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",       "skills": ["Python + NumPy + Pandas", "Linear Algebra & Statistics", "DSA basics"],   "goal": "Kaggle beginner competitions, Python fluency"},
            {"label": "Year 3",   "milestone": "Specialise",       "skills": ["ML (Scikit-learn)", "Deep Learning (PyTorch)", "Data visualisation"],     "goal": "First ML project, Kaggle competition"},
            {"label": "Year 4",   "milestone": "Placement",        "skills": ["NLP / Computer Vision", "MLOps basics", "Research paper reading"],         "goal": "ML Engineer / Data Scientist internship"},
            {"label": "0–3 Yrs",  "milestone": "Junior ML Eng",    "skills": ["Model training pipeline", "Feature engineering", "A/B testing"],           "goal": "ML Engineer / Junior Data Scientist (8–18 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior ML Eng",    "skills": ["MLOps & model serving", "Large-scale pipelines", "Research"],               "goal": "Senior ML Eng / Staff Data Scientist (20–45 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Principal/Research","skills": ["Foundation model training", "AI strategy", "Leadership"],                  "goal": "Research Scientist / AI Lead (60–150 LPA)"},
        ],
        "branches_out": ["🎓 PhD AI/ML → Research Scientist at DeepMind", "🚀 AI Startup Founder", "📊 Head of Data Science", "🤖 Generative AI Engineer", "💡 AI Product Manager"],
    },
    "MECH": {
        "title": "Mechanical Engineering Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",    "skills": ["Engineering Drawing & CAD", "Mechanics & Thermodynamics", "Workshop skills"], "goal": "AutoCAD / SolidWorks basics"},
            {"label": "Year 3",   "milestone": "Specialise",    "skills": ["FEA (ANSYS)", "Manufacturing processes", "MATLAB simulation"],                "goal": "Core sector internship"},
            {"label": "Year 4",   "milestone": "Placement",     "skills": ["SolidWorks / CATIA proficiency", "GATE preparation", "Industry project"],      "goal": "Core job or GATE rank for M.Tech / PSU"},
            {"label": "0–3 Yrs",  "milestone": "GET",           "skills": ["Design software", "Manufacturing standards", "Project execution"],             "goal": "Graduate Engineer Trainee (4–9 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior Eng",    "skills": ["PLM", "Cross-functional lead", "Cost optimisation"],                           "goal": "Senior Engineer / Deputy Manager (12–22 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Manager",       "skills": ["Program management", "Vendor management", "Innovation leadership"],            "goal": "Engineering Manager / Chief Engineer (25–55 LPA)"},
        ],
        "branches_out": ["🎓 M.Tech / MS → Research & Academia", "🏭 Operations / Plant Manager", "🚗 EV Startup", "🛰️ ISRO / DRDO / HAL", "📦 Supply Chain Consulting"],
    },
    "ECE": {
        "title": "Electronics & Communication Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",    "skills": ["Circuit Theory", "Signals & Systems", "Embedded C / Arduino"],                         "goal": "Build circuits, understand analog + digital"},
            {"label": "Year 3",   "milestone": "Specialise",    "skills": ["VLSI / Verilog", "PCB Design", "Communication protocols (SPI/I2C/UART)"],              "goal": "Embedded / VLSI internship, PCB project"},
            {"label": "Year 4",   "milestone": "Placement",     "skills": ["FPGA development", "IoT project portfolio", "GATE prep"],                               "goal": "Core ECE placement or IT sector role"},
            {"label": "0–3 Yrs",  "milestone": "Junior Eng",    "skills": ["Firmware development", "RTOS", "Hardware debugging"],                                   "goal": "Embedded / VLSI Engineer (5–11 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior Hw Eng", "skills": ["SoC design", "RF / mm-wave design", "Silicon validation"],                              "goal": "Senior Engineer at Qualcomm / Intel (14–28 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Principal",     "skills": ["Chip architecture", "Cross-domain leadership", "IP development"],                       "goal": "Principal Engineer / Chip Architect (30–70 LPA)"},
        ],
        "branches_out": ["🎓 M.Tech VLSI / Signal Processing", "🛰️ ISRO / DRDO Space & Defence", "📡 5G Telecom Network Engineer", "💻 IT/Software roles", "🏭 IoT Startup Founder"],
    },
}

@app.get("/api/v1/career-tree/{branch_code}")
def get_career_tree(branch_code: str):
    code = branch_code.upper()
    tree = CAREER_TREES.get(code)
    if not tree:
        raise HTTPException(404, f"Career tree for '{code}' not found")
    return tree


# ─────────────────────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

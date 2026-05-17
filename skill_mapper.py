"""
Skill Mapper — Career Intelligence Engine
10 questions → skill scores → branch recommendations
Question order: q4 → q5 → q8 → q7 → q2 → q3 → q1 → q6 → q10 → q9
(Broad interest first, then specific skills, then career goals last)
"""

from typing import Dict, List, Any
from datetime import datetime


# ---------------------------------------------------------------------------
# Question definitions  (IDs preserved — only display ORDER changed)
# ---------------------------------------------------------------------------

_Q = {}   # keyed by id for easy lookup

_Q["q1"] = {
    "id": "q1",
    "question": "How comfortable are you with writing code / programming?",
    "type": "scale",
    "min": 1, "max": 10,
    "hint": "1 = Never tried  |  5 = Know basics  |  10 = Build projects independently",
    "maps": {"coding": 1.0}
}

_Q["q2"] = {
    "id": "q2",
    "question": "How much do you enjoy Mathematics (calculus, algebra, probability)?",
    "type": "scale",
    "min": 1, "max": 10,
    "hint": "1 = I avoid it  |  10 = I genuinely enjoy solving maths",
    "maps": {"mathematics": 1.0}
}

_Q["q3"] = {
    "id": "q3",
    "question": "How comfortable are you with electronics — circuits, breadboards, soldering?",
    "type": "scale",
    "min": 1, "max": 10,
    "hint": "1 = No experience  |  10 = I build circuits from scratch",
    "maps": {"hardware": 1.0}
}

_Q["q4"] = {
    "id": "q4",
    "question": "Which of these activities excites you the most?",
    "type": "choice",
    "hint": "Pick the one that genuinely interests you — there is no wrong answer",
    "options": [
        {"value": "software",  "text": "💻  Building apps, websites, or games",
         "maps": {"coding": 3, "analytical": 1}},
        {"value": "aiml",      "text": "🤖  Training AI models, analysing data patterns",
         "maps": {"coding": 2, "mathematics": 2, "analytical": 2, "research": 1}},
        {"value": "machines",  "text": "⚙️  Designing mechanical systems, engines, robots",
         "maps": {"hardware": 2, "creativity": 2, "mathematics": 1}},
        {"value": "circuits",  "text": "🔌  Designing circuits, embedded systems, IoT devices",
         "maps": {"hardware": 3, "coding": 1, "mathematics": 1}},
    ]
}

_Q["q5"] = {
    "id": "q5",
    "question": "Which subject did you enjoy the most in 11th / 12th standard?",
    "type": "choice",
    "hint": "The one you actually looked forward to studying",
    "options": [
        {"value": "cs",      "text": "💻  Computer Science / IT",
         "maps": {"coding": 3, "analytical": 1}},
        {"value": "maths",   "text": "📐  Mathematics / Statistics",
         "maps": {"mathematics": 3, "analytical": 2}},
        {"value": "physics", "text": "⚡  Physics (especially electronics / electromagnetism)",
         "maps": {"hardware": 2, "mathematics": 1, "analytical": 1}},
        {"value": "design",  "text": "🎨  Design / Engineering Drawing / Workshop",
         "maps": {"creativity": 3, "hardware": 1}},
    ]
}

_Q["q6"] = {
    "id": "q6",
    "question": "Are you interested in research, data analysis, and finding patterns in large datasets?",
    "type": "choice",
    "hint": "Think: do numbers and hidden patterns genuinely excite you?",
    "options": [
        {"value": "yes",   "text": "Yes — I love finding patterns in data",
         "maps": {"research": 3, "analytical": 2, "mathematics": 1}},
        {"value": "maybe", "text": "Somewhat — I can do it but it's not my passion",
         "maps": {"research": 1, "analytical": 1}},
        {"value": "no",    "text": "Not really — I prefer building or designing physical things",
         "maps": {"creativity": 1, "hardware": 1}},
    ]
}

_Q["q7"] = {
    "id": "q7",
    "question": "Do you prefer working on physical / hardware products or purely software?",
    "type": "choice",
    "hint": "No right or wrong — just your honest gut preference",
    "options": [
        {"value": "software",  "text": "Purely software — I'm a screen + keyboard person",
         "maps": {"coding": 2}},
        {"value": "hardware",  "text": "Physical hardware — I like making real, tangible things",
         "maps": {"hardware": 2, "creativity": 1}},
        {"value": "both",      "text": "Both — embedded systems / mechatronics sounds cool",
         "maps": {"hardware": 1, "coding": 1, "creativity": 1}},
    ]
}

_Q["q8"] = {
    "id": "q8",
    "question": "How strong is your logical / analytical problem-solving ability?",
    "type": "scale",
    "min": 1, "max": 10,
    "hint": "Think: puzzles, Sudoku, maths Olympiad, debugging code — how natural does this feel?",
    "maps": {"analytical": 1.0}
}

_Q["q9"] = {
    "id": "q9",
    "question": "After B.E., would you prefer higher studies (M.Tech / MS / PhD) or going straight to industry?",
    "type": "choice",
    "hint": "Honest answer — both are great paths, no judgement",
    "options": [
        {"value": "research",  "text": "Higher studies / research — I want to go deep into a field",
         "maps": {"research": 3}},
        {"value": "industry",  "text": "Industry right away — I want to build things and earn",
         "maps": {"coding": 1, "entrepreneurship": 1}},
        {"value": "startup",   "text": "Start my own company or build my own product",
         "maps": {"entrepreneurship": 3, "creativity": 2}},
        {"value": "unsure",    "text": "Not sure yet — keeping all options open",
         "maps": {"research": 1}},
    ]
}

_Q["q10"] = {
    "id": "q10",
    "question": "What is your primary goal for choosing an engineering branch?",
    "type": "choice",
    "hint": "Be honest — all goals are completely valid",
    "options": [
        {"value": "salary",   "text": "💰  Highest salary & long-term job security",
         "maps": {"coding": 1, "analytical": 1}},
        {"value": "passion",  "text": "❤️  Do work I am genuinely passionate about every day",
         "maps": {"creativity": 1, "research": 1}},
        {"value": "impact",   "text": "🌍  Create real-world impact and solve big problems",
         "maps": {"research": 1, "entrepreneurship": 1}},
        {"value": "abroad",   "text": "✈️  MS / PhD abroad and build a global career",
         "maps": {"research": 2, "mathematics": 1}},
    ]
}

# ---------------------------------------------------------------------------
# QUESTION ORDER  ← change here to reorder without touching definitions
# ---------------------------------------------------------------------------
QUESTIONS: List[Dict] = [
    _Q["q4"],   # 1. What excites you most?  (broad interest — best opener)
    _Q["q5"],   # 2. Favourite 12th subject?  (school background)
    _Q["q8"],   # 3. Analytical ability?      (logical scale)
    _Q["q7"],   # 4. Hardware or software?    (type preference)
    _Q["q2"],   # 5. Enjoy maths?             (maths scale)
    _Q["q3"],   # 6. Electronics comfort?     (hardware scale)
    _Q["q1"],   # 7. Coding comfort?          (coding scale)
    _Q["q6"],   # 8. Research / data interest? (research aptitude)
    _Q["q10"],  # 9. Primary career goal?     (motivation)
    _Q["q9"],   # 10. Higher studies or industry? (future path — natural closer)
]


# ---------------------------------------------------------------------------
# Branch profiles  (skill dimension → weight 0–1)
# ---------------------------------------------------------------------------

BRANCH_PROFILES = {
    "CSE": {
        "coding": 0.95, "mathematics": 0.70, "analytical": 0.85,
        "hardware": 0.20, "creativity": 0.60, "research": 0.50,
        "communication": 0.55, "entrepreneurship": 0.60
    },
    "CSE-AIML": {
        "coding": 0.90, "mathematics": 0.92, "analytical": 0.95,
        "hardware": 0.15, "creativity": 0.65, "research": 0.80,
        "communication": 0.55, "entrepreneurship": 0.55
    },
    "MECH": {
        "coding": 0.40, "mathematics": 0.80, "analytical": 0.75,
        "hardware": 0.85, "creativity": 0.80, "research": 0.55,
        "communication": 0.60, "entrepreneurship": 0.55
    },
    "ECE": {
        "coding": 0.65, "mathematics": 0.80, "analytical": 0.80,
        "hardware": 0.95, "creativity": 0.55, "research": 0.60,
        "communication": 0.55, "entrepreneurship": 0.45
    }
}

BRANCH_NAMES = {
    "CSE":      "Computer Science & Engineering",
    "CSE-AIML": "CSE with AI & Machine Learning",
    "MECH":     "Mechanical Engineering",
    "ECE":      "Electronics & Communication Engineering"
}


# ---------------------------------------------------------------------------
# SkillMapper
# ---------------------------------------------------------------------------

class SkillMapper:
    def get_questions(self) -> List[Dict]:
        return QUESTIONS

    def calculate_scores(self, answers: Dict[str, Any]) -> Dict[str, float]:
        scores = {
            "coding": 0.0, "mathematics": 0.0, "analytical": 0.0,
            "hardware": 0.0, "creativity": 0.0, "research": 0.0,
            "communication": 0.0, "entrepreneurship": 0.0
        }
        for q in QUESTIONS:
            qid    = q["id"]
            answer = answers.get(qid)
            if answer is None:
                continue
            if q["type"] == "scale":
                val = float(answer)
                for dim, weight in q["maps"].items():
                    scores[dim] += val * weight
            elif q["type"] == "choice":
                for opt in q["options"]:
                    if opt["value"] == answer:
                        for dim, pts in opt["maps"].items():
                            scores[dim] += pts
                        break
        for dim in scores:
            scores[dim] = round(min(10.0, max(0.0, scores[dim])), 2)
        return scores

    def rank_branches(self, scores: Dict[str, float]) -> List[Dict]:
        results = []
        for code, weights in BRANCH_PROFILES.items():
            total = sum(scores.get(d, 0.0) * w for d, w in weights.items())
            max_p = sum(10.0 * w for w in weights.values())
            pct   = round(total / max_p * 100, 1) if max_p else 0
            results.append({
                "code":        code,
                "name":        BRANCH_NAMES[code],
                "match_pct":   pct,
                "explanation": self._explain(code, scores, pct)
            })
        results.sort(key=lambda x: x["match_pct"], reverse=True)
        return results

    def _explain(self, code: str, scores: Dict[str, float], pct: float) -> str:
        weights   = BRANCH_PROFILES[code]
        top_dims  = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:2]
        strengths = [d for d, w in top_dims if scores.get(d, 0) >= 6]
        label     = ("Excellent" if pct >= 75 else "Good" if pct >= 60
                     else "Moderate" if pct >= 45 else "Low")
        text = f"{label} match ({pct:.1f}%). "
        if strengths:
            text += f"Your strength in {' & '.join(d.replace('_',' ') for d in strengths)} aligns well. "
        else:
            text += "Building core skills in this area will be important. "
        advice = {
            "CSE":      "Focus on DSA and system design to excel.",
            "CSE-AIML": "Strong maths + Python are your keys to success.",
            "MECH":     "CAD skills and core sector internships help a lot.",
            "ECE":      "Hands-on embedded labs and FPGA projects set you apart."
        }
        text += advice.get(code, "")
        return text


# ---------------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------------

def run_assessment(answers: Dict[str, Any]) -> Dict[str, Any]:
    mapper       = SkillMapper()
    skill_scores = mapper.calculate_scores(answers)
    ranked       = mapper.rank_branches(skill_scores)
    confidence   = min(1.0, ranked[0]["match_pct"] / 100 + 0.05) if ranked else 0.5
    return {
        "skill_scores":         skill_scores,
        "recommended_branches": ranked,
        "confidence":           round(confidence, 3),
        "timestamp":            datetime.now().isoformat()
    }


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Question order:")
    for i, q in enumerate(QUESTIONS, 1):
        print(f"  {i}. [{q['id']}] {q['question'][:60]}...")

    sample = {
        "q4": "aiml", "q5": "maths", "q8": 9, "q7": "software",
        "q2": 8,      "q3": 2,       "q1": 8, "q6": "yes",
        "q10": "abroad", "q9": "research"
    }
    result = run_assessment(sample)
    print("\nRecommendations:")
    for b in result["recommended_branches"]:
        print(f"  {b['code']:12} {b['match_pct']:5.1f}%")

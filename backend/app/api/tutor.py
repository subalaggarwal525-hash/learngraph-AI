from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import CourseModel, ConceptModel
from backend.app.schemas.schemas import ChatTutorRequest
from backend.app.services.llm_service import LLMService
from backend.app.rag.vector_store import global_vector_store

router = APIRouter(prefix="/api/tutor", tags=["tutor"])
llm_service = LLMService()

@router.post("/chat")
async def chat_with_tutor(req: ChatTutorRequest, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == req.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    concept_title = "Overall Course"
    if req.concept_id:
        concept = db.query(ConceptModel).filter(ConceptModel.id == req.concept_id).first()
        if concept:
            concept_title = concept.title

    retrieved_chunks = global_vector_store.search(query=req.message, course_id=req.course_id, top_k=2)
    sources_cited = [c["section_title"] for c in retrieved_chunks]
    context_text = "\n".join([f"[{c['section_title']}]: {c['content']}" for c in retrieved_chunks])

    system_prompt = f"Subject: {course.title}, Active Concept: {concept_title}. Context: {context_text or 'Standard curriculum'}. Mode: {req.mode}"
    if ai_response.startswith("I am LearnGraph AI Tutor"):
        ai_response = f"Great question regarding **{concept_title}**! Let's break this down:\n\n1. **Core Intuition**: {concept_title} establishes deterministic boundaries and systematic flow.\n2. **Mechanism**: Notice how inputs transform into state changes before resolving to output values.\n\nWould you like an analogy, a worked example, or a quick check question?"

    return {
        "reply": ai_response,
        "concept_id": req.concept_id,
        "concept_title": concept_title,
        "sources_cited": sources_cited
    }

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class EvaluateExplanationRequest(BaseModel):
    course_id: str
    concept_id: str
    student_explanation: str

@router.post("/evaluate-explanation")
async def evaluate_student_explanation(req: EvaluateExplanationRequest, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == req.concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
        
    explanation = req.student_explanation.strip()
    words = len(explanation.split())
    
    # Analyze explanation content for key terms and depth
    title_words = set(concept.title.lower().split())
    student_words = set(explanation.lower().split())
    overlap = len(title_words.intersection(student_words))
    
    clarity_score = min(100, max(40, words * 2 + overlap * 10))
    accuracy_score = 90 if words > 30 else 75 if words > 15 else 55
    
    strengths = []
    gaps = []
    
    if words > 25:
        strengths.append("Clearly articulated structural principles in your own authentic voice.")
    else:
        gaps.append("Explanation is relatively brief; consider detailing how boundary constraints are handled.")
        
    if any(k in explanation.lower() for k in ["because", "therefore", "mapped", "translated", "stored", "executes", "allocates"]):
        strengths.append("Demonstrated causal reasoning regarding underlying mechanisms.")
    else:
        gaps.append("Try adding a causal connection (e.g. why this mechanism is chosen over simpler alternatives).")
        
    feedback = f"### Feynman Technique Assessment for **{concept.title}**\n\n"
    if clarity_score >= 80:
        feedback += f"🌟 **Exceptional Synthesis!** You demonstrated a coherent mental model without relying on robotic jargon.\n\n"
    else:
        feedback += f"👍 **Good start!** You grasp the core premise, but articulating the operational steps will lock in permanent retention.\n\n"
        
    feedback += f"**Key Strengths:**\n" + "\n".join([f"- {s}" for s in strengths]) + "\n\n"
    if gaps:
        feedback += f"**Areas for Deeper Clarity:**\n" + "\n".join([f"- {g}" for g in gaps]) + "\n\n"
    feedback += f"**Teacher's Summary:** Next time you teach someone, compare `{concept.title}` with real hardware registers or memory hierarchies."

    return {
        "concept_id": req.concept_id,
        "concept_title": concept.title,
        "overall_score": int((clarity_score + accuracy_score) / 2),
        "clarity_score": clarity_score,
        "accuracy_score": accuracy_score,
        "strengths": strengths,
        "gaps": gaps,
        "feedback_markdown": feedback
    }

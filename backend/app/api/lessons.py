from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import ConceptModel
from backend.app.schemas.schemas import GenerateLessonRequest, TeachingModeEnum
from backend.app.services.llm_service import LLMService
from backend.app.agents.lesson_generator import LessonGeneratorAgent
from backend.app.rag.vector_store import global_vector_store

router = APIRouter(prefix="/api/lessons", tags=["lessons"])
llm_service = LLMService()
lesson_agent = LessonGeneratorAgent(llm_service)

@router.post("/{concept_id}/generate")
async def generate_lesson(concept_id: str, req: GenerateLessonRequest = GenerateLessonRequest(), db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    retrieved_chunks = global_vector_store.search(query=concept.title, course_id=concept.course_id, top_k=2)
    context_str = "\n".join([f"[{c['section_title']}]: {c['content']}" for c in retrieved_chunks]) if retrieved_chunks else None

    concept_dict = {
        "id": concept.id,
        "title": concept.title,
        "prerequisites": concept.prerequisites or [],
        "learning_objectives": concept.learning_objectives or [],
        "common_misconceptions": concept.common_misconceptions or []
    }
    mode = req.mode or TeachingModeEnum.SIMPLE
    return await lesson_agent.generate_lesson(concept_dict, mode, context_str)

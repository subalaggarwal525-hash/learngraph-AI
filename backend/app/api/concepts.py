from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import ConceptModel

router = APIRouter(prefix="/api/concepts", tags=["concepts"])

@router.get("/{concept_id}")
def get_concept(concept_id: str, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return {
        "id": concept.id,
        "course_id": concept.course_id,
        "title": concept.title,
        "short_summary": concept.short_summary,
        "difficulty": concept.difficulty,
        "importance": concept.importance,
        "estimated_minutes": concept.estimated_minutes,
        "status": concept.status,
        "mastery_score": concept.mastery_score,
        "prerequisites": concept.prerequisites or [],
        "learning_objectives": concept.learning_objectives or [],
        "common_misconceptions": concept.common_misconceptions or []
    }

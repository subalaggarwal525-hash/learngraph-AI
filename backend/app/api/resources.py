from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.database.connection import get_db
from backend.app.database.models import ConceptModel
from backend.app.youtube.analyzer import YouTubeAnalyzer

router = APIRouter(prefix="/api/resources", tags=["resources"])

@router.get("/{concept_id}", response_model=List[Dict[str, Any]])
def get_curated_resources(concept_id: str, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    title = concept.title
    encoded_query = "+".join(title.split())
    coverage_info = YouTubeAnalyzer.analyze_coverage(f"https://www.youtube.com/results?search_query={encoded_query}", title, concept.learning_objectives or [])
    
    return [
        {
            "id": f"res_vid_1_{concept_id}",
            "title": f"MIT OpenCourseWare: Foundations of {title}",
            "url": f"https://www.youtube.com/results?search_query=MIT+OpenCourseWare+{encoded_query}",
            "type": "video",
            "duration_or_read_time": "24 mins",
            "difficulty": "Rigorous / Academic",
            "relevance_score": 98,
            "covered_topics": coverage_info["covered_topics"],
            "missing_topics": coverage_info["missing_topics"],
            "coverage_percentage": coverage_info["coverage_percentage"]
        },
        {
            "id": f"res_doc_1_{concept_id}",
            "title": f"Computer Systems Reference & Architecture Notes: {title}",
            "url": f"https://en.wikipedia.org/wiki/{'_'.join(title.split())}",
            "type": "document",
            "duration_or_read_time": "12 mins read",
            "difficulty": "Reference",
            "relevance_score": 94,
            "covered_topics": [title, "Hardware Constraints", "Performance Invariants"],
            "missing_topics": [],
            "coverage_percentage": 95
        },
        {
            "id": f"res_practice_1_{concept_id}",
            "title": f"Interactive Sandbox & Practice Lab: {title}",
            "url": "#simulation",
            "type": "practice",
            "duration_or_read_time": "15 mins active",
            "difficulty": "Applied",
            "relevance_score": 99,
            "covered_topics": ["Hands-on state transitions", "Edge case debugging"],
            "missing_topics": [],
            "coverage_percentage": 100
        }
    ]

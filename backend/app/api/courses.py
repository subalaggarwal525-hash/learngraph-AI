from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.database.connection import get_db
from backend.app.database.models import CourseModel, ConceptModel, UserModel
from backend.app.schemas.schemas import CreateCourseRequest
from backend.app.services.llm_service import LLMService
from backend.app.agents.graph import LearnGraphOrchestrator
from backend.app.agents.adaptive_controller import AdaptiveController

router = APIRouter(prefix="/api/courses", tags=["courses"])
llm_service = LLMService()
orchestrator = LearnGraphOrchestrator(llm_service)

@router.post("", response_model=Dict[str, Any])
async def create_course(req: CreateCourseRequest, db: Session = Depends(get_db)):
    title = req.title or (req.source_content[:40] if len(req.source_content) > 3 else "New Learning Journey")
    initial_state = {
        "course_id": "temp",
        "source_type": req.source_type,
        "source_content": req.source_content,
        "learning_goal": req.learning_goal.value,
        "current_level": req.current_level.value,
        "study_time_hours": req.study_time_hours_per_week or 5,
        "preferred_style": req.preferred_style.value if req.preferred_style else "simple",
        "topic": "",
        "scope": "",
        "concepts": [],
        "prerequisites_map": {},
        "knowledge_graph": {},
        "roadmap": {},
        "active_concept_id": None,
        "current_lesson": None,
        "current_quiz": None,
        "quiz_submission": None,
        "evaluation_result": None,
        "remediation_required": False,
        "weak_prerequisite_id": None,
        "next_recommended_concept_id": None,
        "learner_mastery_updates": {}
    }

    result_state = await orchestrator.run_initial_course_pipeline(initial_state)

    db_course = CourseModel(
        title=result_state["topic"] or title,
        source_type=req.source_type,
        source_content=req.source_content,
        source_summary=result_state["scope"],
        learning_goal=req.learning_goal.value,
        current_level=req.current_level.value,
        study_time_hours_per_week=req.study_time_hours_per_week or 5,
        preferred_style=req.preferred_style.value if req.preferred_style else "simple",
        knowledge_graph_data=result_state["knowledge_graph"],
        roadmap_data=result_state["roadmap"],
        user_id=req.user_id or "demo_user"
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    for c in result_state["concepts"]:
        cid = f"{db_course.id[:8]}_{c['id']}"
        c["id"] = cid
        db_concept = ConceptModel(
            id=cid,
            course_id=db_course.id,
            title=c["title"],
            short_summary=c.get("short_summary", ""),
            difficulty=c.get("difficulty", 2),
            importance=c.get("importance", 4),
            estimated_minutes=c.get("estimated_minutes", 20),
            status=c.get("status", "locked"),
            mastery_score=c.get("mastery_score", 0.0),
            prerequisites=[f"{db_course.id[:8]}_{p}" for p in c.get("prerequisites", [])],
            learning_objectives=c.get("learning_objectives", []),
            common_misconceptions=c.get("common_misconceptions", []),
            source_references=c.get("source_references", [])
        )
        db.add(db_concept)
    db.commit()

    return {
        "id": db_course.id,
        "title": db_course.title,
        "source_summary": db_course.source_summary,
        "knowledge_graph": result_state["knowledge_graph"],
        "roadmap": result_state["roadmap"],
        "concepts_count": len(result_state["concepts"])
    }

@router.get("", response_model=List[Dict[str, Any]])
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(CourseModel).order_by(CourseModel.created_at.desc()).all()
    results = []
    for c in courses:
        roadmap = c.roadmap_data or {}
        results.append({
            "id": c.id,
            "title": c.title,
            "source_type": c.source_type,
            "learning_goal": c.learning_goal,
            "progress_percentage": roadmap.get("progress_percentage", 0.0),
            "total_concepts": len(c.concepts),
            "created_at": c.created_at.strftime("%b %d, %Y")
        })
    return results

@router.get("/{course_id}")
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    concepts_data = [
        {
            "id": c.id,
            "title": c.title,
            "short_summary": c.short_summary,
            "difficulty": c.difficulty,
            "importance": c.importance,
            "estimated_minutes": c.estimated_minutes,
            "status": c.status,
            "mastery_score": c.mastery_score,
            "prerequisites": c.prerequisites or [],
            "learning_objectives": c.learning_objectives or [],
            "common_misconceptions": c.common_misconceptions or []
        }
        for c in course.concepts
    ]

    revision_schedule = AdaptiveController.compute_spaced_repetition_schedule(concepts_data)
    mastered = sum(1 for c in concepts_data if c["status"] == "mastered")
    total = len(concepts_data)

    mastery_profile = {
        "overall_mastery": round((mastered / total) * 100.0, 1) if total > 0 else 0.0,
        "concepts_mastered": mastered,
        "concepts_in_progress": sum(1 for c in concepts_data if c["status"] == "learning"),
        "concepts_locked": sum(1 for c in concepts_data if c["status"] == "locked"),
        "total_concepts": total,
        "concept_scores": {c["id"]: c["mastery_score"] for c in concepts_data},
        "strongest_concepts": [c["title"] for c in concepts_data if c["mastery_score"] >= 80.0],
        "weakest_concepts": [c["title"] for c in concepts_data if c["status"] == "needs_review" or (c["mastery_score"] < 60 and c["mastery_score"] > 0)],
        "recent_accuracy": 88.5,
        "streak_days": 4,
        "total_xp": 450,
        "level": 2
    }

    return {
        "id": course.id,
        "title": course.title,
        "source_type": course.source_type,
        "source_summary": course.source_summary,
        "learning_goal": course.learning_goal,
        "current_level": course.current_level,
        "created_at": course.created_at.strftime("%b %d, %Y"),
        "concepts": concepts_data,
        "knowledge_graph": course.knowledge_graph_data,
        "roadmap": course.roadmap_data,
        "mastery_profile": mastery_profile,
        "revision_schedule": revision_schedule
    }

@router.get("/{course_id}/roadmap")
def get_roadmap(course_id: str, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.roadmap_data

@router.post("/{course_id}/final-test")
def generate_final_test(course_id: str, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    final_questions = []
    for idx, c in enumerate(course.concepts):
        final_questions.append({
            "id": f"final_q_{idx+1}",
            "type": "scenario",
            "prompt": f"Comprehensive Synthesis [{c.title}]: A system engineer reports high latency during peak hours. How does the architecture of {c.title} resolve or mitigate this failure mode?",
            "options": [
                f"Apply optimized caching, proper resource partitioning, and verify state boundaries of {c.title}",
                "Terminate the entire server instance and restart from cold boot",
                "Disable all security checks and memory limits completely",
                "None of the above"
            ],
            "correct_answer": 0,
            "explanation": f"Optimal engineering demands applying the core mechanisms of {c.title}.",
            "concept_id": c.id,
            "difficulty": 4
        })

    return {
        "id": f"final_test_{course_id}",
        "course_id": course_id,
        "course_title": course.title,
        "total_questions": len(final_questions),
        "pass_threshold": 80.0,
        "questions": final_questions
    }

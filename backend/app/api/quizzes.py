from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import ConceptModel, CourseModel, UserModel, QuizModel, QuizAttemptModel
from backend.app.schemas.schemas import SubmitQuizRequest
from backend.app.agents.quiz_evaluator import QuizEvaluatorAgent
from backend.app.agents.adaptive_controller import AdaptiveController
from datetime import datetime

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])

@router.get("/{concept_id}")
def get_quiz_for_concept(concept_id: str, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return QuizEvaluatorAgent.generate_quiz_for_concept({
        "id": concept.id,
        "title": concept.title,
        "prerequisites": concept.prerequisites or [],
        "learning_objectives": concept.learning_objectives or [],
        "common_misconceptions": concept.common_misconceptions or []
    })

@router.post("/{concept_id}/submit")
def submit_quiz(concept_id: str, req: SubmitQuizRequest, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    course = db.query(CourseModel).filter(CourseModel.id == concept.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    concept_dict = {
        "id": concept.id,
        "title": concept.title,
        "prerequisites": concept.prerequisites or [],
        "mastery_score": concept.mastery_score,
        "learning_objectives": concept.learning_objectives or [],
        "common_misconceptions": concept.common_misconceptions or []
    }
    quiz_data = QuizEvaluatorAgent.generate_quiz_for_concept(concept_dict)
    evaluation_result = QuizEvaluatorAgent.evaluate_quiz_submission(quiz_data, req.answers, concept_dict)

    adaptation = AdaptiveController.update_graph_after_evaluation(
        knowledge_graph=course.knowledge_graph_data or {},
        roadmap=course.roadmap_data or {},
        concept_id=concept_id,
        evaluation_result=evaluation_result
    )

    concept.mastery_score = evaluation_result["updated_mastery"]
    concept.status = "mastered" if evaluation_result["passed"] else "needs_review"
    concept.last_studied = datetime.utcnow()

    for node in adaptation["knowledge_graph"].get("nodes", []):
        db_c = db.query(ConceptModel).filter(ConceptModel.id == node["id"]).first()
        if db_c:
            db_c.status = node["data"]["status"]
            db_c.mastery_score = node["data"]["mastery_score"]

    course.knowledge_graph_data = adaptation["knowledge_graph"]
    course.roadmap_data = adaptation["roadmap"]

    # Persist quiz record and attempt history
    db_quiz = db.query(QuizModel).filter(QuizModel.concept_id == concept.id).first()
    if not db_quiz:
        db_quiz = QuizModel(concept_id=concept.id, questions_json=quiz_data.get("questions", []))
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)

    attempt = QuizAttemptModel(
        quiz_id=db_quiz.id,
        user_id="demo_user",
        score=evaluation_result["total_score"],
        passed=evaluation_result["passed"],
        answers_json=req.answers,
        evaluation_json=evaluation_result
    )
    db.add(attempt)

    user = db.query(UserModel).filter(UserModel.id == "demo_user").first()
    if user:
        user.xp += evaluation_result.get("xp_earned", 50)
        user.level = max(1, user.xp // 250 + 1)
        user.last_active_at = datetime.utcnow()
    db.commit()

    return {
        "evaluation": evaluation_result,
        "updated_knowledge_graph": course.knowledge_graph_data,
        "updated_roadmap": course.roadmap_data
    }

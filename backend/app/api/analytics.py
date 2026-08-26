from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import CourseModel, UserModel, ConceptModel, QuizAttemptModel
from backend.app.agents.adaptive_controller import AdaptiveController
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard")
def get_user_dashboard(user_id: str = "demo_user", db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        user = UserModel(id="demo_user", name="Alex Learner", xp=450, level=2, streak_days=4)
        db.add(user)
        db.commit()
        db.refresh(user)

    courses = db.query(CourseModel).filter(CourseModel.user_id == user_id).all()
    all_concepts = db.query(ConceptModel).all()
    all_attempts = db.query(QuizAttemptModel).all()

    total_concepts = len(all_concepts)
    mastered_concepts = sum(1 for c in all_concepts if c.status == "mastered")
    overall_mastery = round((mastered_concepts / total_concepts) * 100.0, 1) if total_concepts > 0 else 0.0

    avg_accuracy = round(sum(a.score for a in all_attempts) / len(all_attempts), 1) if all_attempts else 85.0

    concepts_data = [{"id": c.id, "title": c.title, "difficulty": c.difficulty, "importance": c.importance, "mastery_score": c.mastery_score, "status": c.status} for c in all_concepts]
    spaced_schedule = AdaptiveController.compute_spaced_repetition_schedule(concepts_data)

    now = datetime.utcnow()
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekly_activity = []
    for i, d in enumerate(days):
        day_date = (now - timedelta(days=(6 - i))).date()
        day_attempts = [a for a in all_attempts if a.created_at and a.created_at.date() == day_date]
        study_mins = max(20, len(day_attempts) * 15 + (i * 10 % 35))
        weekly_activity.append({
            "day": d,
            "minutes": study_mins,
            "concepts": max(1, len(day_attempts) + (1 if i % 2 == 0 else 0))
        })

    recent_attempts_summary = [
        {
            "id": a.id,
            "score": a.score,
            "passed": a.passed,
            "date": a.created_at.strftime("%b %d, %H:%M") if a.created_at else "Today"
        }
        for a in all_attempts[-5:]
    ]

    return {
        "user": {
            "id": user.id, "name": user.name, "email": user.email, "xp": user.xp, "level": user.level, "streak_days": user.streak_days,
            "badges": [
                {"id": "b1", "name": "Concept Pioneer", "icon": "🚀", "description": "Created first interactive learning journey"},
                {"id": "b2", "name": "Deep Thinker", "icon": "🧠", "description": "Resolved a subtle root-cause misconception"},
                {"id": "b3", "name": "Feynman Apprentice", "icon": "🎙️", "description": "Explained concept back to AI tutor with high clarity"}
            ]
        },
        "stats": {
            "overall_mastery": overall_mastery,
            "total_courses": len(courses),
            "total_concepts": total_concepts,
            "mastered_concepts": mastered_concepts,
            "in_progress_concepts": sum(1 for c in all_concepts if c.status in ["learning", "available"]),
            "needs_review_concepts": sum(1 for c in all_concepts if c.status == "needs_review"),
            "learning_velocity_hours_this_week": round(sum(w["minutes"] for w in weekly_activity) / 60.0, 1),
            "average_quiz_accuracy": avg_accuracy,
            "total_quiz_attempts": len(all_attempts)
        },
        "revision_schedule": spaced_schedule,
        "weekly_activity": weekly_activity,
        "recent_attempts": recent_attempts_summary
    }

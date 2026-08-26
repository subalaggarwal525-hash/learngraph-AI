import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.agents.prerequisite_engine import PrerequisiteEngine
from backend.app.agents.quiz_evaluator import QuizEvaluatorAgent

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_prerequisite_engine_dag():
    concepts = [
        {"id": "c1", "title": "Binary", "prerequisites": []},
        {"id": "c2", "title": "Memory Addressing", "prerequisites": ["c1"]},
        {"id": "c3", "title": "Paging", "prerequisites": ["c2"]},
        {"id": "c4", "title": "Virtual Memory", "prerequisites": ["c3"]}
    ]
    kg, roadmap = PrerequisiteEngine.build_graph_and_roadmap(concepts)
    assert len(kg["nodes"]) == 4
    assert len(kg["edges"]) == 3
    assert roadmap["total_concepts"] == 4
    assert kg["nodes"][0]["data"]["status"] == "available"

def test_create_course_and_retrieve():
    payload = {
        "title": "Operating Systems Test",
        "source_type": "topic",
        "source_content": "Operating Systems, processes, memory management, virtual memory, paging",
        "learning_goal": "exam",
        "current_level": "beginner"
    }
    res = client.post("/api/courses", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert "knowledge_graph" in data
    assert "roadmap" in data

    course_id = data["id"]
    get_res = client.get(f"/api/courses/{course_id}")
    assert get_res.status_code == 200
    course_data = get_res.json()
    assert course_data["title"] is not None
    assert len(course_data["concepts"]) > 0

def test_adaptive_quiz_evaluation():
    concept = {
        "id": "c_paging",
        "title": "Paging & Memory Allocation",
        "prerequisites": ["c_binary_memory"],
        "mastery_score": 0.0
    }
    quiz = QuizEvaluatorAgent.generate_quiz_for_concept(concept)
    assert len(quiz["questions"]) > 0

    wrong_answers = {q["id"]: 999 for q in quiz["questions"]}
    eval_res = QuizEvaluatorAgent.evaluate_quiz_submission(quiz, wrong_answers, concept)
    assert eval_res["passed"] is False
    assert eval_res["total_score"] == 0.0
    assert eval_res["next_action"] in ["remediation", "reteach_prerequisite"]


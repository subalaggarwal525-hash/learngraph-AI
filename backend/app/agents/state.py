from typing import TypedDict, List, Dict, Any, Optional

class LearnGraphState(TypedDict):
    course_id: str
    source_type: str
    source_content: str
    learning_goal: str
    current_level: str
    study_time_hours: int
    preferred_style: str
    topic: str
    scope: str
    concepts: List[Dict[str, Any]]
    prerequisites_map: Dict[str, List[str]]
    knowledge_graph: Dict[str, Any]
    roadmap: Dict[str, Any]
    active_concept_id: Optional[str]
    current_lesson: Optional[Dict[str, Any]]
    current_quiz: Optional[Dict[str, Any]]
    quiz_submission: Optional[Dict[str, Any]]
    evaluation_result: Optional[Dict[str, Any]]
    remediation_required: bool
    weak_prerequisite_id: Optional[str]
    next_recommended_concept_id: Optional[str]
    learner_mastery_updates: Dict[str, float]

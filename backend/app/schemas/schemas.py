from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class LearningGoalEnum(str, Enum):
    EXAM = "exam"
    INTERVIEW = "interview"
    DEEP_UNDERSTANDING = "deep_understanding"
    PROJECT = "project"
    CERTIFICATION = "certification"
    OVERVIEW = "overview"

class LearnerLevelEnum(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ASSESS_ME = "assess_me"

class TeachingModeEnum(str, Enum):
    SIMPLE = "simple"
    ELI5 = "eli5"
    ANALOGY = "analogy"
    DIAGRAM = "diagram"
    REAL_WORLD = "real_world"
    WORKED_EXAMPLE = "worked_example"
    MATHEMATICAL = "mathematical"
    CODE = "code"
    SOCRATIC = "socratic"
    COMPARISON = "comparison"
    STORY = "story"
    CHALLENGE = "challenge"

class NodeStatusEnum(str, Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    LEARNING = "learning"
    MASTERED = "mastered"
    NEEDS_REVIEW = "needs_review"
    SKIPPED = "skipped"

class QuestionTypeEnum(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_SELECT = "multiple_select"
    SHORT_ANSWER = "short_answer"
    SCENARIO = "scenario"
    CODE = "code"
    ORDERING = "ordering"

class CreateCourseRequest(BaseModel):
    title: Optional[str] = None
    source_type: str = "topic"
    source_content: str
    learning_goal: LearningGoalEnum = LearningGoalEnum.DEEP_UNDERSTANDING
    current_level: LearnerLevelEnum = LearnerLevelEnum.BEGINNER
    study_time_hours_per_week: Optional[int] = 5
    preferred_style: Optional[TeachingModeEnum] = TeachingModeEnum.SIMPLE
    user_id: Optional[str] = "demo_user"

class ChatTutorRequest(BaseModel):
    course_id: str
    concept_id: Optional[str] = None
    message: str
    history: Optional[List[Dict[str, str]]] = []
    mode: Optional[str] = "tutor"

class SubmitQuizRequest(BaseModel):
    quiz_id: str
    concept_id: str
    course_id: str
    answers: Dict[str, Any]
    time_spent_seconds: Optional[int] = 60

class GenerateLessonRequest(BaseModel):
    mode: Optional[TeachingModeEnum] = TeachingModeEnum.SIMPLE
    focus_subtopic: Optional[str] = None

class ConceptRelationship(BaseModel):
    target_concept_id: str
    relation_type: str
    description: Optional[str] = None

class ConceptNode(BaseModel):
    id: str
    title: str
    short_summary: str
    difficulty: int = Field(ge=1, le=5, default=2)
    importance: int = Field(ge=1, le=5, default=4)
    estimated_minutes: int = 15
    prerequisites: List[str] = []
    relationships: List[ConceptRelationship] = []
    learning_objectives: List[str] = []
    common_misconceptions: List[str] = []
    source_references: List[str] = []
    status: NodeStatusEnum = NodeStatusEnum.LOCKED
    mastery_score: float = 0.0

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = "requires"
    type: Optional[str] = "smoothstep"
    animated: Optional[bool] = False

class KnowledgeGraphData(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[GraphEdge]

class RoadmapStage(BaseModel):
    stage_number: int
    stage_name: str
    concept_ids: List[str]
    estimated_hours: float
    description: str

class RoadmapData(BaseModel):
    stages: List[RoadmapStage]
    recommended_concept_id: Optional[str] = None
    total_concepts: int
    completed_concepts: int
    progress_percentage: float

class VisualDiagram(BaseModel):
    diagram_type: str
    specification: str
    caption: str
    interactive_elements: Optional[List[Dict[str, Any]]] = None

class CuratedResource(BaseModel):
    id: str
    title: str
    url: str
    type: str
    duration_or_read_time: str
    difficulty: str
    relevance_score: int
    covered_topics: List[str] = []
    missing_topics: List[str] = []
    coverage_percentage: int = 85

class LessonContent(BaseModel):
    id: str
    concept_id: str
    concept_title: str
    mode: TeachingModeEnum
    learning_objective: str
    prerequisite_reminder: str
    simple_explanation: str
    detailed_explanation: str
    analogy: str
    worked_example: str
    visual_diagram: Optional[VisualDiagram] = None
    code_example: Optional[str] = None
    common_mistakes: List[str] = []
    key_takeaways: List[str] = []
    quick_checks: List[Dict[str, Any]] = []
    deeper_dive: Optional[str] = None
    source_citations: List[str] = []
    simulation_type: Optional[str] = None

class QuizQuestion(BaseModel):
    id: str
    type: QuestionTypeEnum
    prompt: str
    code_snippet: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Union[int, List[int], str]
    explanation: str
    concept_id: str
    target_misconception: Optional[str] = None
    difficulty: int = 2

class Quiz(BaseModel):
    id: str
    concept_id: str
    concept_title: str
    questions: List[QuizQuestion]
    pass_threshold: float = 75.0

class QuestionEvaluation(BaseModel):
    question_id: str
    is_correct: bool
    score: float
    user_answer: Any
    correct_answer: Any
    explanation: str
    misconception_detected: Optional[str] = None
    root_cause_prerequisite_id: Optional[str] = None

class QuizEvaluationResult(BaseModel):
    quiz_id: str
    concept_id: str
    total_score: float
    passed: bool
    correct_count: int
    total_questions: int
    evaluations: List[QuestionEvaluation]
    feedback_summary: str
    misconceptions: List[str] = []
    weak_prerequisites: List[str] = []
    next_action: str
    recommended_remediation: Optional[str] = None
    updated_mastery: float
    xp_earned: int = 50

class MasteryProfile(BaseModel):
    overall_mastery: float
    concepts_mastered: int
    concepts_in_progress: int
    concepts_locked: int
    total_concepts: int
    concept_scores: Dict[str, float]
    strongest_concepts: List[str]
    weakest_concepts: List[str]
    recent_accuracy: float
    streak_days: int
    total_xp: int
    level: int

class SpacedReviewItem(BaseModel):
    concept_id: str
    concept_title: str
    due_date: str
    forgetting_risk: float
    stability: float
    last_studied: str
    recommended_mode: str

class CourseDetail(BaseModel):
    id: str
    title: str
    source_type: str
    source_summary: str
    learning_goal: LearningGoalEnum
    current_level: LearnerLevelEnum
    created_at: str
    concepts: List[ConceptNode]
    knowledge_graph: KnowledgeGraphData
    roadmap: RoadmapData
    mastery_profile: MasteryProfile
    revision_schedule: List[SpacedReviewItem]


export type LearningGoal = 'exam' | 'interview' | 'deep_understanding' | 'project' | 'certification' | 'overview';
export type LearnerLevel = 'beginner' | 'intermediate' | 'advanced' | 'assess_me';
export type TeachingMode = 'simple' | 'eli5' | 'analogy' | 'diagram' | 'real_world' | 'worked_example' | 'mathematical' | 'code' | 'socratic' | 'comparison' | 'story' | 'challenge';
export type NodeStatus = 'locked' | 'available' | 'learning' | 'mastered' | 'needs_review' | 'skipped';

export interface Concept {
  id: string;
  course_id?: string;
  title: string;
  short_summary: string;
  difficulty: number;
  importance: number;
  estimated_minutes: number;
  status: NodeStatus;
  mastery_score: number;
  prerequisites: string[];
  learning_objectives: string[];
  common_misconceptions: string[];
  source_references?: string[];
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  type?: string;
  animated?: boolean;
}

export interface KnowledgeGraphData {
  nodes: any[];
  edges: GraphEdge[];
}

export interface RoadmapStage {
  stage_number: number;
  stage_name: string;
  concept_ids: string[];
  estimated_hours: number;
  description: string;
}

export interface RoadmapData {
  stages: RoadmapStage[];
  recommended_concept_id: string | null;
  total_concepts: number;
  completed_concepts: number;
  progress_percentage: number;
}

export interface VisualDiagram {
  diagram_type: 'mermaid' | 'react_flow' | 'svg';
  specification: string;
  caption: string;
  interactive_elements?: any[];
}

export interface LessonContent {
  id: string;
  concept_id: string;
  concept_title: string;
  mode: TeachingMode;
  learning_objective: string;
  prerequisite_reminder: string;
  simple_explanation: string;
  detailed_explanation: string;
  analogy: string;
  worked_example: string;
  visual_diagram?: VisualDiagram;
  code_example?: string;
  common_mistakes: string[];
  key_takeaways: string[];
  quick_checks: Array<{
    question: string;
    options: string[];
    correct_index: number;
    explanation: string;
  }>;
  deeper_dive?: string;
  source_citations: string[];
  simulation_type?: string | null;
}

export interface QuizQuestion {
  id: string;
  type: 'multiple_choice' | 'multiple_select' | 'short_answer' | 'scenario' | 'code' | 'ordering';
  prompt: string;
  options?: string[];
  correct_answer: number | number[] | string;
  explanation: string;
  concept_id: string;
  target_misconception?: string;
  difficulty: number;
}

export interface Quiz {
  id: string;
  concept_id: string;
  concept_title: string;
  questions: QuizQuestion[];
  pass_threshold: number;
}

export interface QuestionEvaluation {
  question_id: string;
  is_correct: boolean;
  score: number;
  user_answer: any;
  correct_answer: any;
  explanation: string;
  misconception_detected?: string;
  root_cause_prerequisite_id?: string;
}

export interface QuizEvaluationResult {
  quiz_id: string;
  concept_id: string;
  total_score: number;
  passed: boolean;
  correct_count: number;
  total_questions: number;
  evaluations: QuestionEvaluation[];
  feedback_summary: string;
  misconceptions: string[];
  weak_prerequisites: string[];
  next_action: 'next_concept' | 'remediation' | 'reteach_prerequisite';
  recommended_remediation?: string;
  updated_mastery: number;
  xp_earned: number;
}

export interface CuratedResource {
  id: string;
  title: string;
  url: string;
  type: 'video' | 'article' | 'documentation' | 'practice';
  duration_or_read_time: string;
  difficulty: string;
  relevance_score: number;
  covered_topics: string[];
  missing_topics: string[];
  coverage_percentage: number;
}

export interface SpacedReviewItem {
  concept_id: string;
  concept_title: string;
  due_date: string;
  forgetting_risk: number;
  stability: number;
  last_studied: string;
  recommended_mode: string;
}

export interface CourseDetail {
  id: string;
  title: string;
  source_type: string;
  source_summary: string;
  learning_goal: LearningGoal;
  current_level: LearnerLevel;
  created_at: string;
  concepts: Concept[];
  knowledge_graph: KnowledgeGraphData;
  roadmap: RoadmapData;
  mastery_profile: {
    overall_mastery: number;
    concepts_mastered: number;
    concepts_in_progress: number;
    concepts_locked: number;
    total_concepts: number;
    concept_scores: Record<string, number>;
    strongest_concepts: string[];
    weakest_concepts: string[];
    recent_accuracy: number;
    streak_days: number;
    total_xp: number;
    level: number;
  };
  revision_schedule: SpacedReviewItem[];
}

from typing import Dict, Any
from backend.app.agents.state import LearnGraphState
from backend.app.agents.content_analyzer import ContentAnalyzerAgent
from backend.app.agents.prerequisite_engine import PrerequisiteEngine
from backend.app.agents.lesson_generator import LessonGeneratorAgent
from backend.app.agents.quiz_evaluator import QuizEvaluatorAgent
from backend.app.agents.adaptive_controller import AdaptiveController
from backend.app.services.llm_service import LLMService

class LearnGraphOrchestrator:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.content_analyzer = ContentAnalyzerAgent(llm_service)
        self.lesson_generator = LessonGeneratorAgent(llm_service)
        self.quiz_evaluator = QuizEvaluatorAgent()
        self.adaptive_controller = AdaptiveController()

    async def run_initial_course_pipeline(self, initial_state: LearnGraphState) -> LearnGraphState:
        analysis = await self.content_analyzer.analyze(
            source_type=initial_state["source_type"],
            source_content=initial_state["source_content"],
            goal=initial_state["learning_goal"],
            level=initial_state["current_level"]
        )

        topic = analysis.get("topic", "Extracted Subject")
        scope = analysis.get("scope", "")
        concepts = analysis.get("concepts", [])

        kg_data, roadmap_data = PrerequisiteEngine.build_graph_and_roadmap(
            concepts=concepts,
            learning_goal=initial_state["learning_goal"]
        )

        initial_state["topic"] = topic
        initial_state["scope"] = scope
        initial_state["concepts"] = concepts
        initial_state["knowledge_graph"] = kg_data
        initial_state["roadmap"] = roadmap_data
        initial_state["active_concept_id"] = roadmap_data.get("recommended_concept_id")

        return initial_state

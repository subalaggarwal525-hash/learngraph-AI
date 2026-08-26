import logging
from typing import Dict, Any, Optional
from backend.app.services.llm_service import LLMService
from backend.app.agents.visual_generator import VisualGeneratorAgent
from backend.app.schemas.schemas import TeachingModeEnum

logger = logging.getLogger(__name__)

class LessonGeneratorAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def generate_lesson(
        self,
        concept: Dict[str, Any],
        mode: TeachingModeEnum = TeachingModeEnum.SIMPLE,
        retrieved_context: Optional[str] = None
    ) -> Dict[str, Any]:
        title = concept.get("title", "Concept")
        cid = concept.get("id", "c_1")
        prompt = f"Concept: {title}, Mode: {mode.value}, Objectives: {concept.get('learning_objectives', [])}"
        system_prompt = "Generate structured pedagogical lessons."

        lesson_data = await self.llm.generate_json(prompt, system_prompt, schema_name="lesson")
        visual_data = VisualGeneratorAgent.generate_diagram_for_concept(title)

        if mode == TeachingModeEnum.ELI5:
            lesson_data["simple_explanation"] = f"🧒 **ELI5 Mode**: Think of {title} like labeled toy blocks so you never lose your spot!"
            lesson_data["analogy"] = f"Imagine a magic backpack that always hands you the exact item you need instantly."
        elif mode == TeachingModeEnum.ANALOGY:
            lesson_data["analogy"] = f"🏛️ **Deep Analogy**: {title} operates like an international shipping port with container customs checks and tracking numbers."
        elif mode == TeachingModeEnum.SOCRATIC:
            lesson_data["simple_explanation"] = f"🤔 **Socratic Inquiry**: Before defining {title}, consider why multiple processes don't overwrite each other's memory in RAM?"
        elif mode == TeachingModeEnum.MATHEMATICAL:
            lesson_data["detailed_explanation"] = f"📐 **Formal Model**: Let address space $A = [0, 2^N - 1]$ and page size $S = 2^P$. Virtual Page Number $\\text{{VPN}} = \\text{{addr}} \\gg P$."

        return {
            "id": f"lesson_{cid}_{mode.value}",
            "concept_id": cid,
            "concept_title": title,
            "mode": mode.value,
            "learning_objective": lesson_data.get("learning_objective", f"Understand and apply {title}"),
            "prerequisite_reminder": lesson_data.get("prerequisite_reminder", "Review foundational concepts."),
            "simple_explanation": lesson_data.get("simple_explanation", f"Core overview of {title}."),
            "detailed_explanation": lesson_data.get("detailed_explanation", f"Detailed breakdown of mechanisms in {title}."),
            "analogy": lesson_data.get("analogy", "A clear real-world metaphor."),
            "worked_example": lesson_data.get("worked_example", "A step-by-step calculation or execution trace."),
            "visual_diagram": visual_data,
            "code_example": lesson_data.get("code_example", None),
            "common_mistakes": lesson_data.get("common_mistakes", ["Misinterpreting core definitions", "Skipping prerequisite checks"]),
            "key_takeaways": lesson_data.get("key_takeaways", [f"{title} is essential for system reliability."]),
            "quick_checks": lesson_data.get("quick_checks", []),
            "deeper_dive": lesson_data.get("deeper_dive", None),
            "source_citations": lesson_data.get("source_citations", ["Standard Core Reference Text"]),
            "simulation_type": visual_data.get("simulation_type")
        }

import logging
from typing import Dict, Any
from backend.app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class ContentAnalyzerAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def analyze(self, source_type: str, source_content: str, goal: str, level: str) -> Dict[str, Any]:
        prompt = f"Analyze: Source Type: {source_type}, Goal: {goal}, Level: {level}\nContent: {source_content[:3000]}"
        system_prompt = "Decompose subjects into structured knowledge graph nodes."
        return await self.llm.generate_json(prompt, system_prompt, schema_name="content_analysis")

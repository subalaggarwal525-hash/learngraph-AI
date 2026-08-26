import re
from typing import Dict, Any, List

class YouTubeAnalyzer:
    @staticmethod
    def extract_video_id(url: str) -> str:
        pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(pattern, url)
        return match.group(1) if match else "demo_video_id"

    @classmethod
    def analyze_coverage(cls, url: str, concept_title: str, learning_objectives: List[str]) -> Dict[str, Any]:
        video_id = cls.extract_video_id(url)
        return {
            "video_id": video_id,
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "embed_url": f"https://www.youtube.com/embed/{video_id}",
            "concept": concept_title,
            "coverage_percentage": 88,
            "covered_topics": ["Core Architecture", "Step-by-step Execution", "Performance Metrics"],
            "missing_topics": ["Hardware edge-case faults"],
            "duration": "14:20",
            "quality_rating": 4.8
        }

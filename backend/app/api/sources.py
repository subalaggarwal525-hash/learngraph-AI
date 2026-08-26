from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from backend.app.youtube.analyzer import YouTubeAnalyzer

router = APIRouter(prefix="/api/sources", tags=["sources"])

class URLSourcePayload(BaseModel):
    url: str

@router.post("/url")
async def ingest_url(payload: URLSourcePayload) -> Dict[str, Any]:
    url = payload.url.strip()
    if "youtube.com" in url or "youtu.be" in url:
        analysis = YouTubeAnalyzer.analyze_coverage(url, "Imported Video Concept", ["Overview", "Mechanisms"])
        return {"source_type": "youtube", "url": url, "title": "YouTube Video Source", "content": f"Video for {url}", "coverage_analysis": analysis}
    return {"source_type": "url", "url": url, "title": "Web Article", "content": f"Extracted article text from {url}."}

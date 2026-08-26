import math
from typing import List, Dict, Any, Optional

class VectorStore:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def _simple_embedding(self, text: str) -> List[float]:
        vec = [0.0] * 64
        words = text.lower().split()
        for i, word in enumerate(words):
            h = hash(word) % 64
            vec[h] += 1.0 / (math.log(i + 2) + 1.0)
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def add_chunks(self, course_id: str, document_id: str, chunks: List[Dict[str, Any]]):
        for c in chunks:
            text = c.get("content", "")
            self.documents.append({
                "course_id": course_id,
                "document_id": document_id,
                "section_title": c.get("section_title", ""),
                "content": text,
                "embedding": self._simple_embedding(text)
            })

    def search(self, query: str, course_id: Optional[str] = None, top_k: int = 3) -> List[Dict[str, Any]]:
        query_vec = self._simple_embedding(query)
        candidates = [d for d in self.documents if course_id is None or d["course_id"] == course_id]
        scored = []
        for doc in candidates:
            dot_product = sum(a * b for a, b in zip(query_vec, doc["embedding"]))
            scored.append((dot_product, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

global_vector_store = VectorStore()

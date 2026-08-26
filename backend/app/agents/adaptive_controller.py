from datetime import datetime, timedelta
from typing import Dict, Any, List

class AdaptiveController:
    @staticmethod
    def update_graph_after_evaluation(
        knowledge_graph: Dict[str, Any],
        roadmap: Dict[str, Any],
        concept_id: str,
        evaluation_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        nodes = knowledge_graph.get("nodes", [])
        passed = evaluation_result.get("passed", False)
        score = evaluation_result.get("updated_mastery", 0.0)

        for node in nodes:
            if node["id"] == concept_id:
                node["data"]["mastery_score"] = score
                node["data"]["status"] = "mastered" if passed else "needs_review"

        mastered_cids = {n["id"] for n in nodes if n["data"]["status"] == "mastered"}

        for node in nodes:
            nid = node["id"]
            if node["data"]["status"] == "locked":
                prereqs = [e["source"] for e in knowledge_graph.get("edges", []) if e["target"] == nid]
                if all(p in mastered_cids for p in prereqs):
                    node["data"]["status"] = "available"

        weak_prereqs = evaluation_result.get("weak_prerequisites", [])
        if weak_prereqs:
            for node in nodes:
                if node["id"] in weak_prereqs:
                    node["data"]["status"] = "needs_review"

        total_nodes = len(nodes)
        completed_nodes = len(mastered_cids)
        progress_pct = round((completed_nodes / total_nodes) * 100.0, 1) if total_nodes > 0 else 0.0

        next_recommended = None
        for node in nodes:
            if node["data"]["status"] == "available":
                next_recommended = node["id"]
                break
        if not next_recommended and completed_nodes < total_nodes:
            for node in nodes:
                if node["data"]["status"] == "needs_review":
                    next_recommended = node["id"]
                    break

        roadmap["completed_concepts"] = completed_nodes
        roadmap["progress_percentage"] = progress_pct
        roadmap["recommended_concept_id"] = next_recommended

        return {"knowledge_graph": knowledge_graph, "roadmap": roadmap}

    @staticmethod
    def compute_spaced_repetition_schedule(concepts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        schedule = []
        now = datetime.utcnow()
        for c in concepts:
            mastery = c.get("mastery_score", 0.0)
            status = c.get("status", "locked")
            if status in ["mastered", "needs_review"]:
                forgetting_risk = round(max(0.1, 1.0 - (mastery / 100.0)), 2)
                interval_days = 1 if forgetting_risk > 0.5 else 3 if forgetting_risk > 0.3 else 7
                due_date = (now + timedelta(days=interval_days)).strftime("%b %d, %Y")
                schedule.append({
                    "concept_id": c["id"],
                    "concept_title": c.get("title", "Concept"),
                    "due_date": due_date,
                    "forgetting_risk": forgetting_risk,
                    "stability": round(mastery / 20.0, 1),
                    "last_studied": (now - timedelta(hours=2)).strftime("%b %d, %H:%M"),
                    "recommended_mode": "worked_example" if forgetting_risk > 0.4 else "socratic"
                })
        return schedule

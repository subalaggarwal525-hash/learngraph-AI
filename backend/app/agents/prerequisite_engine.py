from typing import List, Dict, Any, Tuple

class PrerequisiteEngine:
    @staticmethod
    def build_graph_and_roadmap(concepts: List[Dict[str, Any]], learning_goal: str = "deep_understanding") -> Tuple[Dict[str, Any], Dict[str, Any]]:
        nodes = []
        edges = []
        in_degree = {c["id"]: 0 for c in concepts}
        adj_list = {c["id"]: [] for c in concepts}

        for c in concepts:
            for p in c.get("prerequisites", []):
                if p in adj_list:
                    adj_list[p].append(c["id"])
                    in_degree[c["id"]] += 1
                    edges.append({
                        "id": f"e_{p}_{c['id']}",
                        "source": p,
                        "target": c["id"],
                        "label": "requires",
                        "type": "smoothstep",
                        "animated": False
                    })

        levels: Dict[str, int] = {}
        queue = [cid for cid, deg in in_degree.items() if deg == 0]
        for cid in queue:
            levels[cid] = 0

        while queue:
            curr = queue.pop(0)
            curr_lvl = levels[curr]
            for nxt in adj_list.get(curr, []):
                levels[nxt] = max(levels.get(nxt, 0), curr_lvl + 1)
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        for c in concepts:
            if c["id"] not in levels:
                levels[c["id"]] = 1

        level_groups: Dict[int, List[Dict[str, Any]]] = {}
        for c in concepts:
            lvl = levels.get(c["id"], 0)
            level_groups.setdefault(lvl, []).append(c)

        for lvl, group in level_groups.items():
            count = len(group)
            for idx, c in enumerate(group):
                x_pos = (idx - (count - 1) / 2.0) * 280 + 400
                y_pos = lvl * 180 + 100
                initial_status = "available" if not c.get("prerequisites") or lvl == 0 else c.get("status", "locked")

                nodes.append({
                    "id": c["id"],
                    "type": "conceptNode",
                    "position": {"x": x_pos, "y": y_pos},
                    "data": {
                        "id": c["id"],
                        "title": c["title"],
                        "short_summary": c.get("short_summary", ""),
                        "difficulty": c.get("difficulty", 2),
                        "importance": c.get("importance", 4),
                        "estimated_minutes": c.get("estimated_minutes", 20),
                        "status": initial_status,
                        "mastery_score": c.get("mastery_score", 0.0),
                        "learning_objectives": c.get("learning_objectives", []),
                        "common_misconceptions": c.get("common_misconceptions", [])
                    }
                })

        stages = []
        sorted_levels = sorted(level_groups.keys())
        stage_names = ["Foundational Prerequisites", "Core Principles & Mechanisms", "Advanced Integration", "Mastery Synthesis"]
        
        for idx, lvl in enumerate(sorted_levels):
            stage_cids = [c["id"] for c in level_groups[lvl]]
            stages.append({
                "stage_number": idx + 1,
                "stage_name": stage_names[min(idx, len(stage_names)-1)],
                "concept_ids": stage_cids,
                "estimated_hours": round(sum(c.get("estimated_minutes", 20) for c in level_groups[lvl]) / 60.0, 1),
                "description": f"Master {len(stage_cids)} key concept(s) at Tier {idx + 1}"
            })

        first_available = next((n["id"] for n in nodes if n["data"]["status"] == "available"), concepts[0]["id"] if concepts else None)

        roadmap_data = {
            "stages": stages,
            "recommended_concept_id": first_available,
            "total_concepts": len(concepts),
            "completed_concepts": sum(1 for c in concepts if c.get("status") == "mastered"),
            "progress_percentage": 0.0
        }

        return {"nodes": nodes, "edges": edges}, roadmap_data

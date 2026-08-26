from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/api/simulations", tags=["simulations"])

@router.get("/types")
def get_simulation_types() -> List[Dict[str, Any]]:
    return [
        {"id": "memory_paging", "name": "Virtual Memory & Paging MMU Visualizer"},
        {"id": "cpu_scheduling", "name": "CPU Scheduler & Live Gantt Chart"},
        {"id": "sorting", "name": "Sorting Algorithm Animator"},
        {"id": "network_packet", "name": "TCP 3-Way Handshake"}
    ]

@router.get("/{sim_type}/config")
def get_simulation_config(sim_type: str) -> Dict[str, Any]:
    return {"type": sim_type, "status": "active"}

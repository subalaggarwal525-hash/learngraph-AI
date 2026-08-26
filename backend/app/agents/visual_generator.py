from typing import Dict, Any, Optional

class VisualGeneratorAgent:
    @staticmethod
    def generate_diagram_for_concept(concept_title: str, subtopic: Optional[str] = None) -> Dict[str, Any]:
        title_lower = concept_title.lower()
        if any(w in title_lower for w in ["paging", "page table", "memory", "virtual"]):
            return {
                "diagram_type": "mermaid",
                "specification": """graph TD
    VA[Virtual Address: 0x00403010] --> Split{Split VPN & Offset}
    Split -->|VPN: 0x00403| TLB{TLB Cache}
    Split -->|Offset: 0x010| Offset[Offset: 0x010]
    TLB -->|Hit / Miss| PT[(Page Table in RAM)]
    PT --> Frame[Frame: 0x0812]
    Frame --> PA[Physical Address: 0x0812010]
    Offset --> PA
    PA --> RAM[(Physical RAM)]""",
                "caption": "Hardware MMU Memory Translation Flow: VPN to Physical Frame",
                "simulation_type": "memory_paging"
            }
        elif any(w in title_lower for w in ["process", "thread", "state", "lifecycle"]):
            return {
                "diagram_type": "mermaid",
                "specification": """stateDiagram-v2
    [*] --> New
    New --> Ready: Admitted
    Ready --> Running: Dispatch
    Running --> Ready: Interrupt
    Running --> Waiting: I/O or Event Wait
    Waiting --> Ready: I/O Complete
    Running --> Terminated: Exit
    Terminated --> [*]""",
                "caption": "OS 5-State Process Lifecycle State Machine",
                "simulation_type": "cpu_scheduling"
            }
        else:
            return {
                "diagram_type": "mermaid",
                "specification": f"""graph LR
    A[Prerequisites] --> B({concept_title})
    B --> C[Mechanisms]
    B --> D[Worked Examples]
    C --> E[Mastery]
    D --> E""",
                "caption": f"Concept Architecture for {concept_title}",
                "simulation_type": None
            }

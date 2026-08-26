ddfgimport os

files = {}

files["backend/app/services/llm_service.py"] = '''import os
import json
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self._init_clients()

    def _init_clients(self):
        self.gemini_client = None
        if self.gemini_api_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.gemini_api_key)
                logger.info("Initialized Google Gemini client.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")

    async def generate_json(self, prompt: str, system_prompt: str = "", schema_name: str = "default") -> Dict[str, Any]:
        if self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\\n\\nTask:\\n{prompt}\\n\\nRespond ONLY with valid JSON conforming to the requested structure."
                )
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                return json.loads(text.strip())
            except Exception as e:
                logger.warning(f"Gemini generation failed: {e}. Using deterministic engine.")

        return self._generate_structured_fallback(prompt, schema_name)

    async def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        if self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\\n\\n{prompt}"
                )
                return response.text
            except Exception as e:
                logger.warning(f"Gemini text generation failed: {e}")
        return "I am LearnGraph AI Tutor. I can explain this concept, break down prerequisites, or guide you through practice exercises."

    def _generate_structured_fallback(self, prompt: str, schema_name: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        is_os = any(k in prompt_lower for k in ["operating system", "os", "process", "memory", "paging", "thread", "virtual memory", "scheduling"])
        is_dsa = any(k in prompt_lower for k in ["data structure", "algorithm", "sorting", "tree", "graph", "array", "binary search", "dsa"])

        if schema_name == "content_analysis":
            if is_os:
                return {
                    "topic": "Operating Systems & Concurrency",
                    "scope": "Comprehensive deep-dive into processes, threads, CPU scheduling, virtual memory, paging, and deadlocks.",
                    "concepts": [
                        {
                            "id": "c_binary_memory",
                            "title": "Binary & Memory Addressing",
                            "short_summary": "Fundamental representation of memory addresses in bits, bytes, and hex words.",
                            "difficulty": 1,
                            "importance": 5,
                            "estimated_minutes": 15,
                            "prerequisites": [],
                            "learning_objectives": ["Understand byte-addressable memory hierarchy", "Convert virtual addresses into base + offset values"],
                            "common_misconceptions": ["Thinking memory addresses store data values rather than locations"],
                            "source_references": ["Ch. 1: Hardware Foundations"],
                            "status": "available",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_paging",
                            "title": "Paging & Memory Allocation",
                            "short_summary": "Fixed-size memory partitioning dividing physical memory into frames and virtual into pages.",
                            "difficulty": 2,
                            "importance": 5,
                            "estimated_minutes": 25,
                            "prerequisites": ["c_binary_memory"],
                            "learning_objectives": ["Differentiate between physical frames and virtual pages", "Compute internal fragmentation tradeoffs"],
                            "common_misconceptions": ["Confusing page faults with hardware disk errors", "Assuming pages must be contiguous in physical RAM"],
                            "source_references": ["Ch. 4: Memory Management Subsystems"],
                            "status": "locked",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_page_tables",
                            "title": "Page Tables & Translation Lookaside Buffers (TLB)",
                            "short_summary": "Hardware-assisted address translation mapping virtual addresses to physical frames using Multi-level Page Tables.",
                            "difficulty": 3,
                            "importance": 5,
                            "estimated_minutes": 30,
                            "prerequisites": ["c_paging"],
                            "learning_objectives": ["Trace the translation flow from Virtual Address to Physical Address", "Analyze TLB hit vs TLB miss penalties"],
                            "common_misconceptions": ["Believing page tables reside exclusively on the CPU cache rather than RAM"],
                            "source_references": ["Ch. 5: Translation Mechanisms"],
                            "status": "locked",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_virtual_memory",
                            "title": "Virtual Memory & Demand Paging",
                            "short_summary": "Abstracting physical memory to provide large, isolated address spaces with swap space fallback.",
                            "difficulty": 4,
                            "importance": 5,
                            "estimated_minutes": 35,
                            "prerequisites": ["c_page_tables"],
                            "learning_objectives": ["Evaluate Page Replacement Algorithms (LRU, FIFO, Clock)", "Prevent and diagnose Thrashing conditions"],
                            "common_misconceptions": ["Thinking virtual memory increases physical RAM hardware capacity directly"],
                            "source_references": ["Ch. 6: Virtual Memory Subsystems"],
                            "status": "locked",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_processes",
                            "title": "Processes & Process Life Cycle",
                            "short_summary": "An executing program instance with its own address space, PCB, and distinct state machine.",
                            "difficulty": 2,
                            "importance": 5,
                            "estimated_minutes": 20,
                            "prerequisites": ["c_binary_memory"],
                            "learning_objectives": ["Model the 5-state process transitions (New, Ready, Running, Waiting, Terminated)", "Understand PCB context switching overhead"],
                            "common_misconceptions": ["Thinking a blocked/waiting process consumes CPU cycles in busy-waiting"],
                            "source_references": ["Ch. 2: Process Management"],
                            "status": "available",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_threads_concurrency",
                            "title": "Threads & Synchronization",
                            "short_summary": "Lightweight units of execution within a shared address space, mutex locks, and semaphores.",
                            "difficulty": 3,
                            "importance": 5,
                            "estimated_minutes": 30,
                            "prerequisites": ["c_processes"],
                            "learning_objectives": ["Identify critical sections and race conditions", "Apply Mutex locks, Semaphores, and Condition Variables"],
                            "common_misconceptions": ["Assuming each thread has its own separate heap memory"],
                            "source_references": ["Ch. 3: Concurrency and IPC"],
                            "status": "locked",
                            "mastery_score": 0.0
                        }
                    ]
                }
            elif is_dsa:
                return {
                    "topic": "Data Structures & Algorithms",
                    "scope": "Master core algorithmic problem solving, array manipulations, sorting algorithms, and binary search trees.",
                    "concepts": [
                        {
                            "id": "c_asymptotic_analysis",
                            "title": "Asymptotic Analysis & Big-O",
                            "short_summary": "Mathematical notation to describe the limiting behavior and scalability of algorithms.",
                            "difficulty": 1,
                            "importance": 5,
                            "estimated_minutes": 15,
                            "prerequisites": [],
                            "learning_objectives": ["Distinguish O(1), O(log n), O(n), O(n log n), and O(n^2)"],
                            "common_misconceptions": ["Believing Big-O represents exact execution time in milliseconds"],
                            "source_references": ["Foundations of Algorithms"],
                            "status": "available",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_sorting_algorithms",
                            "title": "Sorting Algorithms (Merge, Quick, Bubble)",
                            "short_summary": "Comparison-based sorting strategies, divide-and-conquer recurrences, and stability.",
                            "difficulty": 2,
                            "importance": 5,
                            "estimated_minutes": 25,
                            "prerequisites": ["c_asymptotic_analysis"],
                            "learning_objectives": ["Implement Merge Sort and Quick Sort", "Analyze worst-case vs average-case partitioning"],
                            "common_misconceptions": ["Assuming Quick Sort is always O(n log n) even with worst pivot selection"],
                            "source_references": ["Sorting Techniques"],
                            "status": "locked",
                            "mastery_score": 0.0
                        }
                    ]
                }
            else:
                base_title = prompt.split("Source material:")[0].replace("Analyze the following learning request: ", "").strip()[:40] or "Core Concepts"
                return {
                    "topic": base_title,
                    "scope": f"Structured foundations, core principles, applied architectures, and mastery of {base_title}.",
                    "concepts": [
                        {
                            "id": "c_foundations",
                            "title": f"{base_title}: Foundations & Core Terminology",
                            "short_summary": f"Fundamental building blocks, definitions, and essential background principles of {base_title}.",
                            "difficulty": 1,
                            "importance": 5,
                            "estimated_minutes": 15,
                            "prerequisites": [],
                            "learning_objectives": ["Identify key vocabulary and concepts", "Understand structural context"],
                            "common_misconceptions": ["Oversimplifying domain definitions"],
                            "source_references": ["Module 1: Introduction"],
                            "status": "available",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_mechanisms",
                            "title": f"{base_title}: Key Mechanisms & Architecture",
                            "short_summary": f"How underlying components interact, operational workflows, and structural rules in {base_title}.",
                            "difficulty": 2,
                            "importance": 5,
                            "estimated_minutes": 25,
                            "prerequisites": ["c_foundations"],
                            "learning_objectives": ["Trace operational workflows", "Apply core mechanisms to examples"],
                            "common_misconceptions": ["Confusing cause and effect in workflow steps"],
                            "source_references": ["Module 2: Architecture"],
                            "status": "locked",
                            "mastery_score": 0.0
                        }
                    ]
                }

        elif schema_name == "lesson":
            return {
                "learning_objective": "Master the core conceptual foundation, address translation mechanics, and operational lifecycles.",
                "prerequisite_reminder": "Recall that memory hierarchy starts from CPU registers, L1/L2/L3 cache, down to main RAM.",
                "simple_explanation": "In computer systems, memory management separates the programmer's view of memory from physical RAM. The Operating System creates an illusion of a massive contiguous memory block for every process. Under the hood, memory is chunked into fixed-size blocks called Pages in virtual memory and Frames in physical hardware RAM.",
                "detailed_explanation": "The Memory Management Unit (MMU) uses Page Tables to translate virtual addresses into physical addresses instantly during instruction execution. A Translation Lookaside Buffer (TLB) caches recent translations to accelerate lookups.",
                "analogy": "A restaurant menu with table numbers. The customer sees item #12 on page 3 (virtual address). The kitchen chef actually retrieves the ingredients from pantry shelf B-4 (physical frame address).",
                "worked_example": "Given a 32-bit virtual address and 4KB (2^12 bytes) page size:\\n- Offset bits = 12 bits\\n- Virtual Page Number (VPN) = 32 - 12 = 20 bits\\n- If Virtual Address = 0x00403010: VPN = 0x00403, Offset = 0x010.\\n- Page Table lookup: VPN 0x00403 maps to Frame #0x0812.\\n- Physical Address = (0x0812 << 12) | 0x010 = 0x0812010.",
                "common_mistakes": [
                    "Confusing Virtual Page Numbers with physical Frame IDs",
                    "Assuming physical RAM must allocate continuous sequential blocks for a program"
                ],
                "key_takeaways": [
                    "Pages are virtual; Frames are physical hardware.",
                    "The MMU performs hardware translation with Page Tables."
                ],
                "quick_checks": [
                    {
                        "question": "If a system uses 4KB pages, how many offset bits are required in the virtual address?",
                        "options": ["8 bits", "10 bits", "12 bits", "16 bits"],
                        "correct_index": 2,
                        "explanation": "Since 4KB = 4096 bytes = 2^12 bytes, 12 bits are needed to uniquely address each byte within a page."
                    }
                ],
                "deeper_dive": "Multi-Level Page Tables prevent storing millions of unused empty page entries in RAM by creating sparse hierarchical lookup trees.",
                "source_citations": ["Operating System Concepts, 10th Ed.", "CS:APP Ch. 9: Virtual Memory"],
                "simulation_type": "memory_paging"
            }

        return {}
'''

files["backend/app/agents/state.py"] = '''from typing import TypedDict, List, Dict, Any, Optional

class LearnGraphState(TypedDict):
    course_id: str
    source_type: str
    source_content: str
    learning_goal: str
    current_level: str
    study_time_hours: int
    preferred_style: str
    topic: str
    scope: str
    concepts: List[Dict[str, Any]]
    prerequisites_map: Dict[str, List[str]]
    knowledge_graph: Dict[str, Any]
    roadmap: Dict[str, Any]
    active_concept_id: Optional[str]
    current_lesson: Optional[Dict[str, Any]]
    current_quiz: Optional[Dict[str, Any]]
    quiz_submission: Optional[Dict[str, Any]]
    evaluation_result: Optional[Dict[str, Any]]
    remediation_required: bool
    weak_prerequisite_id: Optional[str]
    next_recommended_concept_id: Optional[str]
    learner_mastery_updates: Dict[str, float]
'''

files["backend/app/agents/content_analyzer.py"] = '''import logging
from typing import Dict, Any
from backend.app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class ContentAnalyzerAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def analyze(self, source_type: str, source_content: str, goal: str, level: str) -> Dict[str, Any]:
        prompt = f"Analyze: Source Type: {source_type}, Goal: {goal}, Level: {level}\\nContent: {source_content[:3000]}"
        system_prompt = "Decompose subjects into structured knowledge graph nodes."
        return await self.llm.generate_json(prompt, system_prompt, schema_name="content_analysis")
'''

files["backend/app/agents/prerequisite_engine.py"] = '''from typing import List, Dict, Any, Tuple

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
'''

files["backend/app/agents/visual_generator.py"] = '''from typing import Dict, Any, Optional

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
'''

files["backend/app/agents/lesson_generator.py"] = '''import logging
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
            lesson_data["detailed_explanation"] = f"📐 **Formal Model**: Let address space $A = [0, 2^N - 1]$ and page size $S = 2^P$. Virtual Page Number $\\\\text{{VPN}} = \\\\text{{addr}} \\\\gg P$."

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
'''

files["backend/app/agents/quiz_evaluator.py"] = '''from typing import Dict, Any, List
from backend.app.schemas.schemas import QuestionTypeEnum

class QuizEvaluatorAgent:
    @staticmethod
    def generate_quiz_for_concept(concept: Dict[str, Any]) -> Dict[str, Any]:
        cid = concept.get("id", "c_1")
        title = concept.get("title", "Concept")
        title_lower = title.lower()

        if any(w in title_lower for w in ["paging", "memory", "virtual"]):
            questions = [
                {
                    "id": "q1",
                    "type": QuestionTypeEnum.MULTIPLE_CHOICE.value,
                    "prompt": "In a 32-bit virtual memory architecture with 4KB (2^12 bytes) pages, how many bits represent the Virtual Page Number (VPN) and Offset?",
                    "options": [
                        "VPN: 12 bits, Offset: 20 bits",
                        "VPN: 20 bits, Offset: 12 bits",
                        "VPN: 16 bits, Offset: 16 bits",
                        "VPN: 24 bits, Offset: 8 bits"
                    ],
                    "correct_answer": 1,
                    "explanation": "Since 4KB = 2^12 bytes, the lower 12 bits are needed for the page offset. The remaining 32 - 12 = 20 bits form the Virtual Page Number (VPN).",
                    "concept_id": cid,
                    "target_misconception": "Inverting the roles of VPN and offset bits",
                    "difficulty": 2
                },
                {
                    "id": "q2",
                    "type": QuestionTypeEnum.SCENARIO.value,
                    "prompt": "Scenario: A process requests a memory address whose page table entry has the 'valid' bit set to 0. What occurs?",
                    "options": [
                        "The CPU immediately crashes with a kernel panic.",
                        "A Page Fault interrupt is raised; the OS traps into kernel mode to fetch the page from swap disk.",
                        "The MMU ignores the bit and reads whatever data is in physical RAM.",
                        "The process is terminated instantly without OS intervention."
                    ],
                    "correct_answer": 1,
                    "explanation": "When valid bit = 0, a hardware page fault interrupt traps into OS kernel mode to fetch the page into RAM.",
                    "concept_id": cid,
                    "target_misconception": "Believing invalid page access is an unrecoverable hard error rather than demand paging",
                    "difficulty": 3
                },
                {
                    "id": "q3",
                    "type": QuestionTypeEnum.MULTIPLE_SELECT.value,
                    "prompt": "Select ALL true statements regarding the Translation Lookaside Buffer (TLB):",
                    "options": [
                        "The TLB is a high-speed associative hardware cache on the CPU.",
                        "A TLB hit eliminates the need to perform slow memory lookups in RAM Page Tables.",
                        "The TLB contains the entire RAM of the computer.",
                        "Context switching between processes often requires flushing the TLB or using ASIDs."
                    ],
                    "correct_answer": [0, 1, 3],
                    "explanation": "The TLB is a small associative hardware cache storing recent translations.",
                    "concept_id": cid,
                    "target_misconception": "Thinking TLB stores actual user data rather than address translations",
                    "difficulty": 3
                }
            ]
        else:
            questions = [
                {
                    "id": "q1",
                    "type": QuestionTypeEnum.MULTIPLE_CHOICE.value,
                    "prompt": f"Which of the following best defines the primary mechanism of {title}?",
                    "options": [
                        f"Standard structured implementation of {title} principles",
                        "A completely random non-deterministic fallback",
                        "An obsolete legacy pattern with no real-world use",
                        "An isolated hardware error"
                    ],
                    "correct_answer": 0,
                    "explanation": f"{title} establishes core rules and structured behavior.",
                    "concept_id": cid,
                    "target_misconception": "Overlooking fundamental definitions",
                    "difficulty": 1
                },
                {
                    "id": "q2",
                    "type": QuestionTypeEnum.SCENARIO.value,
                    "prompt": f"When applying {title} in practice, what is the most critical constraint to balance?",
                    "options": [
                        "Performance vs Correctness Trade-offs",
                        "Ignoring edge-case failures",
                        "Hardcoding arbitrary constants",
                        "Removing all verification checks"
                    ],
                    "correct_answer": 0,
                    "explanation": "Engineering implementations always balance correctness with performance.",
                    "concept_id": cid,
                    "target_misconception": "Treating systems as single-variable optimizations",
                    "difficulty": 2
                }
            ]

        return {
            "id": f"quiz_{cid}",
            "concept_id": cid,
            "concept_title": title,
            "questions": questions,
            "pass_threshold": 75.0
        }

    @classmethod
    def evaluate_quiz_submission(
        cls,
        quiz: Dict[str, Any],
        user_answers: Dict[str, Any],
        concept: Dict[str, Any]
    ) -> Dict[str, Any]:
        questions = quiz.get("questions", [])
        evaluations = []
        correct_count = 0
        total_questions = len(questions)
        misconceptions = []
        weak_prereqs = []
        prerequisites = concept.get("prerequisites", [])

        for q in questions:
            qid = q["id"]
            user_ans = user_answers.get(qid)
            corr_ans = q["correct_answer"]
            
            if isinstance(corr_ans, list):
                if isinstance(user_ans, list):
                    is_correct = sorted(user_ans) == sorted(corr_ans)
                else:
                    is_correct = False
            else:
                is_correct = str(user_ans) == str(corr_ans)

            score = 1.0 if is_correct else 0.0
            if is_correct:
                correct_count += 1
            else:
                if q.get("target_misconception"):
                    misconceptions.append(q["target_misconception"])
                if "bit" in q.get("prompt", "").lower() or "mask" in q.get("prompt", "").lower():
                    if prerequisites:
                        weak_prereqs.append(prerequisites[0])

            evaluations.append({
                "question_id": qid,
                "is_correct": is_correct,
                "score": score,
                "user_answer": user_ans,
                "correct_answer": corr_ans,
                "explanation": q.get("explanation", ""),
                "misconception_detected": q.get("target_misconception") if not is_correct else None,
                "root_cause_prerequisite_id": weak_prereqs[0] if weak_prereqs and not is_correct else None
            })

        total_score = round((correct_count / total_questions) * 100.0, 1) if total_questions > 0 else 100.0
        passed = total_score >= quiz.get("pass_threshold", 75.0)

        if passed:
            next_action = "next_concept"
            feedback_summary = f"🎉 Outstanding! You demonstrated high conceptual mastery ({total_score}%). The next concept is now unlocked!"
            xp_earned = 100
        elif weak_prereqs:
            next_action = "reteach_prerequisite"
            feedback_summary = f"🔍 Diagnostic insight: Your errors stem from a foundational gap in prerequisite topic '{weak_prereqs[0]}'. Let's review that prerequisite first."
            xp_earned = 25
        else:
            next_action = "remediation"
            feedback_summary = f"⚠️ You scored {total_score}%. Let's walk through an adaptive re-teaching mode!"
            xp_earned = 30

        return {
            "quiz_id": quiz.get("id"),
            "concept_id": concept.get("id"),
            "total_score": total_score,
            "passed": passed,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "evaluations": evaluations,
            "feedback_summary": feedback_summary,
            "misconceptions": list(set(misconceptions)),
            "weak_prerequisites": list(set(weak_prereqs)),
            "next_action": next_action,
            "recommended_remediation": f"Review {concept.get('title')} using the Worked Example or Interactive Simulation style.",
            "updated_mastery": total_score if passed else max(concept.get("mastery_score", 0.0), total_score * 0.7),
            "xp_earned": xp_earned
        }
'''

files["backend/app/agents/adaptive_controller.py"] = '''from datetime import datetime, timedelta
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
'''

files["backend/app/agents/graph.py"] = '''from typing import Dict, Any
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
'''

files["backend/app/documents/parser.py"] = '''import os
from typing import List, Dict, Any

class DocumentParser:
    @staticmethod
    def parse_file(file_path: str, filename: str) -> Dict[str, Any]:
        ext = os.path.splitext(filename)[1].lower()
        text_content = ""
        sections = []

        if ext == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        sections.append({"section_title": f"Page {page_num + 1}", "content": page_text.strip()})
                text_content = "\\n\\n".join([s["content"] for s in sections])
            except Exception as e:
                text_content = f"PDF Error: {e}"
                sections = [{"section_title": "Overview", "content": text_content}]
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text_content = f.read()
            sections = [{"section_title": "Section 1", "content": text_content[:1500]}]

        return {"filename": filename, "total_chars": len(text_content), "sections": sections}
'''

files["backend/app/rag/vector_store.py"] = '''import math
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
'''

files["backend/app/youtube/analyzer.py"] = '''import re
from typing import Dict, Any, List

class YouTubeAnalyzer:
    @staticmethod
    def extract_video_id(url: str) -> str:
        pattern = r"(?:v=|\\/)([0-9A-Za-z_-]{11}).*"
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
'''

files["backend/app/api/courses.py"] = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.database.connection import get_db
from backend.app.database.models import CourseModel, ConceptModel, UserModel
from backend.app.schemas.schemas import CreateCourseRequest
from backend.app.services.llm_service import LLMService
from backend.app.agents.graph import LearnGraphOrchestrator
from backend.app.agents.adaptive_controller import AdaptiveController

router = APIRouter(prefix="/api/courses", tags=["courses"])
llm_service = LLMService()
orchestrator = LearnGraphOrchestrator(llm_service)

@router.post("", response_model=Dict[str, Any])
async def create_course(req: CreateCourseRequest, db: Session = Depends(get_db)):
    title = req.title or (req.source_content[:40] if len(req.source_content) > 3 else "New Learning Journey")
    initial_state = {
        "course_id": "temp",
        "source_type": req.source_type,
        "source_content": req.source_content,
        "learning_goal": req.learning_goal.value,
        "current_level": req.current_level.value,
        "study_time_hours": req.study_time_hours_per_week or 5,
        "preferred_style": req.preferred_style.value if req.preferred_style else "simple",
        "topic": "",
        "scope": "",
        "concepts": [],
        "prerequisites_map": {},
        "knowledge_graph": {},
        "roadmap": {},
        "active_concept_id": None,
        "current_lesson": None,
        "current_quiz": None,
        "quiz_submission": None,
        "evaluation_result": None,
        "remediation_required": False,
        "weak_prerequisite_id": None,
        "next_recommended_concept_id": None,
        "learner_mastery_updates": {}
    }

    result_state = await orchestrator.run_initial_course_pipeline(initial_state)

    db_course = CourseModel(
        title=result_state["topic"] or title,
        source_type=req.source_type,
        source_content=req.source_content,
        source_summary=result_state["scope"],
        learning_goal=req.learning_goal.value,
        current_level=req.current_level.value,
        study_time_hours_per_week=req.study_time_hours_per_week or 5,
        preferred_style=req.preferred_style.value if req.preferred_style else "simple",
        knowledge_graph_data=result_state["knowledge_graph"],
        roadmap_data=result_state["roadmap"],
        user_id=req.user_id or "demo_user"
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    for c in result_state["concepts"]:
        db_concept = ConceptModel(
            id=c["id"],
            course_id=db_course.id,
            title=c["title"],
            short_summary=c.get("short_summary", ""),
            difficulty=c.get("difficulty", 2),
            importance=c.get("importance", 4),
            estimated_minutes=c.get("estimated_minutes", 20),
            status=c.get("status", "locked"),
            mastery_score=c.get("mastery_score", 0.0),
            prerequisites=c.get("prerequisites", []),
            learning_objectives=c.get("learning_objectives", []),
            common_misconceptions=c.get("common_misconceptions", []),
            source_references=c.get("source_references", [])
        )
        db.add(db_concept)
    db.commit()

    return {
        "id": db_course.id,
        "title": db_course.title,
        "source_summary": db_course.source_summary,
        "knowledge_graph": result_state["knowledge_graph"],
        "roadmap": result_state["roadmap"],
        "concepts_count": len(result_state["concepts"])
    }

@router.get("", response_model=List[Dict[str, Any]])
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(CourseModel).order_by(CourseModel.created_at.desc()).all()
    results = []
    for c in courses:
        roadmap = c.roadmap_data or {}
        results.append({
            "id": c.id,
            "title": c.title,
            "source_type": c.source_type,
            "learning_goal": c.learning_goal,
            "progress_percentage": roadmap.get("progress_percentage", 0.0),
            "total_concepts": len(c.concepts),
            "created_at": c.created_at.strftime("%b %d, %Y")
        })
    return results

@router.get("/{course_id}")
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    concepts_data = [
        {
            "id": c.id,
            "title": c.title,
            "short_summary": c.short_summary,
            "difficulty": c.difficulty,
            "importance": c.importance,
            "estimated_minutes": c.estimated_minutes,
            "status": c.status,
            "mastery_score": c.mastery_score,
            "prerequisites": c.prerequisites or [],
            "learning_objectives": c.learning_objectives or [],
            "common_misconceptions": c.common_misconceptions or []
        }
        for c in course.concepts
    ]

    revision_schedule = AdaptiveController.compute_spaced_repetition_schedule(concepts_data)
    mastered = sum(1 for c in concepts_data if c["status"] == "mastered")
    total = len(concepts_data)

    mastery_profile = {
        "overall_mastery": round((mastered / total) * 100.0, 1) if total > 0 else 0.0,
        "concepts_mastered": mastered,
        "concepts_in_progress": sum(1 for c in concepts_data if c["status"] == "learning"),
        "concepts_locked": sum(1 for c in concepts_data if c["status"] == "locked"),
        "total_concepts": total,
        "concept_scores": {c["id"]: c["mastery_score"] for c in concepts_data},
        "strongest_concepts": [c["title"] for c in concepts_data if c["mastery_score"] >= 80.0],
        "weakest_concepts": [c["title"] for c in concepts_data if c["status"] == "needs_review" or (c["mastery_score"] < 60 and c["mastery_score"] > 0)],
        "recent_accuracy": 88.5,
        "streak_days": 4,
        "total_xp": 450,
        "level": 2
    }

    return {
        "id": course.id,
        "title": course.title,
        "source_type": course.source_type,
        "source_summary": course.source_summary,
        "learning_goal": course.learning_goal,
        "current_level": course.current_level,
        "created_at": course.created_at.strftime("%b %d, %Y"),
        "concepts": concepts_data,
        "knowledge_graph": course.knowledge_graph_data,
        "roadmap": course.roadmap_data,
        "mastery_profile": mastery_profile,
        "revision_schedule": revision_schedule
    }

@router.get("/{course_id}/roadmap")
def get_roadmap(course_id: str, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.roadmap_data

@router.post("/{course_id}/final-test")
def generate_final_test(course_id: str, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    final_questions = []
    for idx, c in enumerate(course.concepts):
        final_questions.append({
            "id": f"final_q_{idx+1}",
            "type": "scenario",
            "prompt": f"Comprehensive Synthesis [{c.title}]: A system engineer reports high latency during peak hours. How does the architecture of {c.title} resolve or mitigate this failure mode?",
            "options": [
                f"Apply optimized caching, proper resource partitioning, and verify state boundaries of {c.title}",
                "Terminate the entire server instance and restart from cold boot",
                "Disable all security checks and memory limits completely",
                "None of the above"
            ],
            "correct_answer": 0,
            "explanation": f"Optimal engineering demands applying the core mechanisms of {c.title}.",
            "concept_id": c.id,
            "difficulty": 4
        })

    return {
        "id": f"final_test_{course_id}",
        "course_id": course_id,
        "course_title": course.title,
        "total_questions": len(final_questions),
        "pass_threshold": 80.0,
        "questions": final_questions
    }
'''

files["backend/app/api/concepts.py"] = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import ConceptModel

router = APIRouter(prefix="/api/concepts", tags=["concepts"])

@router.get("/{concept_id}")
def get_concept(concept_id: str, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return {
        "id": concept.id,
        "course_id": concept.course_id,
        "title": concept.title,
        "short_summary": concept.short_summary,
        "difficulty": concept.difficulty,
        "importance": concept.importance,
        "estimated_minutes": concept.estimated_minutes,
        "status": concept.status,
        "mastery_score": concept.mastery_score,
        "prerequisites": concept.prerequisites or [],
        "learning_objectives": concept.learning_objectives or [],
        "common_misconceptions": concept.common_misconceptions or []
    }
'''

files["backend/app/api/lessons.py"] = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import ConceptModel
from backend.app.schemas.schemas import GenerateLessonRequest, TeachingModeEnum
from backend.app.services.llm_service import LLMService
from backend.app.agents.lesson_generator import LessonGeneratorAgent
from backend.app.rag.vector_store import global_vector_store

router = APIRouter(prefix="/api/lessons", tags=["lessons"])
llm_service = LLMService()
lesson_agent = LessonGeneratorAgent(llm_service)

@router.post("/{concept_id}/generate")
async def generate_lesson(concept_id: str, req: GenerateLessonRequest = GenerateLessonRequest(), db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    retrieved_chunks = global_vector_store.search(query=concept.title, course_id=concept.course_id, top_k=2)
    context_str = "\\n".join([f"[{c['section_title']}]: {c['content']}" for c in retrieved_chunks]) if retrieved_chunks else None

    concept_dict = {
        "id": concept.id,
        "title": concept.title,
        "prerequisites": concept.prerequisites or [],
        "learning_objectives": concept.learning_objectives or [],
        "common_misconceptions": concept.common_misconceptions or []
    }
    mode = req.mode or TeachingModeEnum.SIMPLE
    return await lesson_agent.generate_lesson(concept_dict, mode, context_str)
'''

files["backend/app/api/quizzes.py"] = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import ConceptModel, CourseModel, UserModel
from backend.app.schemas.schemas import SubmitQuizRequest
from backend.app.agents.quiz_evaluator import QuizEvaluatorAgent
from backend.app.agents.adaptive_controller import AdaptiveController

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])

@router.get("/{concept_id}")
def get_quiz_for_concept(concept_id: str, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return QuizEvaluatorAgent.generate_quiz_for_concept({"id": concept.id, "title": concept.title, "prerequisites": concept.prerequisites or []})

@router.post("/{concept_id}/submit")
def submit_quiz(concept_id: str, req: SubmitQuizRequest, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    course = db.query(CourseModel).filter(CourseModel.id == concept.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    concept_dict = {"id": concept.id, "title": concept.title, "prerequisites": concept.prerequisites or [], "mastery_score": concept.mastery_score}
    quiz_data = QuizEvaluatorAgent.generate_quiz_for_concept(concept_dict)
    evaluation_result = QuizEvaluatorAgent.evaluate_quiz_submission(quiz_data, req.answers, concept_dict)

    adaptation = AdaptiveController.update_graph_after_evaluation(
        knowledge_graph=course.knowledge_graph_data or {},
        roadmap=course.roadmap_data or {},
        concept_id=concept_id,
        evaluation_result=evaluation_result
    )

    concept.mastery_score = evaluation_result["updated_mastery"]
    concept.status = "mastered" if evaluation_result["passed"] else "needs_review"

    for node in adaptation["knowledge_graph"].get("nodes", []):
        db_c = db.query(ConceptModel).filter(ConceptModel.id == node["id"]).first()
        if db_c:
            db_c.status = node["data"]["status"]
            db_c.mastery_score = node["data"]["mastery_score"]

    course.knowledge_graph_data = adaptation["knowledge_graph"]
    course.roadmap_data = adaptation["roadmap"]

    user = db.query(UserModel).filter(UserModel.id == "demo_user").first()
    if user:
        user.xp += evaluation_result.get("xp_earned", 50)
        user.level = max(1, user.xp // 250 + 1)
    db.commit()

    return {
        "evaluation": evaluation_result,
        "updated_knowledge_graph": course.knowledge_graph_data,
        "updated_roadmap": course.roadmap_data
    }
'''

files["backend/app/api/tutor.py"] = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import CourseModel, ConceptModel
from backend.app.schemas.schemas import ChatTutorRequest
from backend.app.services.llm_service import LLMService
from backend.app.rag.vector_store import global_vector_store

router = APIRouter(prefix="/api/tutor", tags=["tutor"])
llm_service = LLMService()

@router.post("/chat")
async def chat_with_tutor(req: ChatTutorRequest, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == req.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    concept_title = "Overall Course"
    if req.concept_id:
        concept = db.query(ConceptModel).filter(ConceptModel.id == req.concept_id).first()
        if concept:
            concept_title = concept.title

    retrieved_chunks = global_vector_store.search(query=req.message, course_id=req.course_id, top_k=2)
    sources_cited = [c["section_title"] for c in retrieved_chunks]
    context_text = "\\n".join([f"[{c['section_title']}]: {c['content']}" for c in retrieved_chunks])

    system_prompt = f"Subject: {course.title}, Active Concept: {concept_title}. Context: {context_text or 'Standard curriculum'}. Mode: {req.mode}"
    ai_response = await llm_service.generate_text(f"Learner: {req.message}", system_prompt)

    if ai_response.startswith("I am LearnGraph AI Tutor"):
        ai_response = f"Great question regarding **{concept_title}**! Let's break this down:\\n\\n1. **Core Intuition**: {concept_title} ensures consistent boundaries and deterministic allocation.\\n2. **Check**: Consider how hardware registers map directly to these abstractions.\\n\\nWould you like an analogy, a worked example, or a quick check question?"

    return {
        "reply": ai_response,
        "concept_id": req.concept_id,
        "concept_title": concept_title,
        "sources_cited": sources_cited
    }
'''

files["backend/app/api/documents.py"] = '''import os, shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import DocumentModel, DocumentChunkModel, CourseModel
from backend.app.documents.parser import DocumentParser
from backend.app.rag.vector_store import global_vector_store

router = APIRouter(prefix="/api/documents", tags=["documents"])
UPLOAD_DIR = "./uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(course_id: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed = DocumentParser.parse_file(file_path, file.filename)
    sections = parsed.get("sections", [])

    db_doc = DocumentModel(course_id=course_id, filename=file.filename, file_type=file.content_type or "application/octet-stream", file_size=os.path.getsize(file_path))
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    for idx, s in enumerate(sections):
        db.add(DocumentChunkModel(document_id=db_doc.id, chunk_index=idx, section_title=s.get("section_title", f"Chunk {idx+1}"), content=s.get("content", "")))
    db.commit()

    global_vector_store.add_chunks(course_id, db_doc.id, sections)
    return {"document_id": db_doc.id, "filename": file.filename, "total_sections": len(sections), "status": "indexed_in_rag"}
'''

files["backend/app/api/sources.py"] = '''from fastapi import APIRouter
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
'''

files["backend/app/api/resources.py"] = '''from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.database.connection import get_db
from backend.app.database.models import ConceptModel
from backend.app.youtube.analyzer import YouTubeAnalyzer

router = APIRouter(prefix="/api/resources", tags=["resources"])

@router.get("/{concept_id}", response_model=List[Dict[str, Any]])
def get_curated_resources(concept_id: str, db: Session = Depends(get_db)):
    concept = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    title = concept.title
    coverage_info = YouTubeAnalyzer.analyze_coverage("https://www.youtube.com/watch?v=demo", title, concept.learning_objectives or [])
    return [
        {
            "id": f"res_vid_1_{concept_id}",
            "title": f"Mastering {title}: Complete In-Depth Walkthrough",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "type": "video",
            "duration_or_read_time": "18 mins",
            "difficulty": "Intermediate",
            "relevance_score": 96,
            "covered_topics": coverage_info["covered_topics"],
            "missing_topics": coverage_info["missing_topics"],
            "coverage_percentage": coverage_info["coverage_percentage"]
        },
        {
            "id": f"res_practice_1_{concept_id}",
            "title": f"Interactive Sandbox & Practice Lab: {title}",
            "url": "#simulation",
            "type": "practice",
            "duration_or_read_time": "15 mins active",
            "difficulty": "Applied",
            "relevance_score": 99,
            "covered_topics": ["Hands-on simulation", "State transitions"],
            "missing_topics": [],
            "coverage_percentage": 100
        }
    ]
'''

files["backend/app/api/simulations.py"] = '''from fastapi import APIRouter
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
'''

files["backend/app/api/analytics.py"] = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import CourseModel, UserModel, ConceptModel
from backend.app.agents.adaptive_controller import AdaptiveController

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard")
def get_user_dashboard(user_id: str = "demo_user", db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        user = UserModel(id="demo_user", name="Alex Learner", xp=450, level=2, streak_days=4)
        db.add(user)
        db.commit()
        db.refresh(user)

    courses = db.query(CourseModel).filter(CourseModel.user_id == user_id).all()
    all_concepts = db.query(ConceptModel).all()

    total_concepts = len(all_concepts)
    mastered_concepts = sum(1 for c in all_concepts if c.status == "mastered")
    overall_mastery = round((mastered_concepts / total_concepts) * 100.0, 1) if total_concepts > 0 else 0.0

    concepts_data = [{"id": c.id, "title": c.title, "difficulty": c.difficulty, "importance": c.importance, "mastery_score": c.mastery_score, "status": c.status} for c in all_concepts]
    spaced_schedule = AdaptiveController.compute_spaced_repetition_schedule(concepts_data)

    return {
        "user": {
            "id": user.id, "name": user.name, "email": user.email, "xp": user.xp, "level": user.level, "streak_days": user.streak_days,
            "badges": [
                {"id": "b1", "name": "Concept Pioneer", "icon": "🚀", "description": "Created first interactive learning journey"},
                {"id": "b2", "name": "Deep Thinker", "icon": "🧠", "description": "Resolved a subtle root-cause misconception"},
                {"id": "b3", "name": "Simulation Master", "icon": "⚡", "description": "Completed hands-on MMU & CPU scheduler simulations"}
            ]
        },
        "stats": {
            "overall_mastery": overall_mastery,
            "total_courses": len(courses),
            "total_concepts": total_concepts,
            "mastered_concepts": mastered_concepts,
            "in_progress_concepts": sum(1 for c in all_concepts if c.status in ["learning", "available"]),
            "needs_review_concepts": sum(1 for c in all_concepts if c.status == "needs_review"),
            "learning_velocity_hours_this_week": 4.5,
            "average_quiz_accuracy": 91.2
        },
        "revision_schedule": spaced_schedule,
        "weekly_activity": [
            {"day": "Mon", "minutes": 45, "concepts": 2},
            {"day": "Tue", "minutes": 60, "concepts": 3},
            {"day": "Wed", "minutes": 30, "concepts": 1},
            {"day": "Thu", "minutes": 55, "concepts": 2},
            {"day": "Fri", "minutes": 40, "concepts": 2},
            {"day": "Sat", "minutes": 70, "concepts": 4},
            {"day": "Sun", "minutes": 25, "concepts": 1}
        ]
    }
'''

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
print(f"Successfully generated {len(files)} files!")


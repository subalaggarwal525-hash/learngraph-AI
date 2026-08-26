import os
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
                    contents=f"{system_prompt}\n\nTask:\n{prompt}\n\nRespond ONLY with valid JSON conforming to the requested structure."
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
                    contents=f"{system_prompt}\n\n{prompt}"
                )
                return response.text
            except Exception as e:
                logger.warning(f"Gemini text generation failed: {e}")
        return "I am LearnGraph AI Tutor. I can explain this concept, break down prerequisites, or guide you through practice exercises."

    def _generate_structured_fallback(self, prompt: str, schema_name: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        is_os = any(k in prompt_lower for k in ["operating system", "os", "process", "memory", "paging", "thread", "virtual memory", "scheduling", "deadlock", "cpu"])
        is_dsa = any(k in prompt_lower for k in ["data structure", "algorithm", "sorting", "tree", "graph", "array", "binary search", "dsa", "stack", "queue", "hash"])
        is_ml = any(k in prompt_lower for k in ["machine learning", "neural", "deep learning", "ai", "transformer", "gradient", "regression", "classification", "llm"])
        is_web = any(k in prompt_lower for k in ["react", "javascript", "web", "http", "api", "css", "html", "frontend", "backend", "database", "sql"])

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
                    "scope": "Master core algorithmic problem solving, time complexity, linear and tree structures, and dynamic programming.",
                    "concepts": [
                        {
                            "id": "c_asymptotic_analysis",
                            "title": "Asymptotic Analysis & Big-O Notation",
                            "short_summary": "Formal mathematical frameworks to calculate worst, average, and amortized runtimes.",
                            "difficulty": 1,
                            "importance": 5,
                            "estimated_minutes": 20,
                            "prerequisites": [],
                            "learning_objectives": ["Classify complexity classes from $O(1)$ to $O(2^n)$", "Analyze loops and recursive relations"],
                            "common_misconceptions": ["Confusing Big-O with exact execution seconds"],
                            "source_references": ["Ch. 1: Complexity Theory"],
                            "status": "available",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_arrays_pointers",
                            "title": "Contiguous Memory & Two-Pointer Patterns",
                            "short_summary": "Cache locality, array indexing mathematics, and two-pointer traversal strategies.",
                            "difficulty": 2,
                            "importance": 4,
                            "estimated_minutes": 25,
                            "prerequisites": ["c_asymptotic_analysis"],
                            "learning_objectives": ["Master opposite and fast-slow pointer techniques", "Leverage memory cache lines for sequential traversal"],
                            "common_misconceptions": ["Assuming dynamic arrays have $O(n)$ insertion cost for every single element"],
                            "source_references": ["Ch. 2: Arrays & Memory"],
                            "status": "locked",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_sorting_algorithms",
                            "title": "Sorting Paradigms & Divide-and-Conquer",
                            "short_summary": "MergeSort, QuickSort, partition invariants, and comparison lower bound proofs.",
                            "difficulty": 3,
                            "importance": 5,
                            "estimated_minutes": 30,
                            "prerequisites": ["c_arrays_pointers"],
                            "learning_objectives": ["Prove $O(n \\log n)$ comparison bound", "Implement in-place partitioning without memory leakage"],
                            "common_misconceptions": ["Assuming QuickSort always runs in $O(n \\log n)$ without randomized pivots"],
                            "source_references": ["Ch. 4: Sorting & Order Statistics"],
                            "status": "locked",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_binary_trees",
                            "title": "Binary Trees & Graph Traversals (BFS/DFS)",
                            "short_summary": "Hierarchical state trees, recursion stacks, breadth-first queues, and topological sorting.",
                            "difficulty": 4,
                            "importance": 5,
                            "estimated_minutes": 35,
                            "prerequisites": ["c_sorting_algorithms"],
                            "learning_objectives": ["Traverse recursive tree structures iteratively", "Detect cycles using graph coloring"],
                            "common_misconceptions": ["Assuming recursion never exceeds call-stack limits on deep trees"],
                            "source_references": ["Ch. 6: Graph Algorithms"],
                            "status": "locked",
                            "mastery_score": 0.0
                        }
                    ]
                }
            elif is_ml:
                return {
                    "topic": "Machine Learning & Neural Architectures",
                    "scope": "Foundations of mathematical optimization, loss functions, backpropagation, and deep transformer models.",
                    "concepts": [
                        {
                            "id": "c_linear_algebra_opt",
                            "title": "Linear Algebra & Gradient Descent",
                            "short_summary": "Vectors, matrices, dot products, loss gradients, and learning rate schedules.",
                            "difficulty": 1,
                            "importance": 5,
                            "estimated_minutes": 20,
                            "prerequisites": [],
                            "learning_objectives": ["Compute gradients of multivariate loss functions", "Implement mini-batch stochastic gradient descent"],
                            "common_misconceptions": ["Believing higher learning rates always converge faster"],
                            "source_references": ["Foundations of Deep Learning"],
                            "status": "available",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_neural_backprop",
                            "title": "Feedforward Networks & Backpropagation",
                            "short_summary": "Multi-layer perceptrons, activation functions (ReLU, GELU), and reverse-mode automatic differentiation.",
                            "difficulty": 3,
                            "importance": 5,
                            "estimated_minutes": 30,
                            "prerequisites": ["c_linear_algebra_opt"],
                            "learning_objectives": ["Derive chain rule for matrix backpropagation", "Mitigate vanishing and exploding gradients"],
                            "common_misconceptions": ["Assuming linear activations can model non-linear boundaries"],
                            "source_references": ["Deep Learning Architectures"],
                            "status": "locked",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_attention_transformers",
                            "title": "Self-Attention & Transformer Architecture",
                            "short_summary": "Scaled dot-product attention, multi-head projections, positional encoding, and KV caching.",
                            "difficulty": 4,
                            "importance": 5,
                            "estimated_minutes": 40,
                            "prerequisites": ["c_neural_backprop"],
                            "learning_objectives": ["Calculate $QK^T / \\sqrt{d_k}$ attention weights", "Understand causal masking in autoregressive LLMs"],
                            "common_misconceptions": ["Confusing cross-attention with self-attention mechanisms"],
                            "source_references": ["Attention Is All You Need (Vaswani et al.)"],
                            "status": "locked",
                            "mastery_score": 0.0
                        }
                    ]
                }
            else:
                base_title = prompt.split("Source material:")[0].replace("Analyze the following learning request: ", "").replace("Analyze:", "").strip()[:45] or "Core Discipline"
                return {
                    "topic": base_title,
                    "scope": f"First-principles breakdown, structural mechanisms, applied workflows, and advanced integration of {base_title}.",
                    "concepts": [
                        {
                            "id": "c_foundations",
                            "title": f"{base_title}: Foundations & Core Terminology",
                            "short_summary": f"Fundamental definitions, essential axioms, and initial principles underpinning {base_title}.",
                            "difficulty": 1,
                            "importance": 5,
                            "estimated_minutes": 15,
                            "prerequisites": [],
                            "learning_objectives": [f"Define primary concepts in {base_title}", "Understand the foundational mental model"],
                            "common_misconceptions": ["Assuming foundational terms are interchangeable without strict boundaries"],
                            "source_references": [f"Module 1: Principles of {base_title}"],
                            "status": "available",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_mechanisms",
                            "title": f"{base_title}: Operational Mechanics & Interactions",
                            "short_summary": f"How component subsystems communicate, state transitions occur, and constraints are enforced in {base_title}.",
                            "difficulty": 2,
                            "importance": 5,
                            "estimated_minutes": 25,
                            "prerequisites": ["c_foundations"],
                            "learning_objectives": ["Trace data and state flows across components", "Analyze error conditions and edge cases"],
                            "common_misconceptions": ["Ignoring side effects during state changes"],
                            "source_references": [f"Module 2: Mechanics of {base_title}"],
                            "status": "locked",
                            "mastery_score": 0.0
                        },
                        {
                            "id": "c_applied_architecture",
                            "title": f"{base_title}: Applied Design & Real-World Optimization",
                            "short_summary": f"Architecting production-grade workflows, mitigating failure modes, and benchmarking trade-offs in {base_title}.",
                            "difficulty": 3,
                            "importance": 4,
                            "estimated_minutes": 30,
                            "prerequisites": ["c_mechanisms"],
                            "learning_objectives": ["Synthesize end-to-end solutions under trade-off constraints", "Diagnose bottlenecks and failure patterns"],
                            "common_misconceptions": ["Over-optimizing premature execution paths before verifying invariants"],
                            "source_references": [f"Module 3: Advanced {base_title}"],
                            "status": "locked",
                            "mastery_score": 0.0
                        }
                    ]
                }

        elif schema_name == "lesson":
            # Extract concept title from prompt if available
            concept_title = "Active Concept"
            if "Concept:" in prompt:
                concept_title = prompt.split("Concept:")[1].split(",")[0].strip()

            c_lower = concept_title.lower()
            if any(k in c_lower for k in ["paging", "memory", "frame", "virtual"]):
                return {
                    "learning_objective": "Understand how the CPU and OS collaborate using hardware Page Tables and TLBs to translate 32-bit virtual addresses into physical RAM frames without fragmentation.",
                    "prerequisite_reminder": "Recall that physical RAM is byte-addressable hardware, while virtual addresses are software abstractions granted per process.",
                    "simple_explanation": "Memory management creates the illusion of an isolated, continuous memory workspace for every executing program. Under the hood, memory is split into fixed chunks: **Pages** in virtual space, and **Frames** in physical RAM.",
                    "detailed_explanation": "When an instruction requests virtual address `0x00403010`, the Memory Management Unit (MMU) extracts the **Virtual Page Number (VPN)** and the **Offset**. It queries the high-speed Translation Lookaside Buffer (TLB). On a TLB hit, the translation finishes in sub-nanoseconds. On a miss, the MMU walks the multi-level Page Table in RAM, identifies physical frame `0x0812`, and generates the target physical address `0x0812010`.",
                    "analogy": "Consider an airport luggage claim: You hold baggage ticket #403 (Virtual Page). The terminal conveyor system maps ticket #403 to cargo bay rack B-12 (Physical Frame). You only ever need your ticket; the airport manages the physical warehouse layout.",
                    "worked_example": "Given 32-bit address `0x00403010` and 4KB ($2^{12}$ bytes) page size:\n- Offset bits = $12$ bits (`0x010`)\n- Virtual Page Number (VPN) = $32 - 12 = 20$ bits (`0x00403`)\n- Page Table lookup: VPN `0x00403` $\\rightarrow$ Frame `0x0812`\n- Physical Address: $(\\text{0x0812} \\ll 12) \\mid \\text{0x010} = \\text{0x0812010}$",
                    "common_mistakes": [
                        "Confusing Virtual Page Numbers (VPN) with Physical Frame Numbers (PFN)",
                        "Believing that physical RAM must allocate continuous sequential blocks for a program"
                    ],
                    "key_takeaways": [
                        "Virtual Pages map to Physical Frames via Page Tables.",
                        "TLB caches accelerate translation from ~50ns to ~0.5ns.",
                        "If a page table entry valid bit is 0, the CPU raises a Page Fault interrupt to fetch data from swap disk."
                    ],
                    "quick_checks": [
                        {
                            "question": "In a system with 4KB ($2^{12}$ B) pages and a 32-bit address space, how many bits are used for the page offset?",
                            "options": ["8 bits", "10 bits", "12 bits", "16 bits"],
                            "correct_index": 2,
                            "explanation": "Because each page holds $2^{12} = 4096$ bytes, 12 bits are required to index every byte within that page."
                        }
                    ],
                    "deeper_dive": "Hierarchical multi-level page tables ensure sparse memory allocations don't waste millions of empty page table entries in physical RAM.",
                    "source_citations": ["Operating Systems: Three Easy Pieces (OSTEP)", "Computer Systems: A Programmer's Perspective (CS:APP)"],
                    "simulation_type": "memory_paging"
                }
            elif any(k in c_lower for k in ["process", "thread", "scheduling", "cpu"]):
                return {
                    "learning_objective": f"Master the architectural lifecycle, context-switching overhead, and synchronization primitives of {concept_title}.",
                    "prerequisite_reminder": "Processes possess separate memory spaces; threads share a common heap within the same process container.",
                    "simple_explanation": f"{concept_title} dictates how the operating system coordinates execution units across physical CPU cores to maximize throughput and minimize latency.",
                    "detailed_explanation": "During a context switch, the OS saves the Process Control Block (PCB) including register values, program counter ($PC$), and stack pointer ($SP$). It switches the memory page directory base register ($CR3$ on x86) and dispatches the highest priority thread from the Ready Queue.",
                    "analogy": "A professional chef (CPU core) switching between cooking multiple recipes. When sauce is simmering (I/O Wait), the chef bookmarks the recipe notebook (PCB context) and starts chopping onions for another dish (Ready Queue).",
                    "worked_example": "Round-Robin scheduling trace with time quantum $q = 10ms$:\n- $P_1$ (burst 25ms), $P_2$ (burst 8ms)\n- $t=0..8ms$: $P_2$ finishes completely\n- $t=8..18ms$: $P_1$ runs for 10ms, preempted to Ready Queue\n- Average turnaround time = $\\frac{8 + 33}{2} = 20.5ms$",
                    "common_mistakes": [
                        "Assuming blocked processes consume CPU execution cycles",
                        "Forgetting that thread context switches are faster because memory mappings remain unchanged"
                    ],
                    "key_takeaways": [
                        "The 5-state model: New $\\rightarrow$ Ready $\\rightarrow$ Running $\\rightarrow$ Waiting $\\rightarrow$ Terminated.",
                        "Context switching incurs cache invalidation and TLB flush penalties."
                    ],
                    "quick_checks": [
                        {
                            "question": "What state does a process enter when it initiates a disk read operation?",
                            "options": ["Running", "Ready", "Waiting / Blocked", "Terminated"],
                            "correct_index": 2,
                            "explanation": "I/O operations are handled asynchronously by hardware controllers; the process is placed in the Waiting state so the CPU can execute other ready processes."
                        }
                    ],
                    "deeper_dive": "Completely Fair Scheduler (CFS) in Linux uses red-black trees to balance virtual runtime ($vruntime$) across threads.",
                    "source_citations": ["Modern Operating Systems (Tanenbaum)", "Linux Kernel Development (Robert Love)"],
                    "simulation_type": "cpu_scheduling"
                }
            elif any(k in c_lower for k in ["sort", "algorithm", "big-o", "tree", "array"]):
                return {
                    "learning_objective": f"Analyze the time/space complexity invariants and algorithmic correctness of {concept_title}.",
                    "prerequisite_reminder": "Review asymptotic bounds: $O(g(n))$ represents the upper bound as $n \\to \\infty$.",
                    "simple_explanation": f"{concept_title} provides systematic, mathematically proven procedures to organize data and optimize computational searches.",
                    "detailed_explanation": "By leveraging divide-and-conquer recurrences $T(n) = 2T(n/2) + O(n)$, comparison-based sorts partition problem instances recursively until reaching base cases, achieving the proven theoretical optimal bound of $O(n \\log n)$.",
                    "analogy": "Organizing an unsorted library: Instead of scanning every shelf randomly, splitting the books into two halves (A-M and N-Z) recursively halves your sorting search space at every step.",
                    "worked_example": "Recurrence Master Theorem evaluation:\n$$T(n) = 2T(n/2) + n$$\n- $a = 2, b = 2, f(n) = n$\n- Critical exponent: $\\log_b a = \\log_2 2 = 1$\n- Since $f(n) = \\Theta(n^1)$, Case 2 applies: $T(n) = \\Theta(n \\log n)$",
                    "common_mistakes": [
                        "Assuming $O(n \\log n)$ algorithms are always faster than $O(n^2)$ algorithms for tiny input sizes ($n < 10$)",
                        "Overlooking auxiliary memory allocations in non-in-place algorithms"
                    ],
                    "key_takeaways": [
                        "Divide-and-conquer reduces polynomial search spaces logarithmically.",
                        "Worst-case vs average-case behavior can diverge based on pivot selection."
                    ],
                    "quick_checks": [
                        {
                            "question": "What is the optimal comparison-based sorting time complexity lower bound?",
                            "options": ["O(n)", "O(n log n)", "O(log n)", "O(n^2)"],
                            "correct_index": 1,
                            "explanation": "Decision tree height for sorting $n!$ permutations is $\\lceil \\log_2(n!) \\rceil = \\Omega(n \\log n)$."
                        }
                    ],
                    "deeper_dive": "TimSort combines MergeSort and InsertionSort to exploit pre-existing natural ordering (runs) in real-world data.",
                    "source_citations": ["Introduction to Algorithms (CLRS)", "The Art of Computer Programming (Knuth)"],
                    "simulation_type": "sorting"
                }
            else:
                return {
                    "learning_objective": f"Develop deep first-principles intuition, structural mechanisms, and applied mastery of {concept_title}.",
                    "prerequisite_reminder": "Verify foundational terms and operational prerequisites before proceeding into advanced trade-offs.",
                    "simple_explanation": f"At its core, **{concept_title}** establishes rules and structures that turn complex problems into reliable, repeatable, and scalable patterns.",
                    "detailed_explanation": f"Understanding {concept_title} requires separating the abstract interface from the underlying execution mechanics. By analyzing inputs, state transitions, and expected outputs, you can systematically diagnose failures and optimize efficiency.",
                    "analogy": f"Think of {concept_title} like a precision clockwork mechanism: every gear has a defined boundary, and together they maintain synchronization without unpredictable side effects.",
                    "worked_example": f"Applying {concept_title} Step-by-Step:\n1. Identify invariant constraints and boundary conditions.\n2. Execute the primary state transformation.\n3. Validate the post-condition result against expected thresholds.",
                    "common_mistakes": [
                        "Skipping boundary condition checks during initialization",
                        "Treating symptoms of errors rather than addressing underlying mental model flaws"
                    ],
                    "key_takeaways": [
                        f"{concept_title} ensures consistency and robust execution.",
                        "Always test edge cases and verify invariants before deployment."
                    ],
                    "quick_checks": [
                        {
                            "question": f"What is the most critical first step when analyzing a problem in {concept_title}?",
                            "options": [
                                "Identify core invariants and boundary conditions",
                                "Write arbitrary code immediately without a plan",
                                "Ignore all prerequisite relationships",
                                "Assume perfect deterministic hardware execution"
                            ],
                            "correct_index": 0,
                            "explanation": "Identifying boundary constraints and invariants establishes the foundation needed to design robust solutions."
                        }
                    ],
                    "deeper_dive": f"Advanced practitioners evaluate trade-offs between computational overhead and architectural maintainability when implementing {concept_title}.",
                    "source_citations": [f"Principles of Modern {concept_title}", "Foundational Engineering Best Practices"],
                    "simulation_type": None
                }

        return {}

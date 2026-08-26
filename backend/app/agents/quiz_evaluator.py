from typing import Dict, Any, List
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

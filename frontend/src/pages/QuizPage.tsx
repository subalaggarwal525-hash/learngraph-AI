import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import { HelpCircle, CheckCircle2, AlertTriangle, Sparkles, ArrowRight, RotateCcw, Zap, Gauge, Check, X } from 'lucide-react';
import { useCourse } from '../context/CourseContext';
import { quizApi } from '../services/api';
import { Quiz, QuizEvaluationResult } from '../types';

export const QuizPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, activeConceptId, refreshCourse, addXP } = useCourse();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, any>>({});
  const [confidenceRatings, setConfidenceRatings] = useState<Record<string, 'low' | 'medium' | 'high'>>({});
  const [evaluation, setEvaluation] = useState<QuizEvaluationResult | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const activeConcept = (activeCourse?.concepts || []).find((c) => c.id === activeConceptId) || activeCourse?.concepts?.[0];

  useEffect(() => {
    const fetchQuiz = async () => {
      if (!activeConcept) return;
      setIsLoading(true);
      setEvaluation(null);
      setSelectedAnswers({});
      setConfidenceRatings({});
      try {
        const quizData = await quizApi.getQuiz(activeConcept.id);
        setQuiz(quizData);
      } catch (err) {
        console.error('Quiz load error:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchQuiz();
  }, [activeConcept?.id]);

  const handleSelectOption = (questionId: string, optionIndex: number, isMulti: boolean) => {
    if (evaluation) return;
    if (isMulti) {
      const currentList: number[] = selectedAnswers[questionId] || [];
      const updated = currentList.includes(optionIndex) ? currentList.filter((i) => i !== optionIndex) : [...currentList, optionIndex];
      setSelectedAnswers({ ...selectedAnswers, [questionId]: updated });
    } else {
      setSelectedAnswers({ ...selectedAnswers, [questionId]: optionIndex });
    }
  };

  const setConfidence = (questionId: string, level: 'low' | 'medium' | 'high') => {
    if (evaluation) return;
    setConfidenceRatings({ ...confidenceRatings, [questionId]: level });
  };

  const handleSubmit = async () => {
    if (!quiz || !activeConcept || !activeCourse) return;
    setIsSubmitting(true);
    try {
      const res = await quizApi.submitQuiz(activeConcept.id, {
        quiz_id: quiz.id,
        concept_id: activeConcept.id,
        course_id: activeCourse.id,
        answers: selectedAnswers,
      });
      setEvaluation(res.evaluation);
      addXP(res.evaluation.xp_earned);
      await refreshCourse();
      if (res.evaluation.passed) {
        confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 } });
      }
    } catch (err) {
      console.error('Quiz error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!activeCourse || !activeConcept) return <div className="p-12 text-center text-slate-400">Please select a concept first.</div>;

  const answeredCount = Object.keys(selectedAnswers).length;
  const totalCount = quiz?.questions.length || 0;
  const progressPct = totalCount > 0 ? Math.round((answeredCount / totalCount) * 100) : 0;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Top Banner */}
      <div className="surface-card p-6 flex flex-wrap justify-between items-center gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs text-indigo-400 font-semibold">{activeCourse.title}</span>
            <span className="text-slate-600">•</span>
            <span className="text-[11px] text-slate-400">Diagnostic Mastery Exam</span>
          </div>
          <h1 className="text-2xl font-black text-white">{activeConcept.title}</h1>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <span className="text-[10px] text-slate-400 block uppercase font-bold">Progress</span>
            <span className="text-xs font-mono font-bold text-indigo-300">{answeredCount} of {totalCount} Answered</span>
          </div>
          <span className="text-xs text-slate-300 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800 font-mono">
            Pass: 75%
          </span>
        </div>
      </div>

      {isLoading || !quiz ? (
        <div className="surface-card py-24 text-center text-slate-400 space-y-3">
          <Sparkles className="h-8 w-8 text-indigo-400 animate-spin mx-auto" />
          <p className="text-sm font-medium">Generating diagnostic quiz questions & misconception traps...</p>
        </div>
      ) : (
        <div className="space-y-6">
          {quiz.questions.map((q, idx) => {
            const isMulti = q.type === 'multiple_select';
            const userAns = selectedAnswers[q.id];
            const qEval = evaluation?.evaluations?.find((e) => e.question_id === q.id);
            const userConfidence = confidenceRatings[q.id];

            return (
              <div
                key={q.id}
                className={`surface-card p-6 space-y-5 transition-all ${qEval
                    ? qEval.is_correct
                      ? 'border-emerald-500/50 bg-emerald-950/10'
                      : 'border-rose-500/50 bg-rose-950/10'
                    : ''
                  }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
                    Question {idx + 1} of {quiz.questions.length}
                  </span>
                  {isMulti && (
                    <span className="text-[10px] bg-purple-950/60 text-purple-300 border border-purple-800 px-2 py-0.5 rounded-full font-bold">
                      Multiple Select
                    </span>
                  )}
                  {qEval && (
                    <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${qEval.is_correct ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-rose-950 text-rose-300 border border-rose-800'
                      }`}>
                      {qEval.is_correct ? '✓ Correct' : '✗ Misconception Detected'}
                    </span>
                  )}
                </div>

                <p className="text-sm font-bold text-slate-100 leading-relaxed">{q.prompt}</p>

                {q.options && (
                  <div className="space-y-2.5">
                    {q.options.map((opt, oIdx) => {
                      const isSelected = isMulti ? Array.isArray(userAns) && userAns.includes(oIdx) : userAns === oIdx;
                      let optionBorder = 'bg-slate-950 border-slate-800/80 text-slate-300 hover:bg-slate-900';

                      if (qEval) {
                        const isCorrectOption = Array.isArray(qEval.correct_answer)
                          ? qEval.correct_answer.includes(oIdx)
                          : qEval.correct_answer === oIdx;
                        if (isCorrectOption) {
                          optionBorder = 'bg-emerald-950/60 border-emerald-500 text-emerald-200 font-bold';
                        } else if (isSelected && !qEval.is_correct) {
                          optionBorder = 'bg-rose-950/60 border-rose-500 text-rose-200 line-through';
                        } else {
                          optionBorder = 'bg-slate-950/40 border-slate-800 text-slate-600';
                        }
                      } else if (isSelected) {
                        optionBorder = 'bg-indigo-600/25 border-indigo-500 text-white shadow-md shadow-indigo-600/20';
                      }

                      return (
                        <button
                          key={oIdx}
                          type="button"
                          disabled={!!evaluation}
                          onClick={() => handleSelectOption(q.id, oIdx, isMulti)}
                          className={`w-full p-3.5 rounded-xl border text-left text-xs font-medium transition-all ${optionBorder}`}
                        >
                          <div className="flex items-center gap-2.5">
                            <span className="h-5 w-5 rounded-md bg-slate-900 border border-slate-700/80 flex items-center justify-center font-mono text-[10px] text-slate-400 shrink-0">
                              {String.fromCharCode(65 + oIdx)}
                            </span>
                            <span className="flex-1">{opt}</span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                )}

                {/* Novel Feature: Confidence Calibration Selector */}
                {!evaluation && (
                  <div className="pt-2 border-t border-slate-800/60 flex flex-wrap items-center justify-between gap-2">
                    <span className="text-[11px] font-bold text-slate-400 flex items-center gap-1.5">
                      <Gauge className="h-3.5 w-3.5 text-amber-400" />
                      Confidence Level:
                    </span>
                    <div className="flex gap-1.5">
                      {[
                        { id: 'low', label: 'Uncertain 🤔', color: 'hover:border-slate-500' },
                        { id: 'medium', label: 'Fairly Sure 👍', color: 'hover:border-indigo-500' },
                        { id: 'high', label: '100% Certain 🎯', color: 'hover:border-emerald-500' },
                      ].map((lvl) => (
                        <button
                          key={lvl.id}
                          type="button"
                          onClick={() => setConfidence(q.id, lvl.id as any)}
                          className={`px-2.5 py-1 rounded-lg text-[10px] font-semibold border transition-all ${userConfidence === lvl.id
                              ? 'bg-amber-500/20 text-amber-300 border-amber-500 shadow-sm'
                              : 'bg-slate-950 border-slate-800 text-slate-400'
                            }`}
                        >
                          {lvl.label}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {qEval && (
                  <div className="mt-3 pt-3 border-t border-slate-800/80 text-xs text-slate-300 space-y-1.5">
                    <div>
                      <span className="font-bold text-indigo-400">Pedagogical Analysis: </span>
                      {qEval.explanation}
                    </div>
                    {qEval.misconception_detected && (
                      <div className="p-2.5 rounded-lg bg-rose-950/40 border border-rose-800/50 text-[11px] text-rose-300 font-medium">
                        ⚠️ <strong>Diagnosed Mental Model Gap:</strong> {qEval.misconception_detected}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}

          {!evaluation ? (
            <div className="surface-card p-5 flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-white">Ready for evaluation?</span>
                <p className="text-[11px] text-slate-400">{answeredCount} of {totalCount} questions selected</p>
              </div>
              <button
                onClick={handleSubmit}
                disabled={isSubmitting || answeredCount === 0}
                className="flex items-center gap-2 px-8 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-50 text-white font-bold text-xs shadow-xl shadow-indigo-600/25 transition-all"
              >
                {isSubmitting ? (
                  <>
                    <Sparkles className="h-4 w-4 animate-spin" />
                    Grading & Diagnosing Mental Models...
                  </>
                ) : (
                  <>
                    <span>Submit Quiz for AI Evaluation</span>
                    <ArrowRight className="h-4 w-4" />
                  </>
                )}
              </button>
            </div>
          ) : (
            <div className="surface-card p-6 space-y-6 border-indigo-500/40">
              <div className="flex justify-between items-center border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`text-xs font-bold uppercase px-2.5 py-0.5 rounded-full ${evaluation.passed ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-rose-950 text-rose-300 border border-rose-800'
                      }`}>
                      {evaluation.passed ? 'PASSED — 75%+ Mastery' : 'REMEDIATION RECOMMENDED'}
                    </span>
                  </div>
                  <h3 className="text-xl font-extrabold text-white">
                    {evaluation.passed ? '🎉 Conceptual Milestone Achieved!' : '⚠️ Adaptive Loop Triggered'}
                  </h3>
                  <p className="text-xs text-slate-300 mt-1 max-w-xl leading-relaxed">{evaluation.feedback_summary}</p>
                </div>
                <div className="text-center bg-slate-950 p-4 rounded-2xl border border-slate-800">
                  <span className="text-[10px] font-bold text-slate-400 block uppercase">Accuracy</span>
                  <div className={`text-3xl font-black ${evaluation.passed ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {evaluation.total_score}%
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
                <div className="text-xs text-slate-400">
                  Earned <strong className="text-amber-400 font-mono">+{evaluation.xp_earned} XP</strong> for this diagnostic attempt.
                </div>
                <div className="flex gap-3">
                  {evaluation.passed ? (
                    <button
                      onClick={() => navigate('/roadmap')}
                      className="flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg shadow-emerald-600/30"
                    >
                      <span>Proceed to Next Roadmap Concept</span>
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  ) : (
                    <button
                      onClick={() => navigate('/remediation')}
                      className="flex items-center gap-2 px-6 py-3 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs shadow-lg shadow-rose-600/30"
                    >
                      <span>Begin Adaptive Remediation</span>
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};


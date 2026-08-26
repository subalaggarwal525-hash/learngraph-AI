import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BookOpen, Sparkles, HelpCircle, Code, Lightbulb, CheckCircle2, ArrowRight,
  MessageSquare, Youtube, Mic, Check, ChevronDown, ChevronUp, BrainCircuit, Play
} from 'lucide-react';
import { useCourse } from '../context/CourseContext';
import { lessonApi, resourceApi, tutorApi } from '../services/api';
import { LessonContent, CuratedResource, TeachingMode } from '../types';
import { DiagramRenderer } from '../components/DiagramRenderer';
import { MemoryPagingSimulation } from '../components/simulations/MemoryPagingSimulation';
import { CPUSchedulingSimulation } from '../components/simulations/CPUSchedulingSimulation';
import { SortingSimulation } from '../components/simulations/SortingSimulation';
import { NetworkPacketSimulation } from '../components/simulations/NetworkPacketSimulation';

export const LessonPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, activeConceptId, setIsTutorOpen, selectedTeachingMode, setSelectedTeachingMode, addXP } = useCourse();
  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [resources, setResources] = useState<CuratedResource[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Progressive Disclosure states
  const [activeStep, setActiveStep] = useState<number>(1);
  const [quickCheckAnswer, setQuickCheckAnswer] = useState<number | null>(null);
  const [showQuickCheckFeedback, setShowQuickCheckFeedback] = useState<boolean>(false);

  // Feynman Technique ("Explain It Back") State
  const [isExplainModalOpen, setIsExplainModalOpen] = useState<boolean>(false);
  const [userExplanationText, setUserExplanationText] = useState<string>('');
  const [explanationEval, setExplanationEval] = useState<any>(null);
  const [isEvaluatingExplain, setIsEvaluatingExplain] = useState<boolean>(false);

  const activeConcept = (activeCourse?.concepts || []).find((c) => c.id === activeConceptId) || activeCourse?.concepts?.[0];

  const teachingModes: Array<{ id: TeachingMode; label: string; icon: string; desc: string }> = [
    { id: 'simple', label: 'Structured', icon: '📝', desc: 'Concise core foundations' },
    { id: 'eli5', label: 'ELI5', icon: '🧒', desc: 'Zero-jargon intuitive story' },
    { id: 'analogy', label: 'Deep Analogy', icon: '🏛️', desc: 'Real-world physical metaphor' },
    { id: 'worked_example', label: 'Step Calculation', icon: '🔢', desc: 'Mathematical execution trace' },
    { id: 'code', label: 'Code First', icon: '💻', desc: 'Concrete implementation' },
    { id: 'mathematical', label: 'Formal Math', icon: '📐', desc: 'Rigorous proofs & bounds' },
    { id: 'socratic', label: 'Socratic Inquiry', icon: '🤔', desc: 'Thought-provoking questions' },
  ];

  useEffect(() => {
    const fetchLesson = async () => {
      if (!activeConcept) return;
      setIsLoading(true);
      setActiveStep(1);
      setQuickCheckAnswer(null);
      setShowQuickCheckFeedback(false);
      try {
        const [lData, rData] = await Promise.all([
          lessonApi.generateLesson(activeConcept.id, selectedTeachingMode as TeachingMode),
          resourceApi.getCuratedResources(activeConcept.id)
        ]);
        setLesson(lData);
        setResources(rData);
      } catch (err) {
        console.error('Lesson load error:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchLesson();
  }, [activeConcept?.id, selectedTeachingMode]);

  const handleEvaluateExplanation = async () => {
    if (!userExplanationText.trim() || !activeCourse || !activeConcept) return;
    setIsEvaluatingExplain(true);
    try {
      const res = await tutorApi.evaluateExplanation({
        course_id: activeCourse.id,
        concept_id: activeConcept.id,
        student_explanation: userExplanationText
      });
      setExplanationEval(res);
      addXP(50);
    } catch (err) {
      console.error('Feynman evaluation error:', err);
    } finally {
      setIsEvaluatingExplain(false);
    }
  };

  if (!activeCourse || !activeConcept) return <div className="p-12 text-center text-slate-400">Please select a course concept first.</div>;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      {/* Concept Header Card */}
      <div className="surface-card p-6 space-y-5">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs text-indigo-400 font-semibold tracking-wide">{activeCourse.title}</span>
              <span className="text-slate-600">•</span>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono">
                {activeConcept.difficulty ? `Level ${activeConcept.difficulty}/5` : 'Applied'}
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">{activeConcept.title}</h1>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsExplainModalOpen(true)}
              className="flex items-center gap-2 px-3.5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500/20 to-orange-500/20 border border-amber-500/40 text-amber-300 hover:text-white text-xs font-bold transition-all hover:scale-105"
            >
              <Mic className="h-4 w-4 text-amber-400" />
              <span>Explain It Back</span>
            </button>
            <button
              onClick={() => setIsTutorOpen(true)}
              className="flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl bg-purple-950/60 text-purple-300 text-xs font-bold border border-purple-800/60 hover:bg-purple-900/60"
            >
              <MessageSquare className="h-4 w-4" /> AI Tutor
            </button>
            <button
              onClick={() => navigate('/quiz')}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30"
            >
              <HelpCircle className="h-4 w-4" /> Take Quiz
            </button>
          </div>
        </div>

        {/* Adaptive Teaching Mode Pills */}
        <div>
          <div className="flex items-center justify-between text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2.5">
            <span>Adaptive Pedagogy Style:</span>
            <span className="text-indigo-400 font-normal normal-case">Tailors tone, math rigor, and analogies</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2">
            {teachingModes.map((m) => (
              <button
                key={m.id}
                onClick={() => setSelectedTeachingMode(m.id)}
                className={`p-2.5 rounded-xl border text-left flex flex-col justify-between transition-all ${selectedTeachingMode === m.id
                    ? 'bg-indigo-600/30 border-indigo-500 text-white ring-2 ring-indigo-500/40 shadow-lg'
                    : 'bg-slate-950/60 border-slate-800/80 text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                  }`}
              >
                <div className="flex items-center gap-1.5 text-xs font-bold">
                  <span>{m.icon}</span>
                  <span className="truncate">{m.label}</span>
                </div>
                <span className="text-[10px] text-slate-400 line-clamp-1 mt-1 font-normal">{m.desc}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {isLoading || !lesson ? (
        <div className="surface-card py-24 text-center text-slate-400 space-y-4">
          <Sparkles className="h-9 w-9 text-indigo-400 animate-spin mx-auto" />
          <p className="text-sm font-medium">Synthesizing pedagogical breakdown in <strong className="text-white">{selectedTeachingMode}</strong> mode...</p>
        </div>
      ) : (
        <div className="space-y-8">
          {/* Step 1: Learning Objective & Prerequisite Reminder */}
          <div className="surface-card p-6 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
                <BrainCircuit className="h-4 w-4" /> 1. Learning Objective & Prerequisite Hook
              </span>
              <span className="text-[11px] font-mono text-slate-400">Step 1 of 4</span>
            </div>

            <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-800/40 space-y-2">
              <span className="text-[11px] font-bold text-indigo-300 uppercase tracking-wider block">Target Competency:</span>
              <p className="text-xs text-slate-200 leading-relaxed font-medium">
                {lesson.learning_objective}
              </p>
            </div>

            {lesson.prerequisite_reminder && (
              <p className="text-xs text-slate-400 flex items-start gap-2 pt-2 border-t border-slate-800/60">
                <span className="text-amber-400 font-bold">Prerequisite Insight:</span>
                <span>{lesson.prerequisite_reminder}</span>
              </p>
            )}
          </div>

          {/* Step 2: Core Concept Breakdown */}
          <div className="surface-card p-6 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-extrabold text-white flex items-center gap-2">
                <BookOpen className="h-4 w-4 text-indigo-400" /> 2. Foundational Explanation
              </h3>
              <span className="text-xs font-bold text-indigo-300 px-2.5 py-0.5 rounded-full bg-indigo-950/80 border border-indigo-800/60 uppercase">
                {lesson.mode}
              </span>
            </div>

            <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800/80 space-y-3">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Intuitive Overview:</span>
              <p className="text-sm text-slate-100 leading-relaxed font-medium">
                {lesson.simple_explanation}
              </p>
            </div>

            <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Mechanism Deep-Dive:</span>
              <p>{lesson.detailed_explanation}</p>
            </div>

            {/* Visual cards for Analogy and Worked Example */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
              <div className="p-5 rounded-2xl bg-gradient-to-br from-purple-950/30 to-slate-950 border border-purple-800/40 space-y-2.5">
                <div className="flex items-center gap-2 text-purple-300 text-xs font-bold">
                  <Lightbulb className="h-4 w-4 text-purple-400" />
                  <span>Real-World Mental Model</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">{lesson.analogy}</p>
              </div>

              <div className="p-5 rounded-2xl bg-gradient-to-br from-emerald-950/30 to-slate-950 border border-emerald-800/40 space-y-2.5">
                <div className="flex items-center gap-2 text-emerald-300 text-xs font-bold">
                  <Code className="h-4 w-4 text-emerald-400" />
                  <span>Worked Example / Calculation</span>
                </div>
                <div className="text-xs font-mono text-emerald-200 bg-slate-950/80 p-3 rounded-xl border border-slate-800 whitespace-pre-wrap leading-relaxed">
                  {lesson.worked_example}
                </div>
              </div>
            </div>
          </div>

          {/* Step 3: Interactive Visuals & Simulation */}
          <div className="space-y-6">
            {lesson.visual_diagram && (
              <DiagramRenderer
                specification={lesson.visual_diagram.specification}
                caption={lesson.visual_diagram.caption}
              />
            )}

            {lesson.simulation_type === 'memory_paging' && <MemoryPagingSimulation />}
            {lesson.simulation_type === 'cpu_scheduling' && <CPUSchedulingSimulation />}
            {lesson.simulation_type === 'sorting' && <SortingSimulation />}
            {lesson.simulation_type === 'network_packet' && <NetworkPacketSimulation />}
          </div>

          {/* Step 4: Inline Micro-Quiz / Quick Check */}
          {lesson.quick_checks && lesson.quick_checks.length > 0 && (
            <div className="surface-card p-6 space-y-4 border-l-4 border-l-amber-500">
              <div className="flex items-center justify-between">
                <span className="text-xs font-extrabold text-amber-300 uppercase tracking-wider flex items-center gap-2">
                  <HelpCircle className="h-4 w-4 text-amber-400" /> Quick Understanding Check
                </span>
                <span className="text-[10px] text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">Immediate Retention Test</span>
              </div>

              {lesson.quick_checks.map((qc, idx) => (
                <div key={idx} className="space-y-3">
                  <p className="text-xs font-semibold text-slate-100">{qc.question}</p>
                  <div className="space-y-2">
                    {qc.options.map((opt, oIdx) => {
                      const isSelected = quickCheckAnswer === oIdx;
                      const isCorrect = oIdx === qc.correct_index;
                      return (
                        <button
                          key={oIdx}
                          disabled={showQuickCheckFeedback}
                          onClick={() => {
                            setQuickCheckAnswer(oIdx);
                            setShowQuickCheckFeedback(true);
                            if (isCorrect) addXP(20);
                          }}
                          className={`w-full p-3 rounded-xl border text-left text-xs font-medium transition-all ${showQuickCheckFeedback
                              ? isCorrect
                                ? 'bg-emerald-950/80 border-emerald-500 text-emerald-100 font-bold'
                                : isSelected
                                  ? 'bg-rose-950/80 border-rose-500 text-rose-200'
                                  : 'bg-slate-950/50 border-slate-800 text-slate-500'
                              : isSelected
                                ? 'bg-indigo-600/30 border-indigo-500 text-white'
                                : 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-900'
                            }`}
                        >
                          {opt}
                        </button>
                      );
                    })}
                  </div>

                  {showQuickCheckFeedback && (
                    <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-1">
                      <div className={`font-bold ${quickCheckAnswer === qc.correct_index ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {quickCheckAnswer === qc.correct_index ? '✓ Correct! +20 XP' : '✗ Not quite.'}
                      </div>
                      <p className="text-slate-300">{qc.explanation}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Curated Resources */}
          <div className="surface-card p-6 space-y-4">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
              <Youtube className="h-4 w-4 text-rose-400" /> Curated Academic Resources & Video Grounding
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {resources.map((res) => (
                <div key={res.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-3">
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-300">{res.type}</span>
                      <span className="text-[11px] font-mono font-bold text-emerald-400 bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-800/40">{res.coverage_percentage}% Match</span>
                    </div>
                    <h4 className="text-xs font-bold text-white">{res.title}</h4>
                  </div>
                  <a href={res.url} target="_blank" rel="noreferrer" className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold pt-2 border-t border-slate-800 block">
                    Access Material ({res.duration_or_read_time}) →
                  </a>
                </div>
              ))}
            </div>
          </div>

          {/* Bottom Action Strip */}
          <div className="flex flex-wrap items-center justify-between gap-4 p-5 surface-card">
            <div>
              <h4 className="text-xs font-bold text-white">Ready to lock in mastery?</h4>
              <p className="text-[11px] text-slate-400">Pass the diagnostic assessment with 75%+ score to unlock the next concept.</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => setIsExplainModalOpen(true)}
                className="flex items-center gap-2 px-5 py-3 rounded-xl bg-amber-950/60 border border-amber-600/40 text-amber-300 text-xs font-bold hover:bg-amber-900/60"
              >
                <Mic className="h-4 w-4 text-amber-400" />
                <span>Explain It Back First</span>
              </button>
              <button
                onClick={() => navigate('/quiz')}
                className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs shadow-xl shadow-indigo-500/20"
              >
                <span>Proceed to Assessment Quiz</span>
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Feynman Technique Modal ("Explain It Back") */}
      {isExplainModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="surface-card max-w-2xl w-full p-6 space-y-5 border-amber-500/30">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-xl bg-amber-500/20 text-amber-400">
                  <Mic className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">Feynman Technique: Explain It Back</h3>
                  <p className="text-[11px] text-slate-400">Teach this concept back to the AI to uncover hidden gaps in your mental model.</p>
                </div>
              </div>
              <button onClick={() => { setIsExplainModalOpen(false); setExplanationEval(null); }} className="text-slate-400 hover:text-white text-sm">✕</button>
            </div>

            {!explanationEval ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-slate-300 mb-1.5">
                    How would you explain <span className="text-indigo-400">"{activeConcept.title}"</span> in your own words?
                  </label>
                  <textarea
                    rows={6}
                    value={userExplanationText}
                    onChange={(e) => setUserExplanationText(e.target.value)}
                    placeholder="E.g. Memory paging works by dividing memory into fixed blocks so programs don't need contiguous RAM..."
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl p-3.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500 font-sans leading-relaxed"
                  />
                  <div className="flex justify-between items-center text-[10px] text-slate-400 mt-1">
                    <span>Aim for clarity and mechanism cause-and-effect.</span>
                    <span>{userExplanationText.split(/\s+/).filter(Boolean).length} words</span>
                  </div>
                </div>

                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => setIsExplainModalOpen(false)}
                    className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleEvaluateExplanation}
                    disabled={isEvaluatingExplain || userExplanationText.trim().length < 10}
                    className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 text-white text-xs font-bold shadow-lg disabled:opacity-50 flex items-center gap-2"
                  >
                    {isEvaluatingExplain ? (
                      <>
                        <Sparkles className="h-4 w-4 animate-spin" />
                        Analyzing Mental Model...
                      </>
                    ) : (
                      <>
                        <span>Submit for Pedagogical Audit (+50 XP)</span>
                        <ArrowRight className="h-4 w-4" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-3">
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
                    <span className="text-[10px] text-slate-400 block uppercase font-bold">Overall Score</span>
                    <span className="text-xl font-black text-amber-400">{explanationEval.overall_score}%</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
                    <span className="text-[10px] text-slate-400 block uppercase font-bold">Clarity</span>
                    <span className="text-xl font-black text-indigo-400">{explanationEval.clarity_score}%</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
                    <span className="text-[10px] text-slate-400 block uppercase font-bold">Mechanics</span>
                    <span className="text-xl font-black text-emerald-400">{explanationEval.accuracy_score}%</span>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 space-y-3 max-h-60 overflow-y-auto leading-relaxed">
                  <div className="space-y-1">
                    <span className="text-[11px] font-bold text-emerald-400 uppercase">Observed Strengths:</span>
                    {explanationEval.strengths.map((s: string, idx: number) => (
                      <div key={idx} className="flex items-start gap-2 text-slate-200">
                        <Check className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                        <span>{s}</span>
                      </div>
                    ))}
                  </div>
                  {explanationEval.gaps && explanationEval.gaps.length > 0 && (
                    <div className="space-y-1 pt-2 border-t border-slate-800">
                      <span className="text-[11px] font-bold text-amber-400 uppercase">Opportunity for Deeper Understanding:</span>
                      {explanationEval.gaps.map((g: string, idx: number) => (
                        <div key={idx} className="text-slate-300">• {g}</div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => { setExplanationEval(null); }}
                    className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold"
                  >
                    Try Explaining Again
                  </button>
                  <button
                    onClick={() => { setIsExplainModalOpen(false); navigate('/quiz'); }}
                    className="px-6 py-2.5 rounded-xl bg-indigo-600 text-white text-xs font-bold"
                  >
                    Proceed to Quiz →
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};


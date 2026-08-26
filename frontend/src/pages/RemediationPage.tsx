import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GitBranch, BookOpen, RotateCcw, ArrowRight, ShieldAlert, Sparkles, CheckCircle2, Lightbulb } from 'lucide-react';
import { useCourse } from '../context/CourseContext';

export const RemediationPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, activeConceptId, setSelectedTeachingMode } = useCourse();
  const activeConcept = (activeCourse?.concepts || []).find((c) => c.id === activeConceptId) || activeCourse?.concepts?.[0];

  if (!activeCourse || !activeConcept) return <div className="p-12 text-center text-slate-400">No active concept for remediation.</div>;
  const prereq = activeConcept.prerequisites?.[0] || 'Foundational Addressing & Memory Architecture';

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Alert Header */}
      <div className="surface-card p-6 border-rose-500/50 bg-gradient-to-br from-rose-950/30 via-slate-900 to-indigo-950/20 space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/80 border border-rose-800 text-xs font-bold text-rose-300">
          <GitBranch className="h-3.5 w-3.5 text-rose-400" />
          <span>Continuous Adaptive Remediation Loop</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white">Re-aligning Mental Model: {activeConcept.title}</h1>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-2xl">
          LearnGraph AI analyzed your diagnostic quiz error patterns. Your confusion is rooted in a fundamental gap within the prerequisite domain: <strong className="text-amber-300 font-mono">[{prereq}]</strong>.
        </p>
      </div>

      {/* Root Cause Diagnostics Card */}
      <div className="surface-card p-6 space-y-5">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
          <ShieldAlert className="h-4 w-4 text-amber-400" />
          <h3 className="text-sm font-extrabold text-white">Root-Cause Mental Model Dissection</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-2">
            <span className="text-[11px] font-bold text-rose-400 uppercase tracking-wider block">Observed Flawed Invariant:</span>
            <p className="text-xs text-slate-300 leading-relaxed">
              Treating address spaces as flat contiguous RAM arrays rather than discrete, page-mapped frame offsets.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-2">
            <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider block">Correct Scientific Model:</span>
            <p className="text-xs text-slate-300 leading-relaxed">
              The MMU hardware separates virtual page indexing (VPN) from offset calculation to allow non-contiguous physical allocation.
            </p>
          </div>
        </div>
      </div>

      {/* Remediation Action Pathways */}
      <div className="surface-card p-6 space-y-4">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Recommended Adaptive Learning Pathways</h3>

        <div className="space-y-3">
          <div className="p-4 rounded-xl bg-slate-950 border border-indigo-500/40 flex flex-wrap items-center justify-between gap-4 hover:bg-slate-900/60 transition-all">
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-xs font-bold text-white">
                <Lightbulb className="h-4 w-4 text-indigo-400" />
                <span>Re-teach with Step-by-Step Worked Example (Recommended)</span>
              </div>
              <p className="text-[11px] text-slate-400">Walk through address calculations bit by bit with zero assumptions.</p>
            </div>
            <button
              onClick={() => { setSelectedTeachingMode('worked_example'); navigate('/lesson'); }}
              className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/20"
            >
              Start Worked Example →
            </button>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-wrap items-center justify-between gap-4 hover:bg-slate-900/60 transition-all">
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-xs font-bold text-white">
                <BookOpen className="h-4 w-4 text-purple-400" />
                <span>Switch to Intuitive Real-World Analogy</span>
              </div>
              <p className="text-[11px] text-slate-400">Reframe the concept using physical warehouse and customs metaphors.</p>
            </div>
            <button
              onClick={() => { setSelectedTeachingMode('analogy'); navigate('/lesson'); }}
              className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold"
            >
              Switch to Analogy →
            </button>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={() => navigate('/quiz')}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-300 text-xs font-semibold"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            <span>Retry Quiz Immediately</span>
          </button>
        </div>
      </div>
    </div>
  );
};

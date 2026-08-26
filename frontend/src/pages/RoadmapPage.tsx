import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Milestone, CheckCircle2, Lock, Play, AlertTriangle, ArrowRight, Clock } from 'lucide-react';
import { useCourse } from '../context/CourseContext';

export const RoadmapPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, setActiveConceptId } = useCourse();

  if (!activeCourse) return <div className="p-12 text-center text-slate-400">Please select a course first.</div>;
  const stages = activeCourse.roadmap?.stages || [];
  const conceptMap = new Map((activeCourse.concepts || []).map((c) => [c.id, c]));

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-2xl font-black text-white">{activeCourse.title} — Personalized Roadmap</h1>
          <p className="text-xs text-slate-400 mt-1">Hierarchical prerequisite dependency tiers.</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex gap-6">
          <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Mastery</span><span className="text-xl font-black text-indigo-400">{activeCourse.roadmap?.progress_percentage ?? 0}%</span></div>
          <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Completed</span><span className="text-xl font-black text-emerald-400">{activeCourse.roadmap?.completed_concepts ?? 0} / {activeCourse.roadmap?.total_concepts ?? 0}</span></div>
        </div>
      </div>

      <div className="space-y-6">
        {stages.map((stg) => (
          <div key={stg.stage_number} className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-3">
                <span className="h-7 w-7 rounded-lg bg-indigo-600/30 text-indigo-300 flex items-center justify-center font-bold text-xs">{stg.stage_number}</span>
                <div><h3 className="text-sm font-bold text-slate-100">{stg.stage_name}</h3><p className="text-[11px] text-slate-400">{stg.description}</p></div>
              </div>
              <span className="text-xs text-slate-400 bg-slate-950 px-3 py-1 rounded-lg border border-slate-800">Est. {stg.estimated_hours}h</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {stg.concept_ids.map((cid) => {
                const concept = conceptMap.get(cid);
                if (!concept) return null;
                const isLocked = concept.status === 'locked';
                return (
                  <div
                    key={cid}
                    onClick={() => { if (!isLocked) { setActiveConceptId(cid); navigate('/lesson'); } }}
                    className={`p-4 rounded-xl border flex flex-col justify-between ${isLocked ? 'bg-slate-950/40 border-slate-800/60 opacity-60 cursor-not-allowed' : 'bg-slate-950 border-slate-800 cursor-pointer hover:border-indigo-500'}`}
                  >
                    <div>
                      <div className="flex justify-between mb-2">
                        <span className="text-[9px] font-bold uppercase px-2 py-0.5 rounded bg-indigo-950 text-indigo-300">{concept.status}</span>
                        <span className="text-[10px] text-slate-400 font-mono">{concept.estimated_minutes}m</span>
                      </div>
                      <h4 className="text-xs font-bold text-slate-100">{concept.title}</h4>
                      <p className="text-[11px] text-slate-400 mt-1">{concept.short_summary}</p>
                    </div>
                    {!isLocked && <div className="mt-3 pt-2 border-t border-slate-800 flex justify-end text-[10px] text-indigo-400 font-bold">Study Now →</div>}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

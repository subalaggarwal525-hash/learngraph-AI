import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Network, CheckCircle2, Loader2, ArrowRight } from 'lucide-react';
import { useCourse } from '../context/CourseContext';

export const AnalysisPage: React.FC = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const navigate = useNavigate();
  const { activeCourse, loadCourse } = useCourse();
  const [stepIndex, setStepIndex] = useState(0);

  const steps = [
    { title: 'Normalizing & Parsing Raw Material', desc: 'Preserving document structure and definitions' },
    { title: 'LangGraph Concept Extraction', desc: 'Identifying core subtopics and common pitfalls' },
    { title: 'Prerequisite Dependency DAG Analysis', desc: 'Computing topological tiers and layout' },
    { title: 'Synthesizing Interactive Knowledge Graph', desc: 'Generating visual layouts and roadmap stages' }
  ];

  useEffect(() => {
    if (courseId) loadCourse(courseId);
  }, [courseId]);

  useEffect(() => {
    const timer = setInterval(() => {
      setStepIndex((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 800);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="max-w-3xl mx-auto px-4 py-16 text-center space-y-8">
      <div className="inline-flex p-4 rounded-3xl bg-indigo-600/10 border border-indigo-500/30 text-indigo-400 shadow-2xl animate-pulse">
        <Network className="h-12 w-12" />
      </div>
      <div>
        <h1 className="text-3xl font-black text-white">Building Knowledge Graph for <span className="text-indigo-400">{activeCourse?.title || 'Subject'}</span></h1>
      </div>
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 text-left space-y-4 max-w-xl mx-auto shadow-2xl">
        {steps.map((s, idx) => (
          <div key={idx} className={`flex items-start gap-3.5 p-3 rounded-xl ${idx <= stepIndex ? 'opacity-100 bg-indigo-950/30' : 'opacity-40'}`}>
            {idx < stepIndex ? <CheckCircle2 className="h-5 w-5 text-emerald-400" /> : <Loader2 className="h-5 w-5 text-indigo-400 animate-spin" />}
            <div>
              <h4 className="text-xs font-bold text-slate-200">{s.title}</h4>
              <p className="text-[11px] text-slate-400">{s.desc}</p>
            </div>
          </div>
        ))}
      </div>
      <button onClick={() => navigate('/graph')} className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold text-xs shadow-xl">
        <span>Open Interactive Knowledge Graph</span>
        <ArrowRight className="h-4 w-4" />
      </button>
    </div>
  );
};

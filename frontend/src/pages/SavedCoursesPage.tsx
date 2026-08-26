import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, PlusCircle, ArrowRight, Library } from 'lucide-react';
import { courseApi } from '../services/api';
import { useCourse } from '../context/CourseContext';

export const SavedCoursesPage: React.FC = () => {
  const navigate = useNavigate();
  const { loadCourse } = useCourse();
  const [courses, setCourses] = useState<any[]>([]);

  useEffect(() => {
    courseApi.listCourses().then(setCourses).catch(console.error);
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      <div className="flex justify-between items-center border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-2xl font-black text-white">Saved Learning Journeys</h1>
          <p className="text-xs text-slate-400 mt-1">Persisted courses and knowledge graph states.</p>
        </div>
        <button onClick={() => navigate('/create')} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-bold">
          <PlusCircle className="h-4 w-4" /> New Journey
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {courses.map((c) => (
          <div
            key={c.id}
            onClick={async () => { await loadCourse(c.id); navigate('/graph'); }}
            className="p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500 cursor-pointer shadow-xl transition-all"
          >
            <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-indigo-950 text-indigo-300">{c.source_type}</span>
            <h3 className="text-base font-bold text-white mt-2">{c.title}</h3>
            <div className="mt-4 flex justify-between text-xs text-indigo-400 font-bold">
              <span>Progress: {c.progress_percentage}%</span>
              <span>Open Graph →</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

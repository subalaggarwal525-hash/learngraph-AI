import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Globe, Youtube, UploadCloud, FileText, ArrowRight, Target, Gauge, Clock, Check } from 'lucide-react';
import { courseApi, documentApi } from '../services/api';
import { useCourse } from '../context/CourseContext';

export const CreateJourneyPage: React.FC = () => {
  const navigate = useNavigate();
  const { loadCourse } = useCourse();

  const [sourceType, setSourceType] = useState<'topic' | 'url' | 'youtube' | 'document' | 'notes'>('topic');
  const [topicInput, setTopicInput] = useState('Operating Systems: Processes, Virtual Memory & Paging');
  const [urlInput, setUrlInput] = useState('');
  const [youtubeInput, setYoutubeInput] = useState('https://www.youtube.com/watch?v=26QPDBe-NB8');
  const [notesInput, setNotesInput] = useState('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const [goal, setGoal] = useState('exam');
  const [level, setLevel] = useState('beginner');
  const [studyHours, setStudyHours] = useState(5);
  const [preferredStyle, setPreferredStyle] = useState('simple');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    let content = topicInput;
    if (sourceType === 'url') content = urlInput || 'https://en.wikipedia.org/wiki/Operating_system';
    if (sourceType === 'youtube') content = youtubeInput;
    if (sourceType === 'notes') content = notesInput || topicInput;
    if (sourceType === 'document') content = uploadedFile ? `Uploaded Document: ${uploadedFile.name}` : topicInput;

    try {
      const result = await courseApi.createCourse({
        title: sourceType === 'topic' ? topicInput : undefined,
        source_type: sourceType,
        source_content: content,
        learning_goal: goal,
        current_level: level,
        study_time_hours_per_week: studyHours,
        preferred_style: preferredStyle
      });

      if (sourceType === 'document' && uploadedFile && result.id) {
        await documentApi.uploadDocument(result.id, uploadedFile);
      }

      await loadCourse(result.id);
      navigate(`/analysis/${result.id}`);
    } catch (err) {
      console.error('Course creation error:', err);
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-black text-white">Create a New Learning Journey</h1>
        <p className="mt-2 text-sm text-slate-400">Provide any source material and select your goals.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
          <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider">1. Select Learning Source</label>
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
            {[
              { id: 'topic', label: 'Topic', icon: Sparkles },
              { id: 'youtube', label: 'YouTube', icon: Youtube },
              { id: 'url', label: 'Web URL', icon: Globe },
              { id: 'document', label: 'File Upload', icon: UploadCloud },
              { id: 'notes', label: 'Notes', icon: FileText },
            ].map((tab) => {
              const Icon = tab.icon;
              const isSelected = sourceType === tab.id;
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setSourceType(tab.id as any)}
                  className={`flex flex-col items-center justify-center p-3 rounded-xl border text-xs font-semibold ${
                    isSelected ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500' : 'bg-slate-950/60 border-slate-800 text-slate-400'
                  }`}
                >
                  <Icon className="h-5 w-5 mb-1.5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          <div className="mt-4">
            {sourceType === 'topic' && (
              <input
                type="text"
                value={topicInput}
                onChange={(e) => setTopicInput(e.target.value)}
                placeholder="e.g. Operating Systems: Processes, Virtual Memory & Paging"
                required
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            )}
            {sourceType === 'youtube' && (
              <input
                type="url"
                value={youtubeInput}
                onChange={(e) => setYoutubeInput(e.target.value)}
                placeholder="https://www.youtube.com/watch?v=..."
                required
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white font-mono"
              />
            )}
            {sourceType === 'url' && (
              <input
                type="url"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://docs.example.com"
                required
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white font-mono"
              />
            )}
            {sourceType === 'document' && (
              <div className="border-2 border-dashed border-slate-800 rounded-xl p-6 text-center">
                <UploadCloud className="h-8 w-8 text-indigo-400 mx-auto mb-2" />
                <label className="cursor-pointer text-xs font-semibold text-indigo-400 hover:underline block">
                  Click to upload PDF, DOCX, PPTX, or TXT
                  <input type="file" className="hidden" accept=".pdf,.docx,.doc,.pptx,.ppt,.txt,.md" onChange={(e) => setUploadedFile(e.target.files ? e.target.files[0] : null)} />
                </label>
                {uploadedFile && <div className="mt-2 text-xs text-indigo-300 font-bold">{uploadedFile.name}</div>}
              </div>
            )}
            {sourceType === 'notes' && (
              <textarea rows={4} value={notesInput} onChange={(e) => setNotesInput(e.target.value)} placeholder="Paste notes..." className="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-xs text-white" />
            )}
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
          <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <Target className="h-4 w-4 text-indigo-400" />
            2. Goal & Level
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {[
              { id: 'exam', title: 'University Exam', desc: 'Coverage & high-yield quiz items' },
              { id: 'interview', title: 'Interview', desc: 'Systems design & code questions' },
              { id: 'deep_understanding', title: 'Deep Understanding', desc: 'First principles & simulations' }
            ].map((opt) => (
              <button
                key={opt.id}
                type="button"
                onClick={() => setGoal(opt.id)}
                className={`p-3.5 rounded-xl border text-left ${goal === opt.id ? 'bg-indigo-600/20 text-white border-indigo-500' : 'bg-slate-950/60 border-slate-800 text-slate-400'}`}
              >
                <div className="text-xs font-bold text-slate-100">{opt.title}</div>
                <div className="text-[11px] text-slate-400 mt-1">{opt.desc}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 text-white font-bold text-sm shadow-xl transition-all"
          >
            {isLoading ? 'LangGraph Processing...' : 'Generate Knowledge Graph & Roadmap'}
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  );
};

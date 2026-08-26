import React, { useState } from 'react';
import { X, Send, Bot, Sparkles, BookOpen } from 'lucide-react';
import { useCourse } from '../context/CourseContext';
import { tutorApi } from '../services/api';

export const AITutorWidget: React.FC = () => {
  const { isTutorOpen, setIsTutorOpen, activeCourse, activeConceptId } = useCourse();
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'ai'; text: string; sources?: string[] }>>([
    {
      sender: 'ai',
      text: "👋 Hi! I'm your LearnGraph AI Tutor. I have full context of your active concept and uploaded study sources. What would you like to explore or clarify?",
      sources: []
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [mode, setMode] = useState<'tutor' | 'socratic'>('tutor');

  if (!isTutorOpen) return null;

  const handleSend = async (customMsg?: string) => {
    const textToSend = customMsg || inputText;
    if (!textToSend.trim() || !activeCourse) return;

    const newMsgs = [...messages, { sender: 'user' as const, text: textToSend }];
    setMessages(newMsgs);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await tutorApi.chat({
        course_id: activeCourse.id,
        concept_id: activeConceptId || undefined,
        message: textToSend,
        mode: mode
      });

      setMessages([
        ...newMsgs,
        {
          sender: 'ai',
          text: response.reply,
          sources: response.sources_cited || []
        }
      ]);
    } catch (err) {
      setMessages([
        ...newMsgs,
        {
          sender: 'ai',
          text: "I am ready to help you with this concept! Try asking for an analogy or a step-by-step example.",
          sources: []
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const quickPrompts = [
    "Explain this concept with an analogy",
    "What are the most common misconceptions?",
    "Give me a quick Socratic check question"
  ];

  return (
    <div className="fixed bottom-6 right-6 z-50 w-96 max-w-[calc(100vw-2rem)] h-[580px] bg-slate-950 border border-slate-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-200">
      <div className="p-4 border-b border-slate-800 bg-slate-900 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="h-8 w-8 rounded-lg bg-purple-600/30 border border-purple-500/50 flex items-center justify-center">
            <Bot className="h-4 w-4 text-purple-300" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <h3 className="text-xs font-bold text-slate-100">LearnGraph AI Tutor</h3>
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
            </div>
            <p className="text-[10px] text-slate-400 truncate max-w-[180px]">
              {activeCourse ? activeCourse.title : 'Ready to help'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1.5">
          <button
            onClick={() => setMode(mode === 'tutor' ? 'socratic' : 'tutor')}
            className={`px-2 py-1 rounded text-[10px] font-bold border transition-colors ${
              mode === 'socratic'
                ? 'bg-amber-950 text-amber-300 border-amber-800'
                : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
          >
            {mode === 'socratic' ? 'Socratic ON' : 'Direct Mode'}
          </button>
          <button onClick={() => setIsTutorOpen(false)} className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800">
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3.5 text-xs">
        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
            <div className={`p-3 rounded-2xl max-w-[85%] leading-relaxed ${
              m.sender === 'user' ? 'bg-indigo-600 text-white rounded-br-none' : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none'
            }`}>
              {m.text}
            </div>
            {m.sources && m.sources.length > 0 && (
              <div className="mt-1 flex items-center gap-1 text-[10px] text-indigo-400 font-mono">
                <BookOpen className="h-3 w-3" />
                <span>Grounding: {m.sources.join(', ')}</span>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex items-center gap-2 text-slate-400 text-xs italic">
            <Sparkles className="h-3.5 w-3.5 animate-spin text-purple-400" />
            AI Tutor is thinking...
          </div>
        )}
      </div>

      <div className="px-3 py-1.5 bg-slate-900/50 border-t border-slate-800/80 flex gap-1.5 overflow-x-auto no-scrollbar">
        {quickPrompts.map((q, idx) => (
          <button key={idx} onClick={() => handleSend(q)} className="shrink-0 px-2.5 py-1 rounded-full bg-slate-800 hover:bg-slate-700 text-[10px] text-slate-300">
            {q}
          </button>
        ))}
      </div>

      <div className="p-3 border-t border-slate-800 bg-slate-900/90 flex gap-2">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask anything about this concept..."
          className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        />
        <button onClick={() => handleSend()} disabled={isLoading || !inputText.trim()} className="p-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white">
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};

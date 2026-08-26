import React from 'react';
import { Link } from 'react-router-dom';
import { Network, Zap, Flame, Bot, PlusCircle, BookOpen } from 'lucide-react';
import { useCourse } from '../context/CourseContext';

export const Navbar: React.FC = () => {
  const { activeCourse, userXP, userLevel, userStreak, setIsTutorOpen, isTutorOpen } = useCourse();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform duration-200">
              <Network className="h-5 w-5 text-white" />
            </div>
            <div>
              <span className="text-lg font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-indigo-200 bg-clip-text text-transparent">
                LearnGraph <span className="text-indigo-400">AI</span>
              </span>
              <span className="block text-[10px] font-medium tracking-wider text-slate-400 uppercase">
                Adaptive University
              </span>
            </div>
          </Link>

          {activeCourse && (
            <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs text-slate-300">
              <BookOpen className="h-3.5 w-3.5 text-indigo-400" />
              <span className="truncate max-w-[200px] font-medium">{activeCourse.title}</span>
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800/50">
                {activeCourse.learning_goal.replace('_', ' ')}
              </span>
            </div>
          )}
        </div>

        <div className="flex items-center gap-3 sm:gap-5">
          <Link
            to="/create"
            className="hidden sm:inline-flex items-center gap-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white px-3.5 py-2 text-xs font-semibold shadow-md shadow-indigo-600/20 transition-colors"
          >
            <PlusCircle className="h-4 w-4" />
            New Journey
          </Link>

          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-950/40 border border-amber-800/40 text-amber-300 text-xs font-bold shadow-sm" title="Daily Learning Streak">
            <Flame className="h-4 w-4 text-amber-400 animate-pulse" />
            <span>{userStreak}d</span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-indigo-950/40 border border-indigo-800/40 text-indigo-200 text-xs font-bold shadow-sm">
            <Zap className="h-4 w-4 text-indigo-400" />
            <span>{userXP} XP</span>
            <span className="px-1.5 py-0.2 rounded bg-indigo-600/30 text-indigo-300 text-[10px]">
              Lvl {userLevel}
            </span>
          </div>

          <button
            onClick={() => setIsTutorOpen(!isTutorOpen)}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              isTutorOpen
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/25 ring-2 ring-purple-400/50'
                : 'bg-slate-900 border border-slate-700 text-slate-200 hover:bg-slate-800'
            }`}
          >
            <Bot className="h-4 w-4 text-purple-300" />
            <span className="hidden sm:inline">AI Tutor</span>
          </button>
        </div>
      </div>
    </header>
  );
};

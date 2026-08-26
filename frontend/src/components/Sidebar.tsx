import React from 'react';
import { NavLink } from 'react-router-dom';
import { Network, Milestone, BookOpen, HelpCircle, Cpu, Trophy, BarChart3, Library, Sparkles } from 'lucide-react';
import { useCourse } from '../context/CourseContext';

export const Sidebar: React.FC = () => {
  const { activeCourse } = useCourse();

  const links = [
    { to: '/graph', label: 'Knowledge Graph', icon: Network, badge: 'Interactive' },
    { to: '/roadmap', label: 'Adaptive Roadmap', icon: Milestone, badge: null },
    { to: '/lesson', label: 'Lesson Studio', icon: BookOpen, badge: '12 Modes' },
    { to: '/quiz', label: 'Assessment & Quiz', icon: HelpCircle, badge: null },
    { to: '/simulations', label: 'Simulations Lab', icon: Cpu, badge: 'Live' },
    { to: '/final-test', label: 'Mastery Boss Test', icon: Trophy, badge: 'Final' },
    { to: '/dashboard', label: 'Analytics & Spaced Rep', icon: BarChart3, badge: null },
    { to: '/courses', label: 'My Saved Journeys', icon: Library, badge: null },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950/60 p-4 flex flex-col justify-between shrink-0 hidden md:flex min-h-[calc(100vh-4rem)]">
      <div className="space-y-6">
        {activeCourse && (
          <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 shadow-inner">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
              <span className="font-semibold uppercase tracking-wider text-[10px]">Progress</span>
              <span className="text-indigo-400 font-bold">
                {activeCourse.roadmap?.progress_percentage ?? 0}%
              </span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${activeCourse.roadmap?.progress_percentage ?? 0}%` }}
              />
            </div>
            <div className="mt-2 text-[11px] text-slate-400 flex items-center justify-between">
              <span>{activeCourse.roadmap?.completed_concepts ?? 0} mastered</span>
              <span>{activeCourse.concepts?.length ?? 0} total</span>
            </div>
          </div>
        )}

        <nav className="space-y-1">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <Icon className="h-4 w-4" />
                  <span>{link.label}</span>
                </div>
                {link.badge && (
                  <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                    {link.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      <div className="p-3 rounded-xl bg-gradient-to-br from-indigo-950/40 via-purple-950/20 to-slate-900 border border-indigo-900/40 text-[11px] text-slate-300">
        <div className="flex items-center gap-2 text-indigo-300 font-bold mb-1">
          <Sparkles className="h-3.5 w-3.5" />
          <span>Continuous Adaptive Loop</span>
        </div>
        <p className="text-slate-400 text-[10px] leading-relaxed">
          Dynamic routing automatically detects weak mental models and branches backward to re-teach prerequisites.
        </p>
      </div>
    </aside>
  );
};

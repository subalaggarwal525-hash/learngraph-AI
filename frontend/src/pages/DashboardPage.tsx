import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BarChart3, Flame, Zap, Award, Calendar, ArrowRight, Sparkles, CheckCircle2, TrendingUp, History } from 'lucide-react';
import { useCourse } from '../context/CourseContext';
import { analyticsApi } from '../services/api';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { setActiveConceptId, setSelectedTeachingMode } = useCourse();
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await analyticsApi.getDashboard();
        setDashboardData(data);
      } catch (err) {
        console.error('Dashboard error:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (isLoading || !dashboardData) {
    return (
      <div className="surface-card max-w-5xl mx-auto my-12 py-24 text-center text-slate-400 space-y-3">
        <Sparkles className="h-8 w-8 text-indigo-400 animate-spin mx-auto" />
        <p className="text-sm font-medium">Aggregating telemetry & cognitive retention schedules...</p>
      </div>
    );
  }

  const { user, stats, revision_schedule, weekly_activity, recent_attempts } = dashboardData;

  const maxMinutes = Math.max(...(weekly_activity || []).map((w: any) => w.minutes), 60);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* User Header Profile */}
      <div className="surface-card p-6 flex flex-wrap justify-between items-center gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl font-black text-white">{user.name}</h1>
            <span className="text-xs text-indigo-300 font-bold px-2.5 py-0.5 rounded-full bg-indigo-950/80 border border-indigo-800/60 font-mono">
              Tier Lvl {user.level}
            </span>
          </div>
          <p className="text-xs text-slate-400 font-mono">{user.email || 'learner@learngraph.ai'}</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="bg-slate-950/90 px-4 py-2.5 rounded-xl border border-amber-900/40 flex items-center gap-2.5 shadow-sm">
            <Flame className="h-5 w-5 text-amber-400 animate-pulse" />
            <div>
              <span className="text-[10px] text-slate-400 block uppercase font-bold leading-none">Learning Streak</span>
              <span className="text-sm font-black text-white">{user.streak_days} Days Active</span>
            </div>
          </div>

          <div className="bg-slate-950/90 px-4 py-2.5 rounded-xl border border-indigo-900/40 flex items-center gap-2.5 shadow-sm">
            <Zap className="h-5 w-5 text-indigo-400" />
            <div>
              <span className="text-[10px] text-slate-400 block uppercase font-bold leading-none">Total Experience</span>
              <span className="text-sm font-black text-indigo-300 font-mono">{user.xp} XP</span>
            </div>
          </div>
        </div>
      </div>

      {/* Primary KPI Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="surface-card p-5 space-y-1">
          <span className="text-[10px] uppercase font-bold text-slate-400 block">Overall Mastery</span>
          <span className="text-3xl font-black text-indigo-400 font-mono">{stats.overall_mastery}%</span>
          <span className="text-[10px] text-slate-500 block">Across all courses</span>
        </div>
        <div className="surface-card p-5 space-y-1">
          <span className="text-[10px] uppercase font-bold text-slate-400 block">Mastered Concepts</span>
          <span className="text-3xl font-black text-emerald-400 font-mono">{stats.mastered_concepts} / {stats.total_concepts}</span>
          <span className="text-[10px] text-slate-500 block">Verified in assessments</span>
        </div>
        <div className="surface-card p-5 space-y-1">
          <span className="text-[10px] uppercase font-bold text-slate-400 block">Quiz Accuracy</span>
          <span className="text-3xl font-black text-purple-400 font-mono">{stats.average_quiz_accuracy}%</span>
          <span className="text-[10px] text-slate-500 block">{stats.total_quiz_attempts || 1} diagnostic attempts</span>
        </div>
        <div className="surface-card p-5 space-y-1">
          <span className="text-[10px] uppercase font-bold text-slate-400 block">Study Velocity</span>
          <span className="text-3xl font-black text-amber-400 font-mono">{stats.learning_velocity_hours_this_week}h</span>
          <span className="text-[10px] text-slate-500 block">Invested this week</span>
        </div>
      </div>

      {/* Activity Bar Chart & Badges Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Activity Visualizer */}
        <div className="surface-card p-6 lg:col-span-2 space-y-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-indigo-400" />
              <h3 className="text-sm font-extrabold text-white">Weekly Learning Velocity & Time Spent</h3>
            </div>
            <span className="text-[11px] font-mono text-slate-400">{stats.learning_velocity_hours_this_week} Hours Total</span>
          </div>

          <div className="flex items-end justify-between gap-3 h-44 pt-4 px-2">
            {(weekly_activity || []).map((act: any, idx: number) => {
              const heightPct = Math.max(15, Math.round((act.minutes / maxMinutes) * 100));
              return (
                <div key={idx} className="flex-1 flex flex-col items-center gap-2 h-full justify-end group">
                  <div className="text-[10px] font-mono text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity">
                    {act.minutes}m
                  </div>
                  <div
                    style={{ height: `${heightPct}%` }}
                    className="w-full max-w-[36px] rounded-t-lg bg-gradient-to-t from-indigo-600 via-indigo-500 to-purple-500 group-hover:from-indigo-400 group-hover:to-purple-400 transition-all shadow-md shadow-indigo-600/20"
                  />
                  <span className="text-[11px] font-bold text-slate-400">{act.day}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Badges / Mastery Accomplishments */}
        <div className="surface-card p-6 space-y-4">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <Award className="h-4 w-4 text-amber-400" />
            <h3 className="text-sm font-extrabold text-white">Cognitive Badges</h3>
          </div>

          <div className="space-y-3">
            {(user.badges || []).map((b: any) => (
              <div key={b.id} className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center gap-3">
                <span className="text-2xl p-1.5 rounded-lg bg-slate-900 border border-slate-800">{b.icon}</span>
                <div>
                  <h4 className="text-xs font-bold text-white">{b.name}</h4>
                  <p className="text-[10px] text-slate-400 leading-tight mt-0.5">{b.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Automated Spaced Repetition Schedule */}
      <div className="surface-card p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-indigo-400" />
            <h3 className="text-sm font-extrabold text-white">Spaced Repetition & Retention Queue</h3>
          </div>
          <span className="text-xs text-slate-400">SM-2 Optimized Review Dates</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {revision_schedule.map((item: any) => (
            <div key={item.concept_id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-3 hover:border-slate-700 transition-all">
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] font-bold text-amber-400 uppercase bg-amber-950/50 px-2 py-0.5 rounded border border-amber-800/40">
                    Due {item.due_date}
                  </span>
                  <span className="text-[10px] text-slate-400 font-mono">
                    Risk: {Math.round(item.forgetting_risk * 100)}%
                  </span>
                </div>
                <h4 className="text-xs font-bold text-white mt-1">{item.concept_title}</h4>
              </div>
              <button
                onClick={() => { setActiveConceptId(item.concept_id); setSelectedTeachingMode(item.recommended_mode); navigate('/lesson'); }}
                className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold pt-2 border-t border-slate-800 block text-left"
              >
                Review Now ({item.recommended_mode.replace('_', ' ')}) →
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};


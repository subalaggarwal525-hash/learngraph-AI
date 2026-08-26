import React from 'react';
import { Link } from 'react-router-dom';
import { Network, Sparkles, ArrowRight, Layers, ShieldCheck, BookOpen, Brain, Cpu, Mic, Gauge, Compass } from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="relative overflow-hidden">
      {/* Background Decorative Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[500px] bg-gradient-to-b from-indigo-600/10 via-purple-600/5 to-transparent blur-3xl pointer-events-none -z-10" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20 text-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-700/80 text-xs font-semibold text-indigo-300 mb-8 shadow-sm">
          <Sparkles className="h-3.5 w-3.5 text-indigo-400" />
          <span>Continuous Adaptive AI Learning Engine</span>
        </div>

        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight text-white max-w-5xl mx-auto leading-[1.1]">
          Turn Any Subject Into an{' '}
          <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-amber-300 bg-clip-text text-transparent">
            Adaptive Knowledge Graph
          </span>
        </h1>

        <p className="mt-6 text-sm sm:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed">
          LearnGraph AI constructs topological prerequisite roadmaps, delivers 12 specialized teaching modalities, detects root-cause misconceptions, and tests true retention with the Feynman technique.
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/create"
            className="flex items-center gap-2 px-7 py-4 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm shadow-xl shadow-indigo-600/30 transition-all hover:scale-105"
          >
            <span>Start a Learning Journey</span>
            <ArrowRight className="h-4 w-4" />
          </Link>

          <Link
            to="/courses"
            className="flex items-center gap-2 px-6 py-4 rounded-xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 text-slate-200 font-semibold text-sm transition-all hover:bg-slate-800/80"
          >
            <BookOpen className="h-4 w-4 text-slate-400" />
            <span>Explore Saved Courses</span>
          </Link>
        </div>
      </div>

      {/* Handcrafted Asymmetrical Feature Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 border-t border-slate-800/80 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="surface-card p-6 space-y-3 border-indigo-500/30 bg-gradient-to-b from-indigo-950/20 to-slate-900">
          <div className="h-10 w-10 rounded-xl bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400">
            <Network className="h-5 w-5" />
          </div>
          <h3 className="text-base font-bold text-white">Topological Prerequisite DAGs</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Eliminates cognitive overload by enforcing strict foundational dependencies before unlocking advanced nodes.
          </p>
        </div>

        <div className="surface-card p-6 space-y-3 border-amber-500/30 bg-gradient-to-b from-amber-950/20 to-slate-900">
          <div className="h-10 w-10 rounded-xl bg-amber-600/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
            <Mic className="h-5 w-5" />
          </div>
          <h3 className="text-base font-bold text-white">Feynman "Explain It Back"</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Verify actual understanding by teaching concepts back in your own words with automated pedagogical feedback.
          </p>
        </div>

        <div className="surface-card p-6 space-y-3 border-emerald-500/30 bg-gradient-to-b from-emerald-950/20 to-slate-900">
          <div className="h-10 w-10 rounded-xl bg-emerald-600/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
            <Gauge className="h-5 w-5" />
          </div>
          <h3 className="text-base font-bold text-white">Confidence Calibration & Heatmaps</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Detect overconfidence and identify exact conceptual struggle zones before taking high-stakes assessments.
          </p>
        </div>
      </div>
    </div>
  );
};

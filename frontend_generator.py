import os

files = {}

files["frontend/package.json"] = '''{
  "name": "learngraph-ai-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.23.0",
    "reactflow": "^11.11.3",
    "lucide-react": "^0.378.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.3.0",
    "mermaid": "^10.9.1",
    "axios": "^1.6.8",
    "canvas-confetti": "^1.9.3"
  },
  "devDependencies": {
    "@types/react": "^18.3.2",
    "@types/react-dom": "^18.3.0",
    "@types/canvas-confetti": "^1.9.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.5",
    "vite": "^5.2.11"
  }
}'''

files["frontend/vite.config.ts"] = '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
});
'''

files["frontend/tailwind.config.js"] = '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
          950: '#1e1b4b',
        },
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
'''

files["frontend/postcss.config.js"] = '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''

files["frontend/tsconfig.json"] = '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
'''

files["frontend/tsconfig.node.json"] = '''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
'''

files["frontend/index.html"] = '''<!doctype html>
<html lang="en" class="dark">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='3'/><path d='M3 12h3m12 0h3M12 3v3m0 12v3'/></svg>" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>LearnGraph AI — Adaptive Learning Platform</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-950 text-slate-100 antialiased min-h-screen selection:bg-indigo-500 selection:text-white font-sans">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''

files["frontend/src/index.css"] = '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer utilities {
  .no-scrollbar::-webkit-scrollbar {
    display: none;
  }
  .no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
}

.react-flow__attribution {
  display: none !important;
}
.react-flow__edge-path {
  stroke: #6366f1 !important;
  stroke-width: 2.5px !important;
}
.react-flow__edge-text {
  fill: #a5b4fc !important;
  font-size: 10px !important;
  font-weight: 700 !important;
}
.react-flow__edge-textbg {
  fill: #0f172a !important;
  rx: 4px;
}
'''

files["frontend/src/types/index.ts"] = '''export type LearningGoal = 'exam' | 'interview' | 'deep_understanding' | 'project' | 'certification' | 'overview';
export type LearnerLevel = 'beginner' | 'intermediate' | 'advanced' | 'assess_me';
export type TeachingMode = 'simple' | 'eli5' | 'analogy' | 'diagram' | 'real_world' | 'worked_example' | 'mathematical' | 'code' | 'socratic' | 'comparison' | 'story' | 'challenge';
export type NodeStatus = 'locked' | 'available' | 'learning' | 'mastered' | 'needs_review' | 'skipped';

export interface Concept {
  id: string;
  course_id?: string;
  title: string;
  short_summary: string;
  difficulty: number;
  importance: number;
  estimated_minutes: number;
  status: NodeStatus;
  mastery_score: number;
  prerequisites: string[];
  learning_objectives: string[];
  common_misconceptions: string[];
  source_references?: string[];
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  type?: string;
  animated?: boolean;
}

export interface KnowledgeGraphData {
  nodes: any[];
  edges: GraphEdge[];
}

export interface RoadmapStage {
  stage_number: number;
  stage_name: string;
  concept_ids: string[];
  estimated_hours: number;
  description: string;
}

export interface RoadmapData {
  stages: RoadmapStage[];
  recommended_concept_id: string | null;
  total_concepts: number;
  completed_concepts: number;
  progress_percentage: number;
}

export interface VisualDiagram {
  diagram_type: 'mermaid' | 'react_flow' | 'svg';
  specification: string;
  caption: string;
  interactive_elements?: any[];
}

export interface LessonContent {
  id: string;
  concept_id: string;
  concept_title: string;
  mode: TeachingMode;
  learning_objective: string;
  prerequisite_reminder: string;
  simple_explanation: string;
  detailed_explanation: string;
  analogy: string;
  worked_example: string;
  visual_diagram?: VisualDiagram;
  code_example?: string;
  common_mistakes: string[];
  key_takeaways: string[];
  quick_checks: Array<{
    question: string;
    options: string[];
    correct_index: number;
    explanation: string;
  }>;
  deeper_dive?: string;
  source_citations: string[];
  simulation_type?: string | null;
}

export interface QuizQuestion {
  id: string;
  type: 'multiple_choice' | 'multiple_select' | 'short_answer' | 'scenario' | 'code' | 'ordering';
  prompt: string;
  options?: string[];
  correct_answer: number | number[] | string;
  explanation: string;
  concept_id: string;
  target_misconception?: string;
  difficulty: number;
}

export interface Quiz {
  id: string;
  concept_id: string;
  concept_title: string;
  questions: QuizQuestion[];
  pass_threshold: number;
}

export interface QuestionEvaluation {
  question_id: string;
  is_correct: boolean;
  score: number;
  user_answer: any;
  correct_answer: any;
  explanation: string;
  misconception_detected?: string;
  root_cause_prerequisite_id?: string;
}

export interface QuizEvaluationResult {
  quiz_id: string;
  concept_id: string;
  total_score: number;
  passed: boolean;
  correct_count: number;
  total_questions: number;
  evaluations: QuestionEvaluation[];
  feedback_summary: string;
  misconceptions: string[];
  weak_prerequisites: string[];
  next_action: 'next_concept' | 'remediation' | 'reteach_prerequisite';
  recommended_remediation?: string;
  updated_mastery: number;
  xp_earned: number;
}

export interface CuratedResource {
  id: string;
  title: string;
  url: string;
  type: 'video' | 'article' | 'documentation' | 'practice';
  duration_or_read_time: string;
  difficulty: string;
  relevance_score: number;
  covered_topics: string[];
  missing_topics: string[];
  coverage_percentage: number;
}

export interface SpacedReviewItem {
  concept_id: string;
  concept_title: string;
  due_date: string;
  forgetting_risk: number;
  stability: number;
  last_studied: string;
  recommended_mode: string;
}

export interface CourseDetail {
  id: string;
  title: string;
  source_type: string;
  source_summary: string;
  learning_goal: LearningGoal;
  current_level: LearnerLevel;
  created_at: string;
  concepts: Concept[];
  knowledge_graph: KnowledgeGraphData;
  roadmap: RoadmapData;
  mastery_profile: {
    overall_mastery: number;
    concepts_mastered: number;
    concepts_in_progress: number;
    concepts_locked: number;
    total_concepts: number;
    concept_scores: Record<string, number>;
    strongest_concepts: string[];
    weakest_concepts: string[];
    recent_accuracy: number;
    streak_days: number;
    total_xp: number;
    level: number;
  };
  revision_schedule: SpacedReviewItem[];
}
'''

files["frontend/src/services/api.ts"] = '''import axios from 'axios';
import { CourseDetail, LessonContent, Quiz, QuizEvaluationResult, CuratedResource, TeachingMode } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api';
const api = axios.create({ baseURL: API_BASE_URL, headers: { 'Content-Type': 'application/json' } });

export const courseApi = {
  listCourses: async () => (await api.get('/courses')).data,
  getCourse: async (courseId: string): Promise<CourseDetail> => (await api.get(`/courses/${courseId}`)).data,
  createCourse: async (payload: any) => (await api.post('/courses', payload)).data,
  getRoadmap: async (courseId: string) => (await api.get(`/courses/${courseId}/roadmap`)).data,
  getFinalTest: async (courseId: string) => (await api.post(`/courses/${courseId}/final-test`)).data,
};

export const lessonApi = {
  generateLesson: async (conceptId: string, mode: TeachingMode = 'simple'): Promise<LessonContent> =>
    (await api.post(`/lessons/${conceptId}/generate`, { mode })).data,
};

export const quizApi = {
  getQuiz: async (conceptId: string): Promise<Quiz> => (await api.get(`/quizzes/${conceptId}`)).data,
  submitQuiz: async (conceptId: string, payload: any): Promise<{ evaluation: QuizEvaluationResult; updated_knowledge_graph: any; updated_roadmap: any }> =>
    (await api.post(`/quizzes/${conceptId}/submit`, payload)).data,
};

export const tutorApi = {
  chat: async (payload: any) => (await api.post('/tutor/chat', payload)).data,
};

export const documentApi = {
  uploadDocument: async (courseId: string, file: File) => {
    const formData = new FormData();
    formData.append('course_id', courseId);
    formData.append('file', file);
    return (await api.post('/documents/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } })).data;
  },
};

export const sourceApi = {
  ingestUrl: async (url: string) => (await api.post('/sources/url', { url })).data,
};

export const resourceApi = {
  getCuratedResources: async (conceptId: string): Promise<CuratedResource[]> => (await api.get(`/resources/${conceptId}`)).data,
};

export const simulationApi = {
  getTypes: async () => (await api.get('/simulations/types')).data,
  getConfig: async (simType: string) => (await api.get(`/simulations/${simType}/config`)).data,
};

export const analyticsApi = {
  getDashboard: async (userId: string = 'demo_user') => (await api.get('/analytics/dashboard', { params: { user_id: userId } })).data,
};

export default api;
'''

files["frontend/src/context/CourseContext.tsx"] = '''import React, { createContext, useContext, useState } from 'react';
import { CourseDetail } from '../types';
import { courseApi } from '../services/api';

interface CourseContextType {
  activeCourse: CourseDetail | null;
  activeConceptId: string | null;
  setActiveConceptId: (id: string | null) => void;
  loadCourse: (courseId: string) => Promise<void>;
  refreshCourse: () => Promise<void>;
  userXP: number;
  userLevel: number;
  userStreak: number;
  addXP: (amount: number) => void;
  isTutorOpen: boolean;
  setIsTutorOpen: (open: boolean) => void;
  selectedTeachingMode: string;
  setSelectedTeachingMode: (mode: string) => void;
}

const CourseContext = createContext<CourseContextType | undefined>(undefined);

export const CourseProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeCourse, setActiveCourse] = useState<CourseDetail | null>(null);
  const [activeConceptId, setActiveConceptId] = useState<string | null>(null);
  const [userXP, setUserXP] = useState<number>(450);
  const [userLevel, setUserLevel] = useState<number>(2);
  const [userStreak, setUserStreak] = useState<number>(4);
  const [isTutorOpen, setIsTutorOpen] = useState<boolean>(false);
  const [selectedTeachingMode, setSelectedTeachingMode] = useState<string>('simple');

  const loadCourse = async (courseId: string) => {
    try {
      const data = await courseApi.getCourse(courseId);
      setActiveCourse(data);
      if (data.roadmap?.recommended_concept_id) {
        setActiveConceptId(data.roadmap.recommended_concept_id);
      } else if (data.concepts && data.concepts.length > 0) {
        setActiveConceptId(data.concepts[0].id);
      }
    } catch (err) {
      console.error('Failed to load course:', err);
    }
  };

  const refreshCourse = async () => {
    if (activeCourse) await loadCourse(activeCourse.id);
  };

  const addXP = (amount: number) => {
    setUserXP((prev) => {
      const updated = prev + amount;
      setUserLevel(Math.max(1, Math.floor(updated / 250) + 1));
      return updated;
    });
  };

  return (
    <CourseContext.Provider
      value={{
        activeCourse,
        activeConceptId,
        setActiveConceptId,
        loadCourse,
        refreshCourse,
        userXP,
        userLevel,
        userStreak,
        addXP,
        isTutorOpen,
        setIsTutorOpen,
        selectedTeachingMode,
        setSelectedTeachingMode,
      }}
    >
      {children}
    </CourseContext.Provider>
  );
};

export const useCourse = () => {
  const context = useContext(CourseContext);
  if (!context) throw new Error('useCourse must be used within CourseProvider');
  return context;
};
'''

files["frontend/src/components/Navbar.tsx"] = '''import React from 'react';
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
'''

files["frontend/src/components/Sidebar.tsx"] = '''import React from 'react';
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
'''

files["frontend/src/components/DiagramRenderer.tsx"] = '''import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';

interface DiagramRendererProps {
  specification: string;
  caption?: string;
  className?: string;
}

export const DiagramRenderer: React.FC<DiagramRendererProps> = ({
  specification,
  caption,
  className = '',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [svgContent, setSvgContent] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'dark',
      securityLevel: 'loose',
      fontFamily: 'Plus Jakarta Sans, sans-serif',
      themeVariables: {
        darkMode: true,
        background: '#090d16',
        primaryColor: '#6366f1',
        primaryTextColor: '#f8fafc',
        primaryBorderColor: '#4f46e5',
        lineColor: '#818cf8',
      },
    });

    const renderDiagram = async () => {
      try {
        setError(null);
        const uniqueId = `mermaid_${Math.random().toString(36).substr(2, 9)}`;
        const cleanSpec = specification.replace(/\\\\n/g, '\\n').trim();
        const { svg } = await mermaid.render(uniqueId, cleanSpec);
        setSvgContent(svg);
      } catch (err: any) {
        setError('Diagram parsing preview');
      }
    };

    if (specification) renderDiagram();
  }, [specification]);

  return (
    <div className={`rounded-xl border border-slate-800 bg-slate-950 p-4 shadow-xl ${className}`}>
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5 mb-3 text-xs text-slate-400">
        <span className="font-semibold text-indigo-400 flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-indigo-500 animate-ping" />
          Structured Visual Model
        </span>
        <span className="text-[10px] bg-slate-900 px-2 py-0.5 rounded border border-slate-800 font-mono">
          Mermaid / SVG
        </span>
      </div>

      {error ? (
        <div className="p-4 rounded-lg bg-slate-900 text-xs font-mono text-slate-300 overflow-x-auto whitespace-pre">
          {specification}
        </div>
      ) : (
        <div
          ref={containerRef}
          className="overflow-x-auto flex justify-center py-2 diagram-container [&_svg]:max-w-full [&_svg]:h-auto"
          dangerouslySetInnerHTML={{ __html: svgContent }}
        />
      )}

      {caption && (
        <p className="mt-3 text-center text-xs text-slate-400 font-medium italic border-t border-slate-800/60 pt-2">
          {caption}
        </p>
      )}
    </div>
  );
};
'''

files["frontend/src/components/AITutorWidget.tsx"] = '''import React, { useState } from 'react';
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
'''

files["frontend/src/components/simulations/MemoryPagingSimulation.tsx"] = '''import React, { useState } from 'react';
import { Cpu, Layers, HardDrive, CheckCircle2, AlertTriangle } from 'lucide-react';

export const MemoryPagingSimulation: React.FC = () => {
  const [virtualAddress, setVirtualAddress] = useState<string>('0x00403010');
  const [tlbEnabled, setTlbEnabled] = useState<boolean>(true);

  const cleanHex = virtualAddress.startsWith('0x') ? virtualAddress.slice(2) : virtualAddress;
  const intVal = parseInt(cleanHex, 16) || 0;
  const offset = intVal & 0xFFF;
  const vpn = (intVal >> 12) & 0xFFFFF;

  const vpnHex = '0x' + vpn.toString(16).toUpperCase().padStart(5, '0');
  const offsetHex = '0x' + offset.toString(16).toUpperCase().padStart(3, '0');

  const pageTableMapping: Record<string, { frame: string; valid: boolean; dirty: boolean }> = {
    '0x00403': { frame: '0x0812', valid: true, dirty: false },
    '0x00A05': { frame: '0x0234', valid: true, dirty: true },
    '0x00100': { frame: '0x0000', valid: false, dirty: false },
  };

  const tlbCache: Record<string, string> = { '0x00403': '0x0812' };
  const isTlbHit = tlbEnabled && !!tlbCache[vpnHex];
  const tableEntry = pageTableMapping[vpnHex];
  const isValid = tableEntry?.valid ?? false;
  const frameNumber = isTlbHit ? tlbCache[vpnHex] : tableEntry ? tableEntry.frame : '0x0999';
  const physicalAddress = isValid
    ? '0x' + ((parseInt(frameNumber.slice(2), 16) << 12) | offset).toString(16).toUpperCase().padStart(7, '0')
    : 'PAGE_FAULT';

  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Layers className="h-5 w-5 text-indigo-400" />
            Interactive MMU & Paging Simulation
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Test real-time 32-bit virtual address bit-splitting, TLB lookups, page tables, and physical RAM frame translation.
          </p>
        </div>
        <button
          onClick={() => setTlbEnabled(!tlbEnabled)}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
            tlbEnabled ? 'bg-indigo-600/30 text-indigo-300 border-indigo-500/50' : 'bg-slate-800 text-slate-400 border-slate-700'
          }`}
        >
          TLB Cache: {tlbEnabled ? 'ON' : 'OFF'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-950 p-4 rounded-xl border border-slate-800/80">
        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1.5">Virtual Memory Address</label>
          <input
            type="text"
            value={virtualAddress}
            onChange={(e) => setVirtualAddress(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1.5">Quick Presets</label>
          <div className="flex gap-2">
            {['0x00403010', '0x00A05024', '0x00100004'].map((addr) => (
              <button key={addr} onClick={() => setVirtualAddress(addr)} className="px-2.5 py-2 rounded-lg bg-slate-900 border border-slate-800 hover:border-indigo-500 text-xs font-mono text-slate-300">
                {addr}
              </button>
            ))}
          </div>
        </div>
        <div className="flex flex-col justify-center">
          <span className="text-[11px] text-slate-400">Page Configuration</span>
          <span className="text-xs font-semibold text-slate-200">Page Size: 4 KB (2¹² B) | Offset: 12b | VPN: 20b</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-slate-950/80 border border-indigo-500/30 flex flex-col justify-between">
          <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <Cpu className="h-4 w-4" /> 1. CPU Virtual Address
          </div>
          <div className="font-mono text-base font-extrabold text-white">{virtualAddress}</div>
          <div className="mt-3 pt-3 border-t border-slate-800 grid grid-cols-2 gap-2 text-xs font-mono">
            <div className="bg-indigo-950/50 p-2 rounded border border-indigo-800/40">
              <span className="text-[10px] text-slate-400 block">VPN (20b)</span>
              <span className="text-indigo-300 font-bold">{vpnHex}</span>
            </div>
            <div className="bg-purple-950/50 p-2 rounded border border-purple-800/40">
              <span className="text-[10px] text-slate-400 block">Offset (12b)</span>
              <span className="text-purple-300 font-bold">{offsetHex}</span>
            </div>
          </div>
        </div>

        <div className={`p-4 rounded-xl bg-slate-950/80 border flex flex-col justify-between ${
          isTlbHit ? 'border-emerald-500/50 bg-emerald-950/10' : 'border-slate-800'
        }`}>
          <div className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>2. TLB Cache</span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${isTlbHit ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'}`}>
              {isTlbHit ? 'HIT (0.5 ns)' : 'MISS'}
            </span>
          </div>
          <div className="text-xs text-slate-400">{isTlbHit ? `Translation VPN ${vpnHex} -> Frame ${frameNumber}` : 'TLB miss occurred. Accessing Page Table in RAM...'}</div>
        </div>

        <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 flex flex-col justify-between">
          <div className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">3. Page Table Entry</div>
          {tableEntry ? (
            <div className="space-y-1.5 text-xs font-mono">
              <div className="flex justify-between"><span className="text-slate-400">Frame:</span><span className="text-emerald-400 font-bold">{tableEntry.frame}</span></div>
              <div className="flex justify-between"><span className="text-slate-400">Valid:</span><span className={tableEntry.valid ? 'text-emerald-400' : 'text-rose-400 font-bold'}>{tableEntry.valid ? '1' : '0 (Fault)'}</span></div>
            </div>
          ) : (
            <div className="text-xs text-slate-400">Simulated Frame: <span className="font-mono text-emerald-400">0x0999</span></div>
          )}
        </div>

        <div className={`p-4 rounded-xl border flex flex-col justify-between ${
          isValid ? 'bg-gradient-to-br from-emerald-950/30 to-slate-950 border-emerald-500/40' : 'bg-gradient-to-br from-rose-950/30 to-slate-950 border-rose-500/40'
        }`}>
          <div className="text-xs font-bold text-slate-200 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <HardDrive className="h-4 w-4 text-emerald-400" /> 4. Physical RAM
          </div>
          {isValid ? (
            <div>
              <span className="text-[11px] text-slate-400 block">Physical Address:</span>
              <div className="font-mono text-lg font-black text-emerald-300">{physicalAddress}</div>
              <div className="mt-2 text-[11px] text-emerald-400/90 flex items-center gap-1">
                <CheckCircle2 className="h-3.5 w-3.5" /> Frame {frameNumber} + Offset {offsetHex}
              </div>
            </div>
          ) : (
            <div>
              <div className="font-mono text-base font-black text-rose-400 flex items-center gap-1.5">
                <AlertTriangle className="h-4 w-4" /> PAGE FAULT
              </div>
              <p className="mt-1 text-[11px] text-rose-300">Interrupts OS to load page from swap.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
'''

files["frontend/src/components/simulations/CPUSchedulingSimulation.tsx"] = '''import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Clock, Cpu } from 'lucide-react';

interface Process { id: string; name: string; arrival: number; burst: number; remaining: number; color: string; }

export const CPUSchedulingSimulation: React.FC = () => {
  const [algorithm, setAlgorithm] = useState<'RR' | 'FCFS' | 'SJF'>('RR');
  const [quantum, setQuantum] = useState<number>(2);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [ganttChart, setGanttChart] = useState<Array<{ pid: string; color: string; time: number }>>([]);

  const defaultProcesses: Process[] = [
    { id: 'P1', name: 'Process 1 (DB Query)', arrival: 0, burst: 5, remaining: 5, color: '#3b82f6' },
    { id: 'P2', name: 'Process 2 (Image Render)', arrival: 1, burst: 3, remaining: 3, color: '#10b981' },
    { id: 'P3', name: 'Process 3 (HTTP Handler)', arrival: 2, burst: 6, remaining: 6, color: '#f59e0b' },
    { id: 'P4', name: 'Process 4 (Audio Stream)', arrival: 4, burst: 2, remaining: 2, color: '#ec4899' },
  ];

  const [processes, setProcesses] = useState<Process[]>(defaultProcesses);

  const reset = () => {
    setIsRunning(false);
    setCurrentTime(0);
    setGanttChart([]);
    setProcesses(defaultProcesses.map((p) => ({ ...p })));
  };

  useEffect(() => {
    let timer: any;
    if (isRunning) {
      timer = setInterval(() => {
        setProcesses((prev) => {
          const available = prev.filter((p) => p.arrival <= currentTime && p.remaining > 0);
          if (available.length === 0) {
            const anyRemaining = prev.some((p) => p.remaining > 0);
            if (!anyRemaining) setIsRunning(false);
            else setCurrentTime((t) => t + 1);
            return prev;
          }

          let selected: Process = available[0];
          if (algorithm === 'SJF') selected = [...available].sort((a, b) => a.remaining - b.remaining)[0];
          else if (algorithm === 'RR') {
            const index = Math.floor(currentTime / quantum) % available.length;
            selected = available[index];
          }

          setGanttChart((g) => [...g, { pid: selected.id, color: selected.color, time: currentTime }]);
          setCurrentTime((t) => t + 1);

          return prev.map((p) => p.id === selected.id ? { ...p, remaining: Math.max(0, p.remaining - 1) } : p);
        });
      }, 600);
    }
    return () => clearInterval(timer);
  }, [isRunning, currentTime, algorithm, quantum]);

  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Cpu className="h-5 w-5 text-indigo-400" />
            Live CPU Scheduler & Gantt Chart
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Simulate Round Robin, First-Come First-Served, and Shortest Job First with real-time state dispatching.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800">
            {(['RR', 'FCFS', 'SJF'] as const).map((algo) => (
              <button
                key={algo}
                onClick={() => { setAlgorithm(algo); reset(); }}
                className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
                  algorithm === algo ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {algo === 'RR' ? 'Round Robin' : algo}
              </button>
            ))}
          </div>

          <button
            onClick={() => setIsRunning(!isRunning)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow"
          >
            {isRunning ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
            {isRunning ? 'Pause' : 'Start Simulation'}
          </button>
          <button onClick={reset} className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs">
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        {processes.map((p) => {
          const pct = Math.round(((p.burst - p.remaining) / p.burst) * 100);
          const isDone = p.remaining === 0;
          return (
            <div key={p.id} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full" style={{ backgroundColor: p.color }} />
                  <span className="font-bold text-xs text-slate-200">{p.id}</span>
                </div>
                <span className="text-[10px] px-1.5 py-0.5 rounded font-semibold bg-indigo-950 text-indigo-300">
                  {isDone ? 'Done' : `Rem: ${p.remaining}s`}
                </span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
                <div className="h-1.5 rounded-full transition-all duration-300" style={{ width: `${pct}%`, backgroundColor: p.color }} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
        <div className="text-xs text-slate-400 mb-3 flex items-center gap-1.5">
          <Clock className="h-4 w-4 text-indigo-400" />
          Execution Timeline (Time: {currentTime}s)
        </div>
        {ganttChart.length === 0 ? (
          <div className="h-14 flex items-center justify-center text-xs text-slate-500 border border-dashed border-slate-800 rounded-lg">
            Click 'Start Simulation' to watch CPU scheduling
          </div>
        ) : (
          <div className="flex overflow-x-auto gap-1 py-1">
            {ganttChart.map((block, idx) => (
              <div key={idx} className="flex-shrink-0 w-10 h-12 rounded-lg flex flex-col items-center justify-center text-xs font-bold text-white shadow-sm" style={{ backgroundColor: block.color }}>
                <span>{block.pid}</span>
                <span className="text-[9px] opacity-80">{block.time}s</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
'''

files["frontend/src/components/simulations/SortingSimulation.tsx"] = '''import React, { useState } from 'react';
import { Play, RotateCcw, BarChart2 } from 'lucide-react';

export const SortingSimulation: React.FC = () => {
  const [array, setArray] = useState<number[]>([48, 15, 82, 34, 91, 23, 67, 5, 53, 76]);
  const [activeIndices, setActiveIndices] = useState<number[]>([]);
  const [isSorting, setIsSorting] = useState<boolean>(false);

  const reset = () => {
    setIsSorting(false);
    setActiveIndices([]);
    setArray([48, 15, 82, 34, 91, 23, 67, 5, 53, 76]);
  };

  const bubbleSort = async () => {
    setIsSorting(true);
    let arr = [...array];
    const n = arr.length;
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n - i - 1; j++) {
        setActiveIndices([j, j + 1]);
        await new Promise((r) => setTimeout(r, 180));
        if (arr[j] > arr[j + 1]) {
          const temp = arr[j];
          arr[j] = arr[j + 1];
          arr[j + 1] = temp;
          setArray([...arr]);
        }
      }
    }
    setActiveIndices([]);
    setIsSorting(false);
  };

  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <BarChart2 className="h-5 w-5 text-indigo-400" />
            Sorting Algorithm Visualizer
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Step-by-step comparative animation showing element comparisons and swaps.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={bubbleSort}
            disabled={isSorting}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-bold shadow"
          >
            <Play className="h-3.5 w-3.5" />
            {isSorting ? 'Sorting...' : 'Animate Bubble Sort'}
          </button>
          <button onClick={reset} disabled={isSorting} className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs">
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="h-48 bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-end justify-center gap-3">
        {array.map((val, idx) => {
          const isActive = activeIndices.includes(idx);
          return (
            <div key={idx} className="flex flex-col items-center gap-1 flex-1 max-w-[40px]">
              <span className="text-[10px] font-mono text-slate-400">{val}</span>
              <div
                className={`w-full rounded-t-lg transition-all duration-200 ${
                  isActive ? 'bg-amber-400 shadow-lg shadow-amber-400/40 scale-105' : 'bg-indigo-600'
                }`}
                style={{ height: `${val * 1.5}px` }}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};
'''

files["frontend/src/components/simulations/NetworkPacketSimulation.tsx"] = '''import React, { useState } from 'react';
import { Send } from 'lucide-react';

export const NetworkPacketSimulation: React.FC = () => {
  const [step, setStep] = useState<number>(0);
  const steps = [
    { name: 'Initial State', clientState: 'CLOSED', serverState: 'LISTEN', description: 'Server listens on port 80/443. Client prepares initial SYN packet.' },
    { name: 'Step 1: SYN', clientState: 'SYN_SENT', serverState: 'LISTEN', description: 'Client sends SYN (Seq=100) requesting connection.' },
    { name: 'Step 2: SYN-ACK', clientState: 'SYN_SENT', serverState: 'SYN_RCVD', description: 'Server acknowledges client Seq (Ack=101) and sends SYN (Seq=300).' },
    { name: 'Step 3: ACK', clientState: 'ESTABLISHED', serverState: 'ESTABLISHED', description: 'Client acknowledges server Seq (Ack=301). Connection is fully ESTABLISHED.' },
  ];

  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Send className="h-5 w-5 text-indigo-400" />
            TCP 3-Way Handshake & Packet Transmission
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">Visualize packet exchange, sequence numbers, and socket state machine.</p>
        </div>
        <button
          onClick={() => setStep((s) => (s < 3 ? s + 1 : 0))}
          className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-xs font-bold text-white shadow"
        >
          {step === 3 ? 'Reset Handshake' : 'Next Packet Step'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-950 p-6 rounded-xl border border-slate-800">
        <div className="p-4 rounded-xl bg-slate-900 border border-indigo-500/30 text-center space-y-2">
          <div className="text-xs font-bold text-indigo-400 uppercase">Client (192.168.1.50)</div>
          <div className="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold bg-indigo-950 text-indigo-300">
            {steps[step].clientState}
          </div>
        </div>
        <div className="p-4 rounded-xl bg-slate-900 border border-purple-500/30 text-center space-y-2">
          <div className="text-xs font-bold text-purple-400 uppercase">Server (142.250.190.46)</div>
          <div className="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold bg-purple-950 text-purple-300">
            {steps[step].serverState}
          </div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 flex items-center gap-4">
        <div className="h-10 w-10 rounded-xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center font-bold text-base shrink-0">
          {step}
        </div>
        <div>
          <h4 className="text-xs font-bold text-slate-200">{steps[step].name}</h4>
          <p className="text-xs text-slate-400 mt-0.5">{steps[step].description}</p>
        </div>
      </div>
    </div>
  );
};
'''

files["frontend/src/pages/LandingPage.tsx"] = '''import React from 'react';
import { Link } from 'react-router-dom';
import { Network, Sparkles, ArrowRight, Layers, ShieldCheck, BookOpen } from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-950/60 border border-indigo-800/60 text-xs font-semibold text-indigo-300 mb-8 shadow-sm">
          <Sparkles className="h-3.5 w-3.5 text-indigo-400" />
          <span>Next-Generation Adaptive AI University</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
          Turn Any Source Into a{' '}
          <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Living Knowledge Graph
          </span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
          LearnGraph AI decomposes topics, textbooks, YouTube videos, and documentation into topological prerequisite roadmaps, structured lessons with 12 adaptive teaching styles, and real-time misconception diagnosis.
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/create"
            className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm shadow-lg shadow-indigo-500/25 transition-all hover:scale-105"
          >
            Start a Learning Journey
            <ArrowRight className="h-4 w-4" />
          </Link>

          <Link
            to="/courses"
            className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-semibold text-sm transition-colors"
          >
            <BookOpen className="h-4 w-4 text-slate-400" />
            Explore Saved Courses
          </Link>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 border-t border-slate-900 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-xl space-y-3">
          <div className="h-10 w-10 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Network className="h-5 w-5" />
          </div>
          <h3 className="text-base font-bold text-white">Topological Prerequisite Engine</h3>
          <p className="text-xs text-slate-400">Orders dependencies into DAGs to prevent cognitive overload.</p>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-xl space-y-3">
          <div className="h-10 w-10 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <Layers className="h-5 w-5" />
          </div>
          <h3 className="text-base font-bold text-white">12 Adaptive Teaching Styles</h3>
          <p className="text-xs text-slate-400">Switch dynamically between ELI5, Deep Analogies, Code, and Simulations.</p>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-xl space-y-3">
          <div className="h-10 w-10 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="h-5 w-5" />
          </div>
          <h3 className="text-base font-bold text-white">Misconception Detection</h3>
          <p className="text-xs text-slate-400">Diagnoses root-cause mental model flaws and loops back to re-teach.</p>
        </div>
      </div>
    </div>
  );
};
'''

files["frontend/src/pages/CreateJourneyPage.tsx"] = '''import React, { useState } from 'react';
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
'''

files["frontend/src/pages/AnalysisPage.tsx"] = '''import React, { useEffect, useState } from 'react';
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
'''

files["frontend/src/pages/KnowledgeGraphPage.tsx"] = '''import React, { useState, useCallback, useMemo } from 'react';
import ReactFlow, { Background, Controls, MiniMap, NodeProps, Handle, Position, useNodesState, useEdgesState } from 'reactflow';
import 'reactflow/dist/style.css';
import { useNavigate } from 'react-router-dom';
import { Lock, CheckCircle, Play, AlertTriangle, BookOpen, HelpCircle } from 'lucide-react';
import { useCourse } from '../context/CourseContext';

const CustomConceptNode: React.FC<NodeProps> = ({ data, selected }) => {
  const status = data.status || 'locked';
  const mastery = data.mastery_score || 0;

  const statusStyles = {
    locked: 'bg-slate-900/90 border-slate-800 text-slate-500 opacity-60',
    available: 'bg-indigo-950/80 border-indigo-500/80 text-slate-100 ring-2 ring-indigo-500/30',
    learning: 'bg-amber-950/80 border-amber-500 text-amber-200 ring-2 ring-amber-500/40',
    mastered: 'bg-emerald-950/80 border-emerald-500 text-emerald-100 ring-2 ring-emerald-500/40',
    needs_review: 'bg-rose-950/80 border-rose-500 text-rose-200 ring-2 ring-rose-500/40',
  };

  return (
    <div className={`px-4 py-3 rounded-2xl border shadow-xl min-w-[220px] max-w-[260px] cursor-pointer transition-all ${statusStyles[status as keyof typeof statusStyles] || statusStyles.locked} ${selected ? 'ring-4 ring-white/50 scale-105' : ''}`}>
      <Handle type="target" position={Position.Top} className="!bg-indigo-400 !w-2 !h-2" />
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-[10px] font-bold uppercase">{status}</span>
        <span className="text-[10px] font-mono font-bold bg-black/40 px-1.5 py-0.5 rounded">{mastery}%</span>
      </div>
      <div className="text-xs font-extrabold line-clamp-2">{data.title}</div>
      <div className="mt-2 flex items-center justify-between text-[10px] opacity-75 border-t border-white/10 pt-1.5">
        <span>⏱️ {data.estimated_minutes || 20}m</span>
        <span>Diff: {'★'.repeat(data.difficulty || 2)}</span>
      </div>
      <Handle type="source" position={Position.Bottom} className="!bg-indigo-400 !w-2 !h-2" />
    </div>
  );
};

export const KnowledgeGraphPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, setActiveConceptId } = useCourse();
  const nodeTypes = useMemo(() => ({ conceptNode: CustomConceptNode }), []);
  const [selectedNodeData, setSelectedNodeData] = useState<any>(null);

  const initialNodes = useMemo(() => activeCourse?.knowledge_graph?.nodes || [], [activeCourse]);
  const initialEdges = useMemo(() => (activeCourse?.knowledge_graph?.edges || []).map((e) => ({ ...e, style: { stroke: '#6366f1', strokeWidth: 2 } })), [activeCourse]);

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  const onNodeClick = useCallback((_: any, node: any) => {
    setSelectedNodeData(node.data);
    setActiveConceptId(node.id);
  }, [setActiveConceptId]);

  if (!activeCourse) return <div className="p-12 text-center text-slate-400">Please select a course first.</div>;

  return (
    <div className="relative h-[calc(100vh-4rem)] w-full flex flex-col">
      <div className="p-4 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between z-10">
        <h2 className="text-base font-black text-white">{activeCourse.title} — Knowledge Graph</h2>
        <div className="flex gap-2 text-[10px]">
          <span className="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-800 text-emerald-300">✓ Mastered</span>
          <span className="px-2 py-0.5 rounded bg-indigo-950 border border-indigo-800 text-indigo-300">▶ Available</span>
          <span className="px-2 py-0.5 rounded bg-rose-950 border border-rose-800 text-rose-300">! Needs Review</span>
          <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">🔒 Locked</span>
        </div>
      </div>

      <div className="flex-1 w-full h-full relative">
        <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onNodeClick={onNodeClick} nodeTypes={nodeTypes} fitView className="bg-slate-950">
          <Background color="#1e293b" gap={20} size={1} />
          <Controls className="!bg-slate-900 !border-slate-800 !text-white" />
          <MiniMap className="!bg-slate-900/90 !border-slate-800" />
        </ReactFlow>

        {selectedNodeData && (
          <div className="absolute top-4 right-4 z-20 w-80 bg-slate-900/95 border border-slate-800 rounded-2xl p-5 shadow-2xl backdrop-blur-md">
            <div className="flex justify-between mb-2">
              <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-indigo-950 text-indigo-300">{selectedNodeData.status}</span>
              <button onClick={() => setSelectedNodeData(null)} className="text-slate-400 text-xs">✕</button>
            </div>
            <h3 className="text-sm font-bold text-white mb-1">{selectedNodeData.title}</h3>
            <p className="text-xs text-slate-300 mb-4">{selectedNodeData.short_summary}</p>
            <div className="flex gap-2">
              <button onClick={() => { setActiveConceptId(selectedNodeData.id); navigate('/lesson'); }} className="flex-1 py-2 rounded-xl bg-indigo-600 text-white text-xs font-bold flex items-center justify-center gap-1.5">
                <BookOpen className="h-3.5 w-3.5" /> Open Lesson
              </button>
              <button onClick={() => { setActiveConceptId(selectedNodeData.id); navigate('/quiz'); }} className="flex-1 py-2 rounded-xl bg-slate-800 text-slate-200 text-xs font-bold flex items-center justify-center gap-1.5">
                <HelpCircle className="h-3.5 w-3.5" /> Quiz
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
'''

files["frontend/src/pages/RoadmapPage.tsx"] = '''import React from 'react';
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
'''

files["frontend/src/pages/LessonPage.tsx"] = '''import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Sparkles, HelpCircle, Code, Lightbulb, CheckCircle2, ArrowRight, MessageSquare, Youtube } from 'lucide-react';
import { useCourse } from '../context/CourseContext';
import { lessonApi, resourceApi } from '../services/api';
import { LessonContent, CuratedResource, TeachingMode } from '../types';
import { DiagramRenderer } from '../components/DiagramRenderer';
import { MemoryPagingSimulation } from '../components/simulations/MemoryPagingSimulation';
import { CPUSchedulingSimulation } from '../components/simulations/CPUSchedulingSimulation';
import { SortingSimulation } from '../components/simulations/SortingSimulation';
import { NetworkPacketSimulation } from '../components/simulations/NetworkPacketSimulation';

export const LessonPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, activeConceptId, setIsTutorOpen, selectedTeachingMode, setSelectedTeachingMode } = useCourse();
  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [resources, setResources] = useState<CuratedResource[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const activeConcept = (activeCourse?.concepts || []).find((c) => c.id === activeConceptId) || activeCourse?.concepts?.[0];

  const teachingModes: Array<{ id: TeachingMode; label: string; icon: string }> = [
    { id: 'simple', label: 'Simple', icon: '📝' },
    { id: 'eli5', label: 'ELI5', icon: '🧒' },
    { id: 'analogy', label: 'Analogy', icon: '🏛️' },
    { id: 'worked_example', label: 'Worked Example', icon: '🔢' },
    { id: 'code', label: 'Code', icon: '💻' },
    { id: 'mathematical', label: 'Math', icon: '📐' },
    { id: 'socratic', label: 'Socratic', icon: '🤔' },
  ];

  useEffect(() => {
    const fetchLesson = async () => {
      if (!activeConcept) return;
      setIsLoading(true);
      try {
        const [lData, rData] = await Promise.all([
          lessonApi.generateLesson(activeConcept.id, selectedTeachingMode as TeachingMode),
          resourceApi.getCuratedResources(activeConcept.id)
        ]);
        setLesson(lData);
        setResources(rData);
      } catch (err) {
        console.error('Lesson load error:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchLesson();
  }, [activeConcept?.id, selectedTeachingMode]);

  if (!activeCourse || !activeConcept) return <div className="p-12 text-center text-slate-400">Please select a course concept first.</div>;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
          <div>
            <span className="text-xs text-indigo-400 font-semibold">{activeCourse.title}</span>
            <h1 className="text-2xl font-black text-white">{activeConcept.title}</h1>
          </div>
          <div className="flex gap-2">
            <button onClick={() => setIsTutorOpen(true)} className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-purple-950/60 text-purple-300 text-xs font-bold border border-purple-800/60">
              <MessageSquare className="h-4 w-4" /> Ask AI Tutor
            </button>
            <button onClick={() => navigate('/quiz')} className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-bold shadow">
              <HelpCircle className="h-4 w-4" /> Take Quiz
            </button>
          </div>
        </div>

        <div>
          <div className="text-[11px] font-bold uppercase text-slate-400 mb-2">Adaptive Teaching Style:</div>
          <div className="flex gap-2 overflow-x-auto pb-1 no-scrollbar">
            {teachingModes.map((m) => (
              <button
                key={m.id}
                onClick={() => setSelectedTeachingMode(m.id)}
                className={`px-3 py-1.5 rounded-xl border text-xs font-semibold flex items-center gap-1.5 ${
                  selectedTeachingMode === m.id ? 'bg-indigo-600 text-white border-indigo-500 shadow' : 'bg-slate-950/60 border-slate-800 text-slate-400'
                }`}
              >
                <span>{m.icon}</span>
                <span>{m.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {isLoading || !lesson ? (
        <div className="py-20 text-center text-slate-400 space-y-3">
          <Sparkles className="h-8 w-8 text-indigo-400 animate-spin mx-auto" />
          <p className="text-sm">Synthesizing lesson in {selectedTeachingMode} mode...</p>
        </div>
      ) : (
        <div className="space-y-8">
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-indigo-400" /> Explanation ({lesson.mode.toUpperCase()})
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-4 rounded-xl border border-slate-800/80">
              {lesson.simple_explanation}
            </p>
            <p className="text-xs text-slate-300 leading-relaxed">{lesson.detailed_explanation}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
              <h4 className="text-xs font-bold text-purple-400 flex items-center gap-2"><Lightbulb className="h-4 w-4" /> Analogy</h4>
              <p className="text-xs text-slate-300">{lesson.analogy}</p>
            </div>
            <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
              <h4 className="text-xs font-bold text-emerald-400 flex items-center gap-2"><Code className="h-4 w-4" /> Worked Example</h4>
              <div className="text-xs text-slate-300 font-mono bg-slate-950 p-3 rounded-xl border border-slate-800 whitespace-pre-wrap">{lesson.worked_example}</div>
            </div>
          </div>

          {lesson.visual_diagram && <DiagramRenderer specification={lesson.visual_diagram.specification} caption={lesson.visual_diagram.caption} />}
          {lesson.simulation_type === 'memory_paging' && <MemoryPagingSimulation />}
          {lesson.simulation_type === 'cpu_scheduling' && <CPUSchedulingSimulation />}
          {lesson.simulation_type === 'sorting' && <SortingSimulation />}
          {lesson.simulation_type === 'network_packet' && <NetworkPacketSimulation />}

          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
              <Youtube className="h-4 w-4 text-rose-400" /> Curated Resources & Video Coverage
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {resources.map((res) => (
                <div key={res.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-3">
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-300">{res.type}</span>
                      <span className="text-[11px] font-mono font-bold text-emerald-400 bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-800/40">{res.coverage_percentage}% Concept Coverage</span>
                    </div>
                    <h4 className="text-xs font-bold text-white">{res.title}</h4>
                  </div>
                  <a href={res.url} target="_blank" rel="noreferrer" className="text-xs text-indigo-400 font-semibold pt-2 border-t border-slate-800">Open Resource ({res.duration_or_read_time}) →</a>
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-end">
            <button onClick={() => navigate('/quiz')} className="flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold text-sm shadow-xl">
              <span>Proceed to Assessment Quiz</span>
              <ArrowRight className="h-5 w-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
'''

files["frontend/src/pages/QuizPage.tsx"] = '''import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import { HelpCircle, CheckCircle2, AlertTriangle, Sparkles, ArrowRight, RotateCcw, Zap } from 'lucide-react';
import { useCourse } from '../context/CourseContext';
import { quizApi } from '../services/api';
import { Quiz, QuizEvaluationResult } from '../types';

export const QuizPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, activeConceptId, refreshCourse, addXP } = useCourse();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, any>>({});
  const [evaluation, setEvaluation] = useState<QuizEvaluationResult | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const activeConcept = (activeCourse?.concepts || []).find((c) => c.id === activeConceptId) || activeCourse?.concepts?.[0];

  useEffect(() => {
    const fetchQuiz = async () => {
      if (!activeConcept) return;
      setIsLoading(true);
      setEvaluation(null);
      setSelectedAnswers({});
      try {
        const quizData = await quizApi.getQuiz(activeConcept.id);
        setQuiz(quizData);
      } catch (err) {
        console.error('Quiz load error:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchQuiz();
  }, [activeConcept?.id]);

  const handleSelectOption = (questionId: string, optionIndex: number, isMulti: boolean) => {
    if (evaluation) return;
    if (isMulti) {
      const currentList: number[] = selectedAnswers[questionId] || [];
      const updated = currentList.includes(optionIndex) ? currentList.filter((i) => i !== optionIndex) : [...currentList, optionIndex];
      setSelectedAnswers({ ...selectedAnswers, [questionId]: updated });
    } else {
      setSelectedAnswers({ ...selectedAnswers, [questionId]: optionIndex });
    }
  };

  const handleSubmit = async () => {
    if (!quiz || !activeConcept || !activeCourse) return;
    setIsSubmitting(true);
    try {
      const res = await quizApi.submitQuiz(activeConcept.id, {
        quiz_id: quiz.id,
        concept_id: activeConcept.id,
        course_id: activeCourse.id,
        answers: selectedAnswers,
      });
      setEvaluation(res.evaluation);
      addXP(res.evaluation.xp_earned);
      await refreshCourse();
      if (res.evaluation.passed) {
        confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 } });
      }
    } catch (err) {
      console.error('Quiz error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!activeCourse || !activeConcept) return <div className="p-12 text-center text-slate-400">Please select a concept first.</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex justify-between items-center">
        <div>
          <span className="text-xs text-indigo-400 font-semibold">{activeCourse.title}</span>
          <h1 className="text-2xl font-black text-white">{activeConcept.title} — Quiz</h1>
        </div>
        <span className="text-xs text-slate-400 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800 font-mono">Pass: 75%</span>
      </div>

      {isLoading || !quiz ? (
        <div className="py-20 text-center text-slate-400 space-y-3">
          <Sparkles className="h-8 w-8 text-indigo-400 animate-spin mx-auto" />
          <p className="text-sm">Generating diagnostic quiz questions...</p>
        </div>
      ) : (
        <div className="space-y-6">
          {quiz.questions.map((q, idx) => {
            const isMulti = q.type === 'multiple_select';
            const userAns = selectedAnswers[q.id];
            const qEval = evaluation?.evaluations?.find((e) => e.question_id === q.id);

            return (
              <div key={q.id} className="p-6 rounded-2xl border bg-slate-900 border-slate-800 shadow-xl space-y-4">
                <span className="text-xs font-bold text-indigo-400 uppercase">Question {idx + 1}</span>
                <p className="text-sm font-semibold text-slate-100">{q.prompt}</p>
                {q.options && (
                  <div className="space-y-2">
                    {q.options.map((opt, oIdx) => {
                      const isSelected = isMulti ? Array.isArray(userAns) && userAns.includes(oIdx) : userAns === oIdx;
                      return (
                        <button
                          key={oIdx}
                          type="button"
                          disabled={!!evaluation}
                          onClick={() => handleSelectOption(q.id, oIdx, isMulti)}
                          className={`w-full p-3.5 rounded-xl border text-left text-xs font-medium ${isSelected ? 'bg-indigo-600/30 border-indigo-500 text-white' : 'bg-slate-950 border-slate-800 text-slate-300'}`}
                        >
                          {opt}
                        </button>
                      );
                    })}
                  </div>
                )}
                {qEval && (
                  <div className="mt-3 pt-3 border-t border-slate-800 text-xs text-slate-300">
                    <span className="font-bold text-indigo-400">Explanation: </span>{qEval.explanation}
                  </div>
                )}
              </div>
            );
          })}

          {!evaluation ? (
            <div className="flex justify-end">
              <button
                onClick={handleSubmit}
                disabled={isSubmitting || Object.keys(selectedAnswers).length === 0}
                className="flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold text-sm shadow-xl"
              >
                {isSubmitting ? 'Evaluating Answers...' : 'Submit Quiz for AI Evaluation'}
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
              <div className="flex justify-between items-center border-b border-slate-800 pb-4">
                <div>
                  <h3 className="text-xl font-extrabold text-white">{evaluation.passed ? '🎉 Concept Mastered!' : '⚠️ Remediation Recommended'}</h3>
                  <p className="text-xs text-slate-400 mt-1">{evaluation.feedback_summary}</p>
                </div>
                <div className="text-2xl font-black text-indigo-400">{evaluation.total_score}%</div>
              </div>
              <div className="flex gap-4">
                {evaluation.passed ? (
                  <button onClick={() => navigate('/roadmap')} className="px-6 py-3 rounded-xl bg-emerald-600 text-white font-bold text-xs">Proceed to Next Concept →</button>
                ) : (
                  <button onClick={() => navigate('/remediation')} className="px-6 py-3 rounded-xl bg-rose-600 text-white font-bold text-xs">Start Adaptive Remediation →</button>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
'''

files["frontend/src/pages/RemediationPage.tsx"] = '''import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GitBranch, BookOpen, RotateCcw } from 'lucide-react';
import { useCourse } from '../context/CourseContext';

export const RemediationPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, activeConceptId, setSelectedTeachingMode } = useCourse();
  const activeConcept = (activeCourse?.concepts || []).find((c) => c.id === activeConceptId) || activeCourse?.concepts?.[0];

  if (!activeCourse || !activeConcept) return <div className="p-12 text-center text-slate-400">No active concept for remediation.</div>;
  const prereq = activeConcept.prerequisites?.[0] || 'Foundational Addressing';

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div className="bg-gradient-to-br from-rose-950/40 via-slate-900 to-indigo-950/30 border border-rose-500/40 rounded-2xl p-6 shadow-2xl space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-950 border border-rose-800 text-xs font-bold text-rose-300">
          <GitBranch className="h-3.5 w-3.5 text-rose-400" />
          <span>Adaptive Remediation Triggered</span>
        </div>
        <h1 className="text-2xl font-black text-white">Re-aligning Mental Model for {activeConcept.title}</h1>
        <p className="text-xs text-slate-300 leading-relaxed">
          LearnGraph AI detected that your error pattern pointed to a gap in prerequisite <strong className="text-amber-300 font-mono">[{prereq}]</strong>.
        </p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex items-center justify-between">
        <div>
          <h4 className="text-xs font-bold text-slate-200">Re-teach with Worked Example</h4>
          <p className="text-[11px] text-slate-400">Re-examine the address bit calculations step by step.</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => { setSelectedTeachingMode('worked_example'); navigate('/lesson'); }}
            className="px-6 py-3 rounded-xl bg-indigo-600 text-white text-xs font-bold"
          >
            Re-teach with Worked Example →
          </button>
          <button onClick={() => navigate('/quiz')} className="px-4 py-3 rounded-xl bg-slate-800 text-slate-200 text-xs font-semibold">
            Retry Quiz
          </button>
        </div>
      </div>
    </div>
  );
};
'''

files["frontend/src/pages/FinalAssessmentPage.tsx"] = '''import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import { Trophy, Sparkles, Award, ArrowRight } from 'lucide-react';
import { useCourse } from '../context/CourseContext';
import { courseApi } from '../services/api';

export const FinalAssessmentPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, addXP } = useCourse();
  const [testData, setTestData] = useState<any>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, number>>({});
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [score, setScore] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchFinalTest = async () => {
      if (!activeCourse) return;
      setIsLoading(true);
      try {
        const data = await courseApi.getFinalTest(activeCourse.id);
        setTestData(data);
      } catch (err) {
        console.error('Final test error:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchFinalTest();
  }, [activeCourse?.id]);

  const handleSubmit = () => {
    if (!testData) return;
    let correct = 0;
    testData.questions.forEach((q: any) => {
      if (selectedAnswers[q.id] === q.correct_answer) correct++;
    });
    const calculatedScore = Math.round((correct / testData.questions.length) * 100);
    setScore(calculatedScore);
    setIsSubmitted(true);
    addXP(200);
    if (calculatedScore >= 80) confetti({ particleCount: 200, spread: 100, origin: { y: 0.5 } });
  };

  if (!activeCourse) return <div className="p-12 text-center text-slate-400">Please select a course first.</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div className="bg-gradient-to-r from-amber-950/40 via-slate-900 to-indigo-950/40 border border-amber-500/40 rounded-2xl p-6 shadow-2xl flex justify-between items-center">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-950 border border-amber-800 text-xs font-bold text-amber-300 mb-1.5">
            <Trophy className="h-3.5 w-3.5 text-amber-400" />
            <span>Boss-Level Final Mastery Test</span>
          </div>
          <h1 className="text-2xl font-black text-white">{activeCourse.title}</h1>
        </div>
        <span className="text-base font-black text-amber-400">+200 XP</span>
      </div>

      {isLoading || !testData ? (
        <div className="py-20 text-center text-slate-400 space-y-3">
          <Sparkles className="h-8 w-8 text-amber-400 animate-spin mx-auto" />
          <p className="text-sm">Synthesizing final exam...</p>
        </div>
      ) : (
        <div className="space-y-6">
          {testData.questions.map((q: any, idx: number) => (
            <div key={q.id} className="p-6 rounded-2xl border bg-slate-900 border-slate-800 shadow-xl space-y-4">
              <span className="text-xs font-bold text-amber-400 uppercase">Question {idx + 1}</span>
              <p className="text-sm font-semibold text-slate-100">{q.prompt}</p>
              <div className="space-y-2">
                {q.options.map((opt: string, oIdx: number) => (
                  <button
                    key={oIdx}
                    disabled={isSubmitted}
                    onClick={() => setSelectedAnswers({ ...selectedAnswers, [q.id]: oIdx })}
                    className={`w-full p-3.5 rounded-xl border text-left text-xs font-medium ${selectedAnswers[q.id] === oIdx ? 'bg-indigo-600/30 border-indigo-500 text-white' : 'bg-slate-950 border-slate-800 text-slate-300'}`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>
          ))}

          {!isSubmitted ? (
            <button onClick={handleSubmit} className="px-8 py-4 rounded-xl bg-gradient-to-r from-amber-600 to-indigo-600 text-white font-bold text-sm shadow-xl">
              Submit Boss Final Exam →
            </button>
          ) : (
            <div className="p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl text-center space-y-6">
              <Award className="h-16 w-16 text-amber-400 mx-auto" />
              <h3 className="text-2xl font-black text-white">Score: {score}%</h3>
              <button onClick={() => navigate('/dashboard')} className="px-6 py-3 rounded-xl bg-indigo-600 text-white text-xs font-bold">View Dashboard →</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
'''

files["frontend/src/pages/DashboardPage.tsx"] = '''import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BarChart3, Flame, Zap, Award, Calendar, ArrowRight, Sparkles } from 'lucide-react';
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
      <div className="py-20 text-center text-slate-400 space-y-3">
        <Sparkles className="h-8 w-8 text-indigo-400 animate-spin mx-auto" />
        <p className="text-sm">Aggregating analytics...</p>
      </div>
    );
  }

  const { user, stats, revision_schedule } = dashboardData;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex justify-between items-center">
        <div>
          <h1 className="text-xl font-extrabold text-white">{user.name} <span className="text-xs text-indigo-400 px-2 py-0.5 rounded bg-indigo-950 border border-indigo-800">Lvl {user.level}</span></h1>
          <p className="text-xs text-slate-400">{user.email}</p>
        </div>
        <div className="flex gap-4">
          <div className="bg-slate-950 px-4 py-2 rounded-xl border border-slate-800 flex items-center gap-2"><Flame className="h-5 w-5 text-amber-400" /><span className="text-sm font-bold text-white">{user.streak_days}d Streak</span></div>
          <div className="bg-slate-950 px-4 py-2 rounded-xl border border-slate-800 flex items-center gap-2"><Zap className="h-5 w-5 text-indigo-400" /><span className="text-sm font-bold text-indigo-300">{user.xp} XP</span></div>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800"><span className="text-[10px] uppercase font-bold text-slate-400 block">Overall Mastery</span><span className="text-2xl font-black text-indigo-400 mt-1 block">{stats.overall_mastery}%</span></div>
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800"><span className="text-[10px] uppercase font-bold text-slate-400 block">Mastered</span><span className="text-2xl font-black text-emerald-400 mt-1 block">{stats.mastered_concepts} / {stats.total_concepts}</span></div>
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800"><span className="text-[10px] uppercase font-bold text-slate-400 block">Quiz Accuracy</span><span className="text-2xl font-black text-purple-400 mt-1 block">{stats.average_quiz_accuracy}%</span></div>
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800"><span className="text-[10px] uppercase font-bold text-slate-400 block">Study Velocity</span><span className="text-2xl font-black text-amber-400 mt-1 block">{stats.learning_velocity_hours_this_week}h</span></div>
      </div>

      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
        <h3 className="text-sm font-bold text-white flex items-center gap-2"><Calendar className="h-4 w-4 text-indigo-400" /> Automated Spaced Repetition</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {revision_schedule.map((item: any) => (
            <div key={item.concept_id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between space-y-3">
              <div>
                <span className="text-[10px] font-bold text-amber-400 uppercase bg-amber-950/50 px-2 py-0.5 rounded">Due {item.due_date}</span>
                <h4 className="text-xs font-bold text-white mt-2">{item.concept_title}</h4>
              </div>
              <button
                onClick={() => { setActiveConceptId(item.concept_id); setSelectedTeachingMode(item.recommended_mode); navigate('/lesson'); }}
                className="text-xs text-indigo-400 font-semibold"
              >
                Review Now →
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
'''

files["frontend/src/pages/SavedCoursesPage.tsx"] = '''import React, { useEffect, useState } from 'react';
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
'''

files["frontend/src/pages/SimulationsPage.tsx"] = '''import React, { useState } from 'react';
import { Cpu, Layers, BarChart2, Send } from 'lucide-react';
import { MemoryPagingSimulation } from '../components/simulations/MemoryPagingSimulation';
import { CPUSchedulingSimulation } from '../components/simulations/CPUSchedulingSimulation';
import { SortingSimulation } from '../components/simulations/SortingSimulation';
import { NetworkPacketSimulation } from '../components/simulations/NetworkPacketSimulation';

export const SimulationsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'paging' | 'cpu' | 'sorting' | 'network'>('paging');

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-black text-white flex items-center gap-2">
          <Cpu className="h-6 w-6 text-indigo-400" />
          Interactive Simulations Lab
        </h1>
        <p className="text-xs text-slate-400 mt-1">Explore hands-on mental model visualizations.</p>
      </div>

      <div className="flex gap-2 border-b border-slate-800 pb-3 overflow-x-auto no-scrollbar">
        {[
          { id: 'paging', label: 'Virtual Memory & Paging MMU', icon: Layers },
          { id: 'cpu', label: 'CPU Scheduler & Gantt Chart', icon: Cpu },
          { id: 'sorting', label: 'Sorting Algorithms', icon: BarChart2 },
          { id: 'network', label: 'TCP 3-Way Handshake', icon: Send },
        ].map((t) => {
          const Icon = t.icon;
          const isSelected = activeTab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id as any)}
              className={`px-4 py-2 rounded-xl border text-xs font-bold flex items-center gap-2 ${
                isSelected ? 'bg-indigo-600 text-white border-indigo-500 shadow' : 'bg-slate-900 border-slate-800 text-slate-400'
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      <div>
        {activeTab === 'paging' && <MemoryPagingSimulation />}
        {activeTab === 'cpu' && <CPUSchedulingSimulation />}
        {activeTab === 'sorting' && <SortingSimulation />}
        {activeTab === 'network' && <NetworkPacketSimulation />}
      </div>
    </div>
  );
};
'''

files["frontend/src/App.tsx"] = '''import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { CourseProvider, useCourse } from './context/CourseContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { AITutorWidget } from './components/AITutorWidget';

import { LandingPage } from './pages/LandingPage';
import { CreateJourneyPage } from './pages/CreateJourneyPage';
import { AnalysisPage } from './pages/AnalysisPage';
import { KnowledgeGraphPage } from './pages/KnowledgeGraphPage';
import { RoadmapPage } from './pages/RoadmapPage';
import { LessonPage } from './pages/LessonPage';
import { QuizPage } from './pages/QuizPage';
import { RemediationPage } from './pages/RemediationPage';
import { FinalAssessmentPage } from './pages/FinalAssessmentPage';
import { SimulationsPage } from './pages/SimulationsPage';
import { DashboardPage } from './pages/DashboardPage';
import { SavedCoursesPage } from './pages/SavedCoursesPage';

const AppLayout: React.FC = () => {
  const location = useLocation();
  const isHome = location.pathname === '/';
  const isCreate = location.pathname === '/create';
  const isAnalysis = location.pathname.startsWith('/analysis');
  const showSidebar = !isHome && !isCreate && !isAnalysis;

  const { activeCourse, loadCourse } = useCourse();

  useEffect(() => {
    if (!activeCourse) {
      fetch('http://127.0.0.1:8000/api/courses')
        .then((res) => res.json())
        .then((courses) => {
          if (courses && courses.length > 0) loadCourse(courses[0].id);
        })
        .catch(() => {});
    }
  }, [activeCourse, loadCourse]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
      <Navbar />
      <div className="flex-1 flex w-full">
        {showSidebar && <Sidebar />}
        <main className="flex-1 overflow-x-hidden">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/create" element={<CreateJourneyPage />} />
            <Route path="/analysis/:courseId" element={<AnalysisPage />} />
            <Route path="/graph" element={<KnowledgeGraphPage />} />
            <Route path="/roadmap" element={<RoadmapPage />} />
            <Route path="/lesson" element={<LessonPage />} />
            <Route path="/quiz" element={<QuizPage />} />
            <Route path="/remediation" element={<RemediationPage />} />
            <Route path="/final-test" element={<FinalAssessmentPage />} />
            <Route path="/simulations" element={<SimulationsPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/courses" element={<SavedCoursesPage />} />
          </Routes>
        </main>
      </div>
      <AITutorWidget />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <CourseProvider>
        <AppLayout />
      </CourseProvider>
    </BrowserRouter>
  );
};

export default App;
'''

files["frontend/src/main.tsx"] = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
print(f"Successfully generated {len(files)} frontend files!")


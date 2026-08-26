import React, { useEffect } from 'react';
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

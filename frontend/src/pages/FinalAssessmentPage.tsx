import React, { useState, useEffect } from 'react';
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

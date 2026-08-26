import React, { createContext, useContext, useState } from 'react';
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

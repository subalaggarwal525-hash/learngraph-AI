import axios from 'axios';
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
  evaluateExplanation: async (payload: { course_id: string; concept_id: string; student_explanation: string }) =>
    (await api.post('/tutor/evaluate-explanation', payload)).data,
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

from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=True)
    name = Column(String, default="Alex Learner")
    xp = Column(Integer, default=450)
    level = Column(Integer, default=2)
    streak_days = Column(Integer, default=4)
    last_active_at = Column(DateTime, default=datetime.utcnow)
    preferences = Column(JSON, default={})

    courses = relationship("CourseModel", back_populates="user", cascade="all, delete-orphan")

class CourseModel(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), default="demo_user")
    title = Column(String, nullable=False)
    source_type = Column(String, default="topic")
    source_content = Column(Text, nullable=False)
    source_summary = Column(Text, default="")
    learning_goal = Column(String, default="deep_understanding")
    current_level = Column(String, default="beginner")
    study_time_hours_per_week = Column(Integer, default=5)
    preferred_style = Column(String, default="simple")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    knowledge_graph_data = Column(JSON, default={})
    roadmap_data = Column(JSON, default={})
    analytics_data = Column(JSON, default={})

    user = relationship("UserModel", back_populates="courses")
    concepts = relationship("ConceptModel", back_populates="course", cascade="all, delete-orphan")
    documents = relationship("DocumentModel", back_populates="course", cascade="all, delete-orphan")

class ConceptModel(Base):
    __tablename__ = "concepts"

    id = Column(String, primary_key=True, default=generate_uuid)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    short_summary = Column(Text, default="")
    difficulty = Column(Integer, default=2)
    importance = Column(Integer, default=4)
    estimated_minutes = Column(Integer, default=15)
    status = Column(String, default="locked")
    mastery_score = Column(Float, default=0.0)
    prerequisites = Column(JSON, default=[])
    relationships = Column(JSON, default=[])
    learning_objectives = Column(JSON, default=[])
    common_misconceptions = Column(JSON, default=[])
    source_references = Column(JSON, default=[])
    last_studied = Column(DateTime, nullable=True)
    stability = Column(Float, default=1.0)
    repetition_interval_days = Column(Integer, default=1)

    course = relationship("CourseModel", back_populates="concepts")
    lessons = relationship("LessonModel", back_populates="concept", cascade="all, delete-orphan")
    quizzes = relationship("QuizModel", back_populates="concept", cascade="all, delete-orphan")

class LessonModel(Base):
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, default=generate_uuid)
    concept_id = Column(String, ForeignKey("concepts.id"), nullable=False)
    mode = Column(String, default="simple")
    content_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    concept = relationship("ConceptModel", back_populates="lessons")

class QuizModel(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True, default=generate_uuid)
    concept_id = Column(String, ForeignKey("concepts.id"), nullable=False)
    questions_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    concept = relationship("ConceptModel", back_populates="quizzes")
    attempts = relationship("QuizAttemptModel", back_populates="quiz", cascade="all, delete-orphan")

class QuizAttemptModel(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String, primary_key=True, default=generate_uuid)
    quiz_id = Column(String, ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(String, default="demo_user")
    score = Column(Float, default=0.0)
    passed = Column(Boolean, default=False)
    answers_json = Column(JSON, default={})
    evaluation_json = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    quiz = relationship("QuizModel", back_populates="attempts")

class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("CourseModel", back_populates="documents")
    chunks = relationship("DocumentChunkModel", back_populates="document", cascade="all, delete-orphan")

class DocumentChunkModel(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, default=generate_uuid)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, default=0)
    section_title = Column(String, default="")
    content = Column(Text, nullable=False)
    embedding_json = Column(JSON, nullable=True)

    document = relationship("DocumentModel", back_populates="chunks")


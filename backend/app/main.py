import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database.connection import init_db
from backend.app.api import (
    courses,
    concepts,
    lessons,
    quizzes,
    tutor,
    documents,
    sources,
    resources,
    simulations,
    analytics
)

# Initialize database schema immediately
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="LearnGraph AI API",
    description="Adaptive AI learning platform with LangGraph knowledge graphs, prerequisite roadmaps, and adaptive teaching loops.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "LearnGraph AI API", "version": "1.0.0"}

# Include routers
app.include_router(courses.router)
app.include_router(concepts.router)
app.include_router(lessons.router)
app.include_router(quizzes.router)
app.include_router(tutor.router)
app.include_router(documents.router)
app.include_router(sources.router)
app.include_router(resources.router)
app.include_router(simulations.router)
app.include_router(analytics.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)


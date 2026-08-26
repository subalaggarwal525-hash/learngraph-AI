import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database.models import Base, UserModel

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./learngraph.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(UserModel).filter(UserModel.id == "demo_user").first()
        if not user:
            demo_user = UserModel(
                id="demo_user",
                email="learner@learngraph.ai",
                name="Alex Learner",
                xp=450,
                level=2,
                streak_days=4
            )
            db.add(demo_user)
            db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


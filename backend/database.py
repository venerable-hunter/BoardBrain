import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "kanban.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database with required tables."""
    Base.metadata.create_all(bind=engine)


def ensure_db_exists():
    """Ensure the database exists and is initialized."""
    if not os.path.exists(DB_PATH):
        init_db()


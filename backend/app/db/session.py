from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# This would normally come from environment variables
DATABASE_URL = "sqlite:///./data/llm_lab.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

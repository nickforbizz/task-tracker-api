from sqlalchemy.orm import Session
from src.db import SessionLocal

# Dependency to get the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

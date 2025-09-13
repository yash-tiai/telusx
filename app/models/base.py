from sqlalchemy.orm import declarative_base, Session
from app.models.session import SessionLocal

# Dependency to get DB session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()  # create a base class

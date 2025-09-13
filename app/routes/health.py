from fastapi import APIRouter
from sqlalchemy import create_engine

from core.config import DATABASE_URL

health_router = APIRouter()

@health_router.get("/health")
def health_check():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    print("Connected successfully")
    return {"status": "ok"}

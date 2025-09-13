from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base

class UserLoginActivity(Base):
    __tablename__ = "user_login_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    country = Column(String(100), nullable=False)
    device_hash = Column(String(100), nullable=False)
    timezone = Column(String(100), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

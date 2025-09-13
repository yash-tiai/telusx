from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base

class UserVerificationInfo(Base):
    __tablename__ = "user_verification_info"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    timezone = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

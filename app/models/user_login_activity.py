from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from app.models.base import Base
from schema.fraud_check_schema import ActivityStatus


class UserLoginActivity(Base):
    __tablename__ = "user_login_activity"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    country = Column(String(100), nullable=False)
    device_hash = Column(String(100), nullable=False)
    timezone = Column(String(100), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String(50), nullable=False, default=ActivityStatus.IN_PROCESS)
    anomaly_score = Column(Integer, nullable=True)
    is_anomalous = Column(Boolean, nullable=True)

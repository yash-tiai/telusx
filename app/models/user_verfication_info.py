from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from sqlalchemy.orm import Session

from app.models.base import Base
from schema.fraud_check_schema import CountryCode


class UserVerificationInfo(Base):
    __tablename__ = "user_verification_info"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    timezone = Column(String(100), nullable=False)
    country = Column(Enum(CountryCode), nullable=False)  # 🔹 Now Enum instead of String
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @classmethod
    def get_by_user_id(cls, user_id: str, db: Session) -> 'UserVerificationInfo | None':
        return db.query(cls).filter(cls.user_id == user_id).first()

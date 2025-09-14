import pytz
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Enum, Float
from app.models.base import Base
from schema.fraud_check_schema import ActivityStatus, FraudCheckRequest, IspType


class UserLoginActivity(Base):
    __tablename__ = "user_login_activity"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    country = Column(String(100), nullable=False)
    device_hash = Column(String(100), nullable=False)
    timezone = Column(String(100), nullable=False)
    vpn_flag = Column(Boolean, nullable=True)
    isp_type = Column(Enum(IspType), nullable=False)
    status = Column(String(50), nullable=False, default=ActivityStatus.IN_PROCESS)
    anomaly_score = Column(Float, nullable=True)
    is_anomalous = Column(String(20), nullable=True)

    @classmethod
    async def add_login_activity_log(cls, request: FraudCheckRequest, db) -> "UserLoginActivity":
        activity = cls(
            user_id=request.user_id,
            country=request.ip_country,
            timezone=request.ip_timezone,
            device_hash=request.device_hash,
            created_on=request.login_at,
            isp_type=request.isp_type,
            vpn_flag=request.vpn_flag,
        )
        db.add(activity)
        db.commit()
        return activity

    @classmethod
    async def get_all_login_activities(cls, user_id, db):
        rows = db.query(cls).filter(
            cls.user_id == user_id
        ).all()
        result = list()
        for i in rows:
            result.append({
                "user_id": i.user_id,
                "ip_country": i.country,
                "timezone": i.timezone,
                "vpn_flag": i.vpn_flag,
                "device_hash": i.device_hash,
                "isp_type": i.isp_type.value,
                "login_time": i.created_on.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"),
            })
        return result

    def update_fraud_status(self, anomaly_score: float, is_anomaly: bool, db) -> None:
        self.anomaly_score = anomaly_score
        self.is_anomalous = is_anomaly
        self.status = ActivityStatus.COMPLETED
        db.commit()

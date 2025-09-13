from fastapi import Depends
from sqlalchemy.orm import Session

from models import UserLoginActivity
from schema.fraud_check_schema import FraudCheckRequest, FraudCheckUser
from app.models.user_verfication_info import UserVerificationInfo
from models.base import get_db


async def check_login_fraud(request: FraudCheckRequest, db):
    activity = await add_login_activity_log(request, db)
    base_info = UserVerificationInfo.get_by_user_id(activity.user_id, db)
    update_risk_engine(activity, base_info.country, base_info.timezone)


async def add_login_activity_log(request: FraudCheckRequest, db) -> UserLoginActivity:
    activity = UserLoginActivity(
        user_id=request.user_id,
        country=request.ip_country,
        timezone=request.ip_timezone,
        device_hash=request.device_hash,
        created_on=request.login_at
    )
    db.add(activity)
    db.commit()
    return activity


def update_risk_engine(activity: UserLoginActivity, base_country: str, base_timezone: str) -> None:
    print("Updating risk engine with activity:", activity, base_country, base_timezone)


async def get_fraud_user_data(db: Session = Depends(get_db)) -> list[FraudCheckUser | None]:
    users = db.query(UserLoginActivity).all()
    user_data = list()
    for user in users:
        user_data.append(FraudCheckUser(
            id=user.id,
            user_id=user.user_id,
            ip_country=user.country,
            ip_timezone=user.timezone,
            device_hash=user.device_hash,
            login_at=user.created_on,
            anomaly_score=user.anomaly_score,
            is_anomalous=user.is_anomalous,
            status=user.status
        ))
    return user_data

from fastapi import Depends
from sqlalchemy.orm import Session

from schema.fraud_check import FraudCheckRequest, FraudCheckUser
from app.models.user_login_activity import UserLoginActivity
from models.base import get_db


async def check_login_fraud(request: FraudCheckRequest):
    activity = await add_fraud_check_record(request)
    update_risk_engine(activity)


async def add_fraud_check_record(request: FraudCheckRequest, db: Session = Depends(get_db)) -> UserLoginActivity:
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


def update_risk_engine(activity: UserLoginActivity) -> None:
    print("Updating risk engine with activity:", activity)


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
            login_at=user.created_on
        ))
    return user_data

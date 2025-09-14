import pytz
from fastapi import Depends
from sqlalchemy.orm import Session

from models import UserLoginActivity
from risk_engine import get_anomaly_results_as_dict
from schema.fraud_check_schema import FraudCheckRequest, FraudCheckUser
from app.models.user_verfication_info import UserVerificationInfo
from models.base import get_db


async def check_login_fraud(request: FraudCheckRequest, db) -> None:
    activity = await UserLoginActivity.add_login_activity_log(request, db)
    base_info = UserVerificationInfo.get_by_user_id(activity.user_id, db)
    all_data = await UserLoginActivity.get_all_login_activities(activity.user_id, db)
    data = get_anomaly_results_as_dict(all_data, base_info.country, base_info.timezone)
    dt_str = activity.created_on.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
    print('--------', dt_str, data[dt_str])

async def get_filtered_fraud_user_data(db: Session = Depends(get_db)) -> list[FraudCheckUser | None]:
    users = db.query(UserLoginActivity).filter(UserLoginActivity.is_anomalous == True).all()
    result = list()
    for user in users:
        result.append(FraudCheckUser(
            id=user.id,
            user_id=user.user_id,
            ip_country=user.country,
            ip_timezone=user.timezone,
            login_at=user.created_on,
            anomaly_score=user.anomaly_score,
            is_anomalous=user.is_anomalous,
            status=user.status
        ))
    return result

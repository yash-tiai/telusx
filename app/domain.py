from typing import Optional

import pytz
from fastapi import Depends
from sqlalchemy.orm import Session

from models import UserLoginActivity
from risk_engine import get_anomaly_results_as_dict
from schema.fraud_check_schema import FraudCheckRequest, FraudCheckUser, CountryCode, Timezone
from app.models.user_verfication_info import UserVerificationInfo
from models.base import get_db
from sdk import send_slack_teams_message


async def check_login_fraud(request: FraudCheckRequest, db) -> None:
    activity = await UserLoginActivity.add_login_activity_log(request, db)
    base_info = UserVerificationInfo.get_by_user_id(activity.user_id, db)
    if not base_info:
        base_country = CountryCode.IN
        base_timezone = Timezone.IST
    else:
        base_timezone = base_info.timezone
        base_country = base_info.country
    all_data = await UserLoginActivity.get_all_login_activities(activity.user_id, db)
    data = get_anomaly_results_as_dict(all_data, base_country, base_timezone)
    anomaly_score, is_anomaly = _extract_anomaly_scores(activity, data)
    if anomaly_score is not None and is_anomaly is not None:
        activity.update_fraud_status(anomaly_score, is_anomaly, db)
    if is_anomaly == "Anomaly":
        send_slack_teams_message(request)
    return


def _extract_anomaly_scores(activity, anomaly_data: dict) -> tuple[Optional[float], Optional[bool]]:
    dt_str = activity.created_on.astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
    record = anomaly_data.get(dt_str, {})
    return record.get("anomaly_score"), record.get("is_anomaly")


async def get_filtered_fraud_user_data(db: Session = Depends(get_db)) -> list[FraudCheckUser | None]:
    users = db.query(UserLoginActivity).filter(UserLoginActivity.is_anomalous == 'Anomaly').all()
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

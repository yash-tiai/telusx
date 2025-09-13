from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.base import get_db
from schema.fraud_check import FraudCheckRequest, FraudCheckResponse, FraudUserListResponse
from app import domain

fraud_check_router = APIRouter()


@fraud_check_router.post("/check-login-fraud/", response_model=FraudCheckResponse)
async def check_login_fraud(login_data: FraudCheckRequest, db: Session = Depends(get_db)):
    await domain.add_fraud_check_record(login_data, db)
    return FraudCheckResponse(success=True)


@fraud_check_router.post("/get-login-fraud/", response_model=FraudUserListResponse)
async def get_login_fraud_users(db: Session = Depends(get_db)):
    users = await domain.get_fraud_user_data(db)
    return FraudUserListResponse(data=users)

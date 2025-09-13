from fastapi import APIRouter
from schema.fraud_check import FraudCheckRequest, FraudCheckResponse
from app import domain

fraud_check_router = APIRouter()


@fraud_check_router.post("/check_login_fraud/", response_model=FraudCheckResponse)
async def check_login_fraud(login_data: FraudCheckRequest):
    await domain.add_fraud_check_record(login_data)
    return FraudCheckResponse(success=True)

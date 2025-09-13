import uvicorn
from fastapi import FastAPI
from app.routes import fraud_check_router, health_router

app = FastAPI(title="FastAPI Service")


def init_router(app):
    app.include_router(fraud_check_router, prefix="/api/v1", tags=["Fraud Check"])
    app.include_router(health_router, prefix="/api/v1", tags=["Health"])


init_router(app)
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # app instance
        host="0.0.0.0",
        port=8000,
        reload=True  # set False in production
    )


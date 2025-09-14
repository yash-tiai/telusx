import uvicorn
import joblib
from fastapi import FastAPI
from app.routes import fraud_check_router, health_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI Service")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # allow all headers
)


def init_router(app):
    app.include_router(fraud_check_router, prefix="/api/v1", tags=["Fraud Check"])
    app.include_router(health_router, prefix="/api/v1", tags=["Health"])


def train_ml_model():
    """Load the trained Isolation Forest model"""
    try:
        model = joblib.load("risk_engine_iforest.pkl")
        print("Model loaded successfully from 'risk_engine_iforest.pkl'")
        return model
    except FileNotFoundError:
        print("Model file 'risk_engine_iforest.pkl' not found. Please run train_isolation_forest.py first.")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


init_router(app)

if __name__ == "__main__":
    model = train_ml_model()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

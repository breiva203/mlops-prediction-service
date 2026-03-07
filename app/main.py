from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import numpy as np

from .config import get_settings
from .model import load_model
from .schemas import PredictionRequest, PredictionResponse


# ==============================
# Load configuration
# ==============================
settings = get_settings()
model = None


# ==============================
# Modern Lifespan (Startup + Shutdown)
# ==============================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown.
    Replaces deprecated @app.on_event("startup").
    """
    global model

    # ---- Startup ----
    model = load_model()
    print("🚀 Application starting...")
    print(f"App: {settings.app_name}")
    print(f"Model: {settings.model_name} v{settings.model_version}")

    yield  # Application runs here

    # ---- Shutdown ----
    print("🛑 Application shutting down...")
    model = None


# ==============================
# FastAPI App
# ==============================
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan
)


# ==============================
# Health Check
# ==============================
@app.get("/health")
def health():
    return {"status": "healthy"}


# ==============================
# Readiness Check
# ==============================
@app.get("/ready")
def readiness():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready"}


# ==============================
# Prediction Endpoint
# ==============================
@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    features = np.array([[request.feature1, request.feature2]])
    prediction = model.predict(features)[0]

    return PredictionResponse(prediction=float(prediction))
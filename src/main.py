from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
import numpy as np
import logging

from prometheus_fastapi_instrumentator import Instrumentator

from .config import get_settings
from .model import load_model
from .schemas import PredictionRequest, PredictionResponse


# ==============================
# Logging Configuration
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("prediction-service")


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
    logger.info("Application starting")
    logger.info(f"App name: {settings.app_name}")
    logger.info(f"Version: {settings.version}")
    logger.info(f"Model: {settings.model_name} v{settings.model_version}")

    try:
        model = load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Model failed to load: {e}")
        raise

    yield  # Application runs here

    # ---- Shutdown ----
    logger.info("Application shutting down")
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
# Prometheus Metrics
# ==============================
Instrumentator().instrument(app).expose(app)


# ==============================
# Request Logging Middleware
# ==============================
@app.middleware("http")
async def log_requests(request: Request, call_next):

    logger.info(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")

    return response


# ==============================
# Health Check
# ==============================
@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "healthy"}


# ==============================
# Readiness Check
# ==============================
@app.get("/ready")
def readiness():

    logger.info("Readiness check requested")

    if model is None:
        logger.warning("Readiness check failed: model not loaded")
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {"status": "ready"}


# ==============================
# Prediction Endpoint
# ==============================
@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    logger.info(
        f"Prediction request received | feature1={request.feature1}, feature2={request.feature2}"
    )

    if model is None:
        logger.error("Prediction requested but model not loaded")
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        features = np.array([[request.feature1, request.feature2]])

        prediction = model.predict(features)[0]

        logger.info(f"Prediction generated: {prediction}")

        return PredictionResponse(prediction=float(prediction))

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
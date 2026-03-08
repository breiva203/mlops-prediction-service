# src/main.py
import os
import pickle
import pandas as pd
from fastapi import FastAPI
from src.models import CustomerData  # your Pydantic model

app = FastAPI()

# ===============================
# Paths
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root

MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_model.pkl")
PREPROCESS_PATH = os.path.join(BASE_DIR, "models", "preprocessing.pkl")

# ===============================
# Load model artifacts
# ===============================
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(PREPROCESS_PATH, "rb") as f:
    preprocessing = pickle.load(f)

label_encoders = preprocessing["label_encoders"]
scaler = preprocessing["scaler"]
categorical_cols = preprocessing["categorical_cols"]
numerical_cols = preprocessing["numerical_cols"]
feature_columns = preprocessing["feature_columns"]

# ===============================
# Preprocessing function
# ===============================
def preprocess_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])

    for col in categorical_cols:
        df[col] = label_encoders[col].transform(df[col])

    df[numerical_cols] = scaler.transform(df[numerical_cols])

    df = df[feature_columns]

    return df

# ===============================
# Health & Readiness endpoints
# ===============================
@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/readiness")
def readiness():
    return {"status": "ready"}

# ===============================
# Single prediction endpoint
# ===============================
@app.post("/predict")
async def predict(customer: CustomerData):
    # Use model_dump() for Pydantic v2
    df = preprocess_input(customer.model_dump())
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": float(probability)
    }

# ===============================
# Batch prediction endpoint
# ===============================
@app.post("/batch-predict")
async def batch_predict(customers: list[CustomerData]):
    results = []
    for c in customers:
        df = preprocess_input(c.model_dump())
        prediction = model.predict(df)[0]
        results.append(int(prediction))

    return {"predictions": results}
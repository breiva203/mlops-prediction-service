# tests/test_prediction.py
from fastapi.testclient import TestClient
from src.main import app
from src.models import CustomerData

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_readiness():
    response = client.get("/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

def test_predict():
    # example input matching CustomerData fields
    sample_customer = {
        "gender": "Male",
        "age": 30,
        "contract_type": "Month-to-month",
        "payment_method": "Credit card",
        "paperless_billing": "Yes",
        "partner": "No",
        "dependents": "No",
        "tenure_months": 12,
        "monthly_charges": 70.0,
        "total_charges": 840.0,
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "Yes",
        "device_protection": "Yes",
        "tech_support": "No",
        "streaming_tv": "No",
        "streaming_movies": "Yes",
        "num_support_tickets": 2,
        "num_logins_last_month": 20,
        "feature_usage_score": 50,
        "late_payments": 0
    }

    response = client.post("/predict", json=sample_customer)
    assert response.status_code == 200
    json_data = response.json()
    assert "churn_prediction" in json_data
    assert "churn_probability" in json_data

def test_batch_predict():
    sample_customers = [
        {
            "gender": "Male",
            "age": 30,
            "contract_type": "Month-to-month",
            "payment_method": "Credit card",
            "paperless_billing": "Yes",
            "partner": "No",
            "dependents": "No",
            "tenure_months": 12,
            "monthly_charges": 70.0,
            "total_charges": 840.0,
            "internet_service": "Fiber optic",
            "online_security": "No",
            "online_backup": "Yes",
            "device_protection": "Yes",
            "tech_support": "No",
            "streaming_tv": "No",
            "streaming_movies": "Yes",
            "num_support_tickets": 2,
            "num_logins_last_month": 20,
            "feature_usage_score": 50,
            "late_payments": 0
        }
    ]

    response = client.post("/batch-predict", json=sample_customers)
    assert response.status_code == 200
    json_data = response.json()
    assert "predictions" in json_data
    assert isinstance(json_data["predictions"], list)
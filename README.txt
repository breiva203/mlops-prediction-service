🚀 MLOps Prediction Service

--------------------------------------------------
📌 Project Overview
--------------------------------------------------

This project is a production-style machine learning API built with:

- FastAPI
- Docker
- Docker Compose
- Automated Testing (pytest)
- CI/CD-ready structure
- Kubernetes-ready deployment

It demonstrates:

✔ Model lifecycle management
✔ Health & readiness probes
✔ Containerization
✔ Automated testing
✔ Deployment automation

The model used is a simple dummy model for demonstration purposes.

--------------------------------------------------
🖥 Run Locally (Without Docker)
--------------------------------------------------

1) Create Virtual Environment

python -m venv venv
venv\Scripts\activate

2) Install Dependencies

pip install -r requirements.txt

3) Run Application

uvicorn app.main:app --reload --port 8010

Open in browser:
http://localhost:8010/docs

--------------------------------------------------
🐳 Docker
--------------------------------------------------

Build Image:

docker build -t prediction-service:1.0 .

Run Container:

docker run -p 8010:8010 prediction-service:1.0

Docker Compose:

docker compose up --build

--------------------------------------------------
☸ Kubernetes
--------------------------------------------------

kubectl apply -f k8s/
kubectl get pods
kubectl get svc

--------------------------------------------------
🔍 API Examples
--------------------------------------------------

Health Check:

curl http://localhost:8010/health

Readiness Check:

curl http://localhost:8010/ready

Prediction:

curl -X POST http://localhost:8010/predict \
  -H "Content-Type: application/json" \
  -d '{"feature1": 2, "feature2": 3}'

Expected Response:

{ "prediction": 5.0 }

--------------------------------------------------
🔐 Production Notes
--------------------------------------------------

- Always version Docker images
- Avoid using "latest" tag
- Use health & readiness probes
- Store secrets as environment variables
- Implement CI/CD for automation
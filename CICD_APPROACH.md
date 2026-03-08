# CI/CD Pipeline Approach

This project implements a CI/CD pipeline to automate testing, building,
and deployment of the Customer Churn Prediction API.

The goal of the pipeline is to ensure that every code change is
automatically validated, tested, and deployed in a consistent and
reliable way.

------------------------------------------------------------------------

# Pipeline Overview

The CI/CD pipeline is triggered whenever a developer pushes code to the
repository.

The pipeline consists of the following stages:

1.  Code Push
2.  Linting
3.  Testing
4.  Build Docker Image
5.  Push Image to Container Registry
6.  Deployment

------------------------------------------------------------------------

# Pipeline Workflow

## 1. Developer Pushes Code

A developer pushes new code to the repository.

Example:

git push origin main

This triggers the CI pipeline automatically using GitHub Actions.

------------------------------------------------------------------------

## 2. Linting Stage

The first stage checks code quality using flake8.

Purpose: - Detect syntax errors - Enforce consistent coding style -
Prevent bad code from entering the pipeline

Command executed:

flake8 src

------------------------------------------------------------------------

## 3. Testing Stage

After linting passes, automated tests are executed using pytest.

Purpose: - Verify API endpoints work correctly - Validate prediction
functionality - Prevent regressions

Command executed:

pytest -v

Tests included in the project:

-   API health endpoint test
-   Readiness endpoint test
-   Single prediction endpoint test
-   Batch prediction endpoint test

------------------------------------------------------------------------

## 4. Build Stage

If all tests pass, a Docker image for the application is built.

Docker ensures the application runs consistently across different
environments.

Command used:

docker build -t churn-api .

The Docker image contains:

-   FastAPI application
-   Trained machine learning model
-   Required Python dependencies
-   Uvicorn server

------------------------------------------------------------------------

## 5. Push Stage

After building the image, it is pushed to a container registry such as
DockerHub.

Example command:

docker push username/churn-api:latest

The container registry stores the application image so it can be
deployed anywhere.

------------------------------------------------------------------------

## 6. Deployment Stage

The application can be deployed using either Docker Compose or
Kubernetes.

### Option 1 --- Docker Compose

Suitable for local development or small environments.

Command:

docker-compose up -d

This starts the API container and exposes it on port 8000.

### Option 2 --- Kubernetes Deployment

For production environments, the service can be deployed to Kubernetes.

Kubernetes provides:

-   container orchestration
-   automatic scaling
-   self-healing
-   rolling updates

Example deployment command:

kubectl apply -f kubernetes/deployment.yaml

------------------------------------------------------------------------

# Monitoring and Health Checks

Monitoring tools ensure the system remains healthy in production.

Common tools include:

Prometheus --- Metrics collection\
Grafana --- Visualization dashboards\
FastAPI Health Endpoint --- Service status monitoring

The API exposes a health endpoint:

GET /health

This endpoint is used by Docker and Kubernetes health checks.

------------------------------------------------------------------------

# CI/CD Tools Used

CI Pipeline --- GitHub Actions\
Code Quality --- flake8\
Testing --- pytest\
Build --- Docker\
Container Registry --- DockerHub\
Deployment --- Docker Compose / Kubernetes\
Monitoring --- Prometheus + Grafana

------------------------------------------------------------------------

# Benefits of this CI/CD Pipeline

-   Automated testing ensures reliability
-   Consistent application environments using Docker
-   Faster and safer deployments
-   Scalable infrastructure with Kubernetes
-   Improved development workflow

------------------------------------------------------------------------

# Summary

This CI/CD pipeline automates the full lifecycle of the machine learning
API. Every code change is automatically linted, tested, packaged into a
Docker image, and deployed in a controlled and repeatable way.

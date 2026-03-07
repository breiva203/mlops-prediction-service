# CI/CD Pipeline Design

This document describes the CI/CD strategy for the `mlops-prediction-service`.

The goal is to automate testing, building, scanning, and deployment in a secure and reproducible way.

---

# Trigger Strategy

## On Pull Request
- Run automated tests
- Run code quality checks
- Prevent merge if pipeline fails

## On Merge to `main`
- Build Docker image
- Tag image with commit SHA
- Push image to registry
- Deploy automatically to environment

This ensures only validated code reaches production.

---

# Pipeline Stages

## Stage 1 — Lint & Test

Purpose:
Validate code quality and correctness before building artifacts.

### Actions
- Run `pytest`
- Run `flake8` (optional but recommended)
- Fail fast if any test fails

Example commands:

```bash
pytest
flake8 app
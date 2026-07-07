# Travio AI – AI-Powered Multi-Agent Travel Planning Platform

Travio AI is a production-style AI travel planning platform that combines multi-agent orchestration, machine learning, and modern web engineering to deliver personalized end-to-end trip planning experiences.

## Features

- Multi-agent travel planning workflows using CrewAI and LangChain
- Personalized itinerary generation based on user preferences
- Budget estimation and travel recommendation pipelines
- ML model experimentation for prediction and optimization
- FastAPI backend ready for API-first integrations
- React + Tailwind frontend architecture for scalable UI delivery

## Tech Stack

### Frontend
- React.js
- Tailwind CSS
- HTML, CSS, JavaScript

### Backend
- Python
- FastAPI

### AI/ML
- CrewAI
- LangChain
- Random Forest
- XGBoost
- LSTM
- Scikit-learn
- Pandas
- NumPy

### Database
- MongoDB

### Tools
- Git, GitHub
- VS Code
- Postman

## Repository Structure

```text
Travio-AI/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── backend/
├── datasets/
├── docs/
│   ├── architecture.png
│   ├── database-schema.png
│   ├── demo.gif
│   ├── screenshots/
│   └── workflow.png
├── frontend/
├── ml_models/
├── tests/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation Guide

1. Clone the repository:
   ```bash
   git clone https://github.com/amrutak826/Travio-AI.git
   cd Travio-AI
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install frontend dependencies (when frontend package.json is added/updated):
   ```bash
   cd frontend
   npm install
   ```

## Usage

- Start backend (example):
  ```bash
  uvicorn backend.main:app --reload
  ```
- Run tests:
  ```bash
  pytest
  ```
- Start frontend (example):
  ```bash
  cd frontend
  npm run dev
  ```

## API Endpoints

> Placeholder endpoints for initial project structure.

- `GET /health` – Service health check
- `POST /api/v1/trips/plan` – Generate AI-powered travel plan
- `POST /api/v1/recommendations` – Get personalized recommendations
- `POST /api/v1/budget/estimate` – Estimate travel budget

## Screenshots

Add UI screenshots in `/docs/screenshots/` and reference them here.

## Architecture

High-level architecture artifacts are stored in `/docs/`:
- `architecture.png`
- `workflow.png`
- `database-schema.png`
- `demo.gif`

## Future Enhancements

- Real-time pricing and availability integrations
- User authentication and profile-based memory
- Advanced multi-agent negotiation for cost optimization
- MLOps pipeline for model monitoring and retraining
- Deployment automation for cloud-native environments

## Contributors

- [@amrutak826](https://github.com/amrutak826)

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).

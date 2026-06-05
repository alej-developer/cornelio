# Cornelio

Corporate monorepo for MLX-based inference services and the Cornelio web interface.

## Architecture

```
cornelio/
├── backend/        # Python 3.11+ / FastAPI — MLX inference API
├── frontend/       # Next.js (React) — Cornelio web client
├── .env.example    # Environment variable template
└── .gitignore      # Security-hardened ignore rules
```

## Stack

| Layer     | Technology                  |
|-----------|-----------------------------|
| Runtime   | Apple MLX                   |
| API       | Python 3.11+, FastAPI, Uvicorn |
| Frontend  | Next.js 14+, React 18       |
| Package   | uv (backend), npm (frontend)|

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Cornelio)

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Copy the template and populate with your credentials:

```bash
cp .env.example .env
```

See `.env.example` for the full list of required variables.

## License

Proprietary. All rights reserved.

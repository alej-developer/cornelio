# Cornelio — Corporate Intelligence Platform

Cornelio is a local-first, privacy-focused corporate inference and document intelligence platform. Engineered under stringent zero-egress security policies, it leverages Apple Silicon MLX hardware acceleration for large language models and a secure vector store infrastructure for Retrieval-Augmented Generation (RAG). 

By operating entirely within the corporate perimeter, Cornelio ensures sensitive intellectual property is never transmitted to external cloud providers.

## System Architecture

The project adopts a monolithic repository containing decoupled backend and frontend environments.

* **Backend (`/backend`):** RESTful API built on FastAPI. Integrates `mlx-lm` for quantized local model inference and ChromaDB for document vectorization and retrieval. Dependency injection prevents tight coupling across services.
* **Frontend (`/frontend`):** Next.js single-page application adopting a strict bespoke UI token system via CSS modules. Prevents internal server state leakage through rigorous error sanitization filters.

## Prerequisites

Due to hardware-accelerated local inference requirements:
* **Hardware:** MacOS device equipped with an Apple Silicon (M-series) chipset.
* **Memory:** Minimum 16GB Unified Memory (32GB+ highly recommended for optimal 8B+ parameter model loading).
* **Software:** Python 3.11+, Node.js 20+.

## Installation & Setup

### 1. Repository Clone
```bash
git clone https://github.com/alej-developer/cornelio.git
cd cornelio
```

### 2. Backend Initialization
The backend operates securely over a virtual environment.
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Generate the environment configuration:
```bash
cp .env.example .env
```
Ensure configuration values align with your local topology before initialization.

Run the FastAPI server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Frontend Initialization
```bash
cd frontend
npm install
```

Start the Next.js development server:
```bash
npm run dev
```

The corporate interface will be accessible via `http://localhost:3000`.

## QA & Security Tooling

* **Security Audit:** Run the automated Static Application Security Testing (SAST) tool.
  ```bash
  cd backend && ./security_audit.bat
  ```
* **Backend Unit Tests:** `pytest backend/tests`
* **Frontend Unit Tests:** `cd frontend && npm run test`
* **Load Testing:** `locust -f backend/benchmark.py`

## Contribution Guidelines

1. **Atomic Commits:** Maintain descriptive commit messages conforming to conventional commit standards (e.g., `feat:`, `fix:`, `refactor:`, `test:`).
2. **Pull Request Policy:** Direct commits to `main` are restricted. All proposed changes mandate a Pull Request subject to the CI/CD pipeline validation.
3. **Security Exclusivity:** Commits introducing external APIs, telemetry, or cloud-sync methodologies will be systematically rejected to preserve zero-egress integrity.

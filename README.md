# Cornelio — Plataforma Corporativa de Inteligencia (Corporate Intelligence Platform)

Cornelio es una plataforma de inferencia y análisis de documentos corporativos centrada en la privacidad y orientada al uso en redes locales (local-first). Diseñada bajo estrictas políticas de seguridad de cero exposición (zero-egress), aprovecha la aceleración de hardware Apple Silicon MLX para grandes modelos de lenguaje (LLMs) y una infraestructura segura de base de datos vectorial para Generación Aumentada por Recuperación (RAG).

Al operar enteramente dentro del perímetro corporativo, Cornelio garantiza que la propiedad intelectual sensible nunca sea transmitida a proveedores de la nube externos.

## Arquitectura del Sistema

El proyecto adopta un repositorio monolítico que contiene entornos backend y frontend desacoplados.

* **Backend (`/backend`):** API RESTful construida sobre FastAPI. Integra `mlx-lm` para inferencia de modelos locales cuantizados y ChromaDB para vectorización y recuperación de documentos. La inyección de dependencias previene el acoplamiento fuerte entre servicios.
* **Frontend (`/frontend`):** Aplicación de página única (SPA) en Next.js que adopta un sistema estricto de tokens UI a medida mediante módulos CSS. Previene la filtración del estado interno del servidor a través de rigurosos filtros de sanitización de errores.

## Requisitos Previos

Debido a los requerimientos de inferencia local acelerada por hardware:
* **Hardware:** Dispositivo MacOS equipado con un procesador Apple Silicon (serie M).
* **Memoria:** Mínimo 16GB de Memoria Unificada (se recomiendan encarecidamente 32GB+ para una carga óptima de modelos de 8B+ parámetros).
* **Software:** Python 3.11+, Node.js 20+.

## Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/alej-developer/cornelio.git
cd cornelio
```

### 2. Inicialización del Backend
El backend opera de forma segura sobre un entorno virtual.
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Generar la configuración del entorno:
```bash
cp .env.example .env
```
Asegúrese de que los valores de configuración se alineen con su topología local antes de la inicialización.

Ejecutar el servidor FastAPI:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Inicialización del Frontend
```bash
cd frontend
npm ci
```

Iniciar el servidor de desarrollo Next.js:
```bash
npm run dev
```

La interfaz corporativa estará accesible a través de `http://localhost:3000`.

## Herramientas de QA y Seguridad (DevOps)

* **Auditoría de Seguridad:** Ejecute la herramienta automatizada de Pruebas de Seguridad de Aplicaciones Estáticas (SAST).
  ```bash
  cd backend && ./security_audit.bat
  ```
* **Pruebas Unitarias Backend:** `pytest backend/tests`
* **Pruebas Unitarias Frontend:** `cd frontend && npm run test`
* **Pruebas de Carga (Benchmark):** Simule tráfico concurrente contra la latencia de MLX.
  ```bash
  locust -f backend/benchmark.py
  ```

## Pautas de Contribución

1. **Commits Atómicos:** Mantenga mensajes de commit descriptivos y estrictamente en español, conformes a los estándares de Conventional Commits (ej., `feat:`, `fix:`, `refactor:`, `test:`).
2. **Política de Pull Requests:** Los commits directos a `main` están restringidos. Todos los cambios propuestos exigen un Pull Request sujeto a la validación del pipeline CI/CD (GitHub Actions).
3. **Exclusividad de Seguridad:** Los commits que introduzcan APIs externas, telemetría o metodologías de sincronización en la nube serán rechazados sistemáticamente para preservar la integridad zero-egress.

---

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
npm ci
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

1. **Atomic Commits:** Maintain descriptive commit messages strictly in Spanish conforming to conventional commit standards (e.g., `feat:`, `fix:`, `refactor:`, `test:`).
2. **Pull Request Policy:** Direct commits to `main` are restricted. All proposed changes mandate a Pull Request subject to the CI/CD pipeline validation.
3. **Security Exclusivity:** Commits introducing external APIs, telemetry, or cloud-sync methodologies will be systematically rejected to preserve zero-egress integrity.

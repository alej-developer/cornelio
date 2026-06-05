"""
Services package — business logic, MLX integration, and RAG pipeline.

Service architecture follows SOLID principles:
- base.py defines abstract interfaces (Dependency Inversion)
- Each concrete service has a single responsibility
- dependencies.py provides FastAPI-compatible DI resolution
"""

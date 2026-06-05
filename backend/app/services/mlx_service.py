"""
MLX inference service — local model loading and text generation.

This module guarantees zero network egress: models must be pre-downloaded
and available at the configured local path. No data is sent to external
APIs or telemetry endpoints.

Follows the Open/Closed Principle: extend by subclassing LLMServiceBase
without modifying this implementation.
"""

import asyncio
import logging
import time
from typing import Any

from app.core.config import Settings
from app.core.exceptions import ModelNotLoadedError
from app.services.base import GenerationResult, LLMServiceBase

logger = logging.getLogger(__name__)


class MLXService(LLMServiceBase):
    """
    Concrete LLM service backed by Apple MLX.

    Loads a quantized model via mlx-lm and runs inference entirely
    on-device using the Apple Silicon unified memory architecture.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model: Any | None = None
        self._tokenizer: Any | None = None
        self._model_name: str = settings.MLX_MODEL_PATH or "not-configured"
        self._loaded: bool = False

    def is_loaded(self) -> bool:
        return self._loaded

    async def load_model(self) -> None:
        """
        Load the MLX model and tokenizer from the configured local path.

        This is a blocking operation offloaded to a thread pool to avoid
        starving the event loop during weight loading.
        """
        if self._loaded:
            logger.info("Model already loaded, skipping reload.")
            return

        model_path = self._settings.MLX_MODEL_PATH
        if not model_path:
            logger.warning(
                "MLX_MODEL_PATH is not configured. "
                "The inference service will operate in degraded mode."
            )
            return

        logger.info("Loading MLX model from '%s'...", model_path)
        try:
            loop = asyncio.get_running_loop()
            self._model, self._tokenizer = await loop.run_in_executor(
                None, self._load_model_sync, model_path
            )
            self._model_name = model_path
            self._loaded = True
            logger.info("MLX model loaded successfully: %s", model_path)
        except Exception as exc:
            logger.error("Failed to load MLX model: %s", str(exc))
            raise ModelNotLoadedError(
                internal_detail=f"Model load failure at '{model_path}': {exc}"
            ) from exc

    @staticmethod
    def _load_model_sync(model_path: str) -> tuple[Any, Any]:
        """Synchronous model loading (runs in thread pool)."""
        try:
            from mlx_lm import load  # type: ignore[import-untyped]

            model, tokenizer = load(model_path)
            return model, tokenizer
        except ImportError as exc:
            raise ModelNotLoadedError(
                internal_detail="mlx-lm is not installed or not available on this platform."
            ) from exc

    async def unload_model(self) -> None:
        """Release model and tokenizer from memory."""
        self._model = None
        self._tokenizer = None
        self._loaded = False
        logger.info("MLX model unloaded.")

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> GenerationResult:
        """
        Generate text using the loaded MLX model.

        All computation runs on-device. No network calls are made.
        """
        if not self._loaded or self._model is None or self._tokenizer is None:
            raise ModelNotLoadedError(
                internal_detail="generate() called but model is not loaded."
            )

        effective_max_tokens = min(
            max_tokens, self._settings.MLX_MAX_TOKENS
        )

        start_time = time.perf_counter()

        try:
            loop = asyncio.get_running_loop()
            generated_text = await loop.run_in_executor(
                None,
                self._generate_sync,
                prompt,
                effective_max_tokens,
                temperature,
            )
        except ModelNotLoadedError:
            raise
        except Exception as exc:
            logger.error("MLX generation failed: %s", str(exc))
            raise ModelNotLoadedError(
                internal_detail=f"Generation error: {exc}"
            ) from exc

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        token_count = self._estimate_token_count(generated_text)

        return GenerationResult(
            text=generated_text,
            model_name=self._model_name,
            tokens_generated=token_count,
            latency_ms=round(elapsed_ms, 2),
        )

    def _generate_sync(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """Synchronous generation (runs in thread pool)."""
        try:
            from mlx_lm import generate as mlx_generate  # type: ignore[import-untyped]

            return mlx_generate(
                self._model,
                self._tokenizer,
                prompt=prompt,
                max_tokens=max_tokens,
                temp=temperature,
            )
        except ImportError as exc:
            raise ModelNotLoadedError(
                internal_detail="mlx-lm generate function not available."
            ) from exc

    @staticmethod
    def _estimate_token_count(text: str) -> int:
        """
        Rough token count estimation.

        Uses a 4-characters-per-token heuristic when the tokenizer
        is not available for precise counting.
        """
        return max(1, len(text) // 4)

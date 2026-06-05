"""
Abstract base classes for all application services.

Follows the Dependency Inversion Principle (SOLID-D): high-level modules
depend on abstractions, not on concrete implementations. All endpoint
handlers receive service instances through FastAPI's dependency injection.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# [ES] Objetos de transferencia de datos usados entre límites de servicio / [EN] Data transfer objects used across service boundaries
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class DocumentChunk:
    """A single chunk of text extracted from a source document."""

    content: str
    source_filename: str
    chunk_index: int
    document_id: str


@dataclass(frozen=True, slots=True)
class SearchResult:
    """A single result returned by the vector store search."""

    content: str
    source_filename: str
    score: float
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class GenerationResult:
    """The output of a language model generation call."""

    text: str
    model_name: str
    tokens_generated: int
    latency_ms: float


# ---------------------------------------------------------------------------
# [ES] Interfaces de servicio / [EN] Service interfaces
# ---------------------------------------------------------------------------

class LLMServiceBase(ABC):
    """
    Interface for language model inference.

    Implementations must guarantee that no data leaves the local machine.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> GenerationResult:
        """Generate text from the given prompt."""
        ...

    @abstractmethod
    def is_loaded(self) -> bool:
        """Return True if the model is ready to serve requests."""
        ...

    @abstractmethod
    async def load_model(self) -> None:
        """Load the model weights into memory."""
        ...

    @abstractmethod
    async def unload_model(self) -> None:
        """Release model resources."""
        ...


class VectorStoreBase(ABC):
    """
    Interface for document vectorization and similarity search.

    Implementations must persist vectors locally (no external API calls).
    """

    @abstractmethod
    async def add_documents(self, chunks: list[DocumentChunk]) -> int:
        """
        Vectorize and store document chunks.

        Returns the number of chunks successfully indexed.
        """
        ...

    @abstractmethod
    async def search(self, query: str, k: int = 5) -> list[SearchResult]:
        """
        Search for the top-k most relevant chunks given a query string.
        """
        ...

    @abstractmethod
    async def get_document_count(self) -> int:
        """Return the total number of indexed documents."""
        ...

    @abstractmethod
    async def get_all_document_ids(self) -> list[str]:
        """Return all unique document IDs in the store."""
        ...

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the vector store (create collections, etc.)."""
        ...


class DocumentParserBase(ABC):
    """
    Interface for extracting raw text from uploaded files.

    Supports PDF and plain text formats.
    """

    @abstractmethod
    async def parse(
        self,
        content: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        """
        Parse file content and return extracted text.

        Raises UnsupportedFileTypeError for unrecognized content types.
        """
        ...

    @abstractmethod
    def supported_types(self) -> set[str]:
        """Return the set of MIME types this parser can handle."""
        ...

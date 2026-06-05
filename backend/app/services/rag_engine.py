"""
RAG (Retrieval-Augmented Generation) engine.

Reads local documents, splits them into chunks, vectorizes using
sentence-transformers, stores in ChromaDB, and retrieves relevant
context for query augmentation.

All processing is local. No data leaves the machine.

Follows the Interface Segregation Principle: this module implements
VectorStoreBase and exposes only the methods required by consumers.
"""

import logging
import uuid
from pathlib import Path
from typing import Any

from app.core.config import Settings
from app.core.exceptions import DocumentProcessingError, VectorStoreError
from app.services.base import DocumentChunk, SearchResult, VectorStoreBase

logger = logging.getLogger(__name__)

_DEFAULT_CHUNK_SIZE: int = 1000
_DEFAULT_CHUNK_OVERLAP: int = 200
_COLLECTION_NAME: str = "cornelio_documents"


class RAGEngine(VectorStoreBase):
    """
    Concrete vector store implementation backed by ChromaDB
    with sentence-transformers embeddings.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client: Any | None = None
        self._collection: Any | None = None
        self._persist_dir: str = settings.CHROMA_PERSIST_DIR or "chroma_data"
        self._embedding_model: str = settings.EMBEDDING_MODEL or "all-MiniLM-L6-v2"
        self._initialized: bool = False

    async def initialize(self) -> None:
        """
        Initialize ChromaDB client and create or load the document collection.

        Uses a persistent storage directory so indexed documents survive
        application restarts.
        """
        if self._initialized:
            return

        try:
            import chromadb  # type: ignore[import-untyped]
            from chromadb.config import Settings as ChromaSettings  # type: ignore[import-untyped]

            persist_path = Path(self._persist_dir)
            persist_path.mkdir(parents=True, exist_ok=True)

            self._client = chromadb.PersistentClient(
                path=str(persist_path),
                settings=ChromaSettings(anonymized_telemetry=False),
            )

            self._collection = self._client.get_or_create_collection(
                name=_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )

            self._initialized = True
            logger.info(
                "ChromaDB initialized at '%s' with collection '%s' (%d documents).",
                self._persist_dir,
                _COLLECTION_NAME,
                self._collection.count(),
            )
        except ImportError as exc:
            logger.error("ChromaDB is not installed: %s", str(exc))
            raise VectorStoreError(
                internal_detail="chromadb package is not installed."
            ) from exc
        except Exception as exc:
            logger.error("Failed to initialize ChromaDB: %s", str(exc))
            raise VectorStoreError(
                internal_detail=f"ChromaDB init failure: {exc}"
            ) from exc

    async def add_documents(self, chunks: list[DocumentChunk]) -> int:
        """
        Vectorize and store document chunks in ChromaDB.

        Each chunk is embedded using the configured sentence-transformers model
        via ChromaDB's default embedding function.
        """
        self._ensure_initialized()

        if not chunks:
            return 0

        try:
            ids: list[str] = []
            documents: list[str] = []
            metadatas: list[dict[str, str]] = []

            for chunk in chunks:
                chunk_id = f"{chunk.document_id}_{chunk.chunk_index}"
                ids.append(chunk_id)
                documents.append(chunk.content)
                metadatas.append({
                    "source_filename": chunk.source_filename,
                    "document_id": chunk.document_id,
                    "chunk_index": str(chunk.chunk_index),
                })

            self._collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
            )

            logger.info(
                "Indexed %d chunks from document '%s'.",
                len(chunks),
                chunks[0].source_filename if chunks else "unknown",
            )
            return len(chunks)

        except Exception as exc:
            logger.error("Failed to add documents to ChromaDB: %s", str(exc))
            raise VectorStoreError(
                internal_detail=f"ChromaDB add failure: {exc}"
            ) from exc

    async def search(self, query: str, k: int = 5) -> list[SearchResult]:
        """
        Perform a similarity search against the indexed document corpus.

        Returns the top-k most relevant chunks ordered by cosine similarity.
        """
        self._ensure_initialized()

        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=min(k, self._collection.count() or 1),
                include=["documents", "metadatas", "distances"],
            )

            search_results: list[SearchResult] = []

            if not results["documents"] or not results["documents"][0]:
                return search_results

            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                distance = results["distances"][0][i] if results["distances"] else 1.0

                relevance_score = max(0.0, 1.0 - distance)

                search_results.append(
                    SearchResult(
                        content=doc,
                        source_filename=metadata.get("source_filename", "unknown"),
                        score=round(relevance_score, 4),
                        metadata=metadata,
                    )
                )

            return search_results

        except Exception as exc:
            logger.error("ChromaDB search failed: %s", str(exc))
            raise VectorStoreError(
                internal_detail=f"ChromaDB search failure: {exc}"
            ) from exc

    async def get_document_count(self) -> int:
        """Return the total number of chunks in the collection."""
        self._ensure_initialized()
        try:
            return self._collection.count()
        except Exception as exc:
            raise VectorStoreError(
                internal_detail=f"ChromaDB count failure: {exc}"
            ) from exc

    async def get_all_document_ids(self) -> list[str]:
        """Return all unique document IDs currently in the store."""
        self._ensure_initialized()
        try:
            all_data = self._collection.get(include=["metadatas"])
            if not all_data["metadatas"]:
                return []

            doc_ids: set[str] = set()
            for meta in all_data["metadatas"]:
                if meta and "document_id" in meta:
                    doc_ids.add(meta["document_id"])

            return sorted(doc_ids)
        except Exception as exc:
            raise VectorStoreError(
                internal_detail=f"ChromaDB get_all_document_ids failure: {exc}"
            ) from exc

    def _ensure_initialized(self) -> None:
        """Guard clause: raise if the store has not been initialized."""
        if not self._initialized or self._collection is None:
            raise VectorStoreError(
                internal_detail="RAGEngine used before initialization."
            )


# ---------------------------------------------------------------------------
# [ES] Utilidad de fragmentación de texto / [EN] Text chunking utility
# ---------------------------------------------------------------------------

def chunk_text(
    text: str,
    chunk_size: int = _DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = _DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """
    Split text into overlapping chunks for vectorization.

    Uses LangChain's RecursiveCharacterTextSplitter when available,
    falls back to a simple sliding-window implementation.
    """
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        return splitter.split_text(text)

    except ImportError:
        logger.warning(
            "langchain-text-splitters not available. Using fallback chunker."
        )
        return _fallback_chunk(text, chunk_size, chunk_overlap)


def _fallback_chunk(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    """Simple sliding-window text chunker."""
    chunks: list[str] = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - chunk_overlap

    return chunks if chunks else [text.strip()] if text.strip() else []


def create_document_chunks(
    text: str,
    filename: str,
    document_id: str | None = None,
    chunk_size: int = _DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = _DEFAULT_CHUNK_OVERLAP,
) -> list[DocumentChunk]:
    """
    Full pipeline: split text into chunks and wrap them as DocumentChunk DTOs.

    Generates a unique document_id if one is not provided.
    """
    doc_id = document_id or uuid.uuid4().hex[:12]
    raw_chunks = chunk_text(text, chunk_size, chunk_overlap)

    return [
        DocumentChunk(
            content=chunk,
            source_filename=filename,
            chunk_index=i,
            document_id=doc_id,
        )
        for i, chunk in enumerate(raw_chunks)
    ]

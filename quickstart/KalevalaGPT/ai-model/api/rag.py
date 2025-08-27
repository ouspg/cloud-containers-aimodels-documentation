"""RAG service built on LlamaIndex

This module contains:
  - Embedding model setup
  - Vector index loading and persistence
  - Retrieval with top_k and similarity cutoff
"""

from __future__ import annotations

import os
import threading
from typing import List, Tuple

from llama_index.core import Settings, load_index_from_storage, StorageContext
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine

class RagService:
    """Semantic retrieval over a pre-built vector index."""

    def __init__(self) -> None:
        # Hardcoded config
        self.storage_dir: str = os.path.join(os.path.dirname(__file__), "..", "storage")
        self.embedding_model: str = "Qwen/Qwen3-Embedding-0.6B"
        self.chunk_size: int = 256
        self.chunk_overlap: int = 25
        self.top_k_default: int = 3
        self.similarity_cutoff: float = 0.5

        self._lock = threading.RLock()
        self._index = None

        # Global LlamaIndex settings
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=self.embedding_model,
            device = "cpu")
        Settings.llm = None
        Settings.chunk_size = self.chunk_size
        Settings.chunk_overlap = self.chunk_overlap

        self._load_index()

    def query(
        self,
        question: str,
        top_k: int | None = None,
        similarity_cutoff: float | None = None,
    ) -> Tuple[str, List[str]]:
        """Retrieve context passages for a question.

        Returns a concatenated context string and list of sources.
        """
        top_k = top_k or self.top_k_default
        similarity_cutoff = self.similarity_cutoff if similarity_cutoff is None else similarity_cutoff

        with self._lock:
            retriever = VectorIndexRetriever(index=self._index, similarity_top_k=top_k)
            query_engine = RetrieverQueryEngine(
                retriever=retriever,
                node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=similarity_cutoff)],
            )
            response = query_engine.query(question)

        context_lines: List[str] = []
        sources: List[str] = []
        for node in response.source_nodes[:top_k]:
            context_lines.append(node.text.strip())
            src = node.metadata.get("file_name") if node.metadata else "unknown"
            sources.append(str(src))

        context = "\n".join(context_lines) + "\n"
        return context, sources

    def _load_index(self) -> None:
        """Load the index from storage. Raises if not available."""
        with self._lock:
            storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
            self._index = load_index_from_storage(storage_context)

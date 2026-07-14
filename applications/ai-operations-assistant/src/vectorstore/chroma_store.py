"""Persistent ChromaDB vector-store service."""

from pathlib import Path
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection


DEFAULT_COLLECTION_NAME = "enterprise_documents"
DEFAULT_DATABASE_PATH = "chroma_db"


class ChromaStore:
    """Store and retrieve document embeddings using ChromaDB."""

    def __init__(
        self,
        database_path: str = DEFAULT_DATABASE_PATH,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        """Create a persistent ChromaDB client and collection."""
        if not database_path.strip():
            raise ValueError("database_path cannot be empty")

        if not collection_name.strip():
            raise ValueError("collection_name cannot be empty")

        Path(database_path).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=database_path)

        self.collection: Collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Enterprise AI Platform documents"},
        )

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """Add document chunks and their embeddings to ChromaDB."""
        record_count = len(ids)

        if record_count == 0:
            raise ValueError("At least one document is required")

        if not (
            record_count
            == len(documents)
            == len(embeddings)
            == len(metadatas)
        ):
            raise ValueError(
                "ids, documents, embeddings and metadatas "
                "must contain the same number of items"
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        number_of_results: int = 3,
    ) -> dict[str, Any]:
        """Find documents nearest to the supplied query embedding."""
        if not query_embedding:
            raise ValueError("query_embedding cannot be empty")

        if number_of_results <= 0:
            raise ValueError("number_of_results must be greater than zero")

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=number_of_results,
            include=["documents", "metadatas", "distances"],
        )

    def count(self) -> int:
        """Return the number of records in the collection."""
        return self.collection.count()
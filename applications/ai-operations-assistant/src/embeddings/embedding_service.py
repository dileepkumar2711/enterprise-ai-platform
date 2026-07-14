"""Generate numerical embeddings from text.

This module contains the local embedding service used by the
Enterprise AI Platform.
"""

from collections.abc import Sequence

from sentence_transformers import SentenceTransformer


DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:
    """Generate embeddings using a Sentence Transformer model."""

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        """Load the embedding model.

        Args:
            model_name: Name or path of the Sentence Transformer model.
        """
        if not model_name.strip():
            raise ValueError("model_name cannot be empty")

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        """Convert multiple text values into embedding vectors.

        Args:
            texts: Text values that must be converted into embeddings.

        Returns:
            A list containing one embedding vector for each text.

        Raises:
            ValueError: If no text was supplied or a text is empty.
        """
        if not texts:
            raise ValueError("At least one text value is required")

        cleaned_texts = []

        for text in texts:
            if not isinstance(text, str):
                raise TypeError("Every item must be a string")

            cleaned_text = text.strip()

            if not cleaned_text:
                raise ValueError("Text cannot be empty")

            cleaned_texts.append(cleaned_text)

        embeddings = self.model.encode(
            cleaned_texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """Convert one search query into an embedding vector."""
        if not isinstance(query, str):
            raise TypeError("Query must be a string")

        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError("Query cannot be empty")

        embedding = self.model.encode(
            cleaned_query,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embedding.tolist()


if __name__ == "__main__":
    service = EmbeddingService()

    example_texts = [
        "Kubernetes orchestrates containerized applications.",
        "Azure Kubernetes Service is a managed Kubernetes platform.",
        "Bengaluru receives rainfall during the monsoon season.",
    ]

    vectors = service.embed_texts(example_texts)

    print(f"Number of texts: {len(example_texts)}")
    print(f"Number of vectors: {len(vectors)}")
    print(f"Dimensions per vector: {len(vectors[0])}")
    print(f"First five values: {vectors[0][:5]}")
import pytest

from src.embeddings.embedding_service import EmbeddingService


@pytest.fixture(scope="module")
def embedding_service() -> EmbeddingService:
    return EmbeddingService()


def test_embed_query_returns_vector(
    embedding_service: EmbeddingService,
) -> None:
    vector = embedding_service.embed_query(
        "Kubernetes manages containers."
    )

    assert isinstance(vector, list)
    assert len(vector) > 0
    assert all(isinstance(value, float) for value in vector)


def test_embed_texts_returns_one_vector_per_text(
    embedding_service: EmbeddingService,
) -> None:
    texts = [
        "Terraform manages infrastructure.",
        "Prometheus collects metrics.",
    ]

    vectors = embedding_service.embed_texts(texts)

    assert len(vectors) == len(texts)
    assert len(vectors[0]) == len(vectors[1])


def test_empty_query_raises_error(
    embedding_service: EmbeddingService,
) -> None:
    with pytest.raises(ValueError):
        embedding_service.embed_query("   ")
from unittest.mock import MagicMock

from src.rag.rag_pipeline import RAGPipeline


def test_rag_pipeline_returns_grounded_answer():
    rag = RAGPipeline()

    rag.embedding_service = MagicMock()
    rag.vector_store = MagicMock()
    rag.llm_service = MagicMock()

    rag.embedding_service.embed_query.return_value = [0.1, 0.2, 0.3]

    rag.vector_store.search.return_value = {
        "documents": [[
            "Azure Key Vault securely stores passwords, secrets and certificates."
        ]]
    }

    rag.llm_service.generate.return_value = (
        "Application passwords should be stored in Azure Key Vault."
    )

    answer = rag.answer(
        "Where should I securely store application passwords?"
    )

    assert answer == (
        "Application passwords should be stored in Azure Key Vault."
    )

    rag.embedding_service.embed_query.assert_called_once()
    rag.vector_store.search.assert_called_once()
    rag.llm_service.generate.assert_called_once()
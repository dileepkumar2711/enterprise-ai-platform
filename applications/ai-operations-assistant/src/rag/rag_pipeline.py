"""End-to-end RAG pipeline."""

import time

import mlflow

from src.embeddings.embedding_service import EmbeddingService
from src.vectorstore.chroma_store import ChromaStore
from src.rag.prompt_builder import build_rag_prompt
from src.llm.ollama_service import OllamaService


class RAGPipeline:
    """Retrieve relevant context and generate a grounded answer."""

    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_store = ChromaStore()
        self.llm_service = OllamaService()

        mlflow.set_tracking_uri("http://127.0.0.1:5000")
        mlflow.set_experiment("AI-Operations-Assistant-LLMOps")

    def answer(self, question: str) -> str:
        """Answer a question using retrieved enterprise knowledge."""

        if not isinstance(question, str):
            raise TypeError("Question must be a string")

        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty")

        start_time = time.perf_counter()

        with mlflow.start_run():

            # Track configuration used for this RAG execution.
            mlflow.log_param("model", self.llm_service.model)
            mlflow.log_param("retrieval_k", 3)

            # 1. Convert the user's question into an embedding.
            query_embedding = self.embedding_service.embed_query(question)

            # 2. Retrieve the most relevant documents from ChromaDB.
            results = self.vector_store.search(
                query_embedding=query_embedding,
                number_of_results=3,
            )

            documents = results.get("documents", [[]])[0]

            if not documents:
                answer = (
                    "I don't have enough information in the provided context."
                )

                latency_seconds = time.perf_counter() - start_time

                mlflow.log_metric(
                    "latency_seconds",
                    latency_seconds,
                )
                mlflow.log_metric(
                    "retrieved_document_count",
                    0,
                )

                mlflow.set_tag("question", question)
                mlflow.set_tag("answer", answer)

                return answer

            # 3. Build a grounded RAG prompt.
            prompt = build_rag_prompt(
                question=question,
                context_documents=documents,
            )

            # 4. Send the grounded prompt to the local LLM.
            answer = self.llm_service.generate(prompt)

            latency_seconds = time.perf_counter() - start_time

            # Track RAG metrics.
            mlflow.log_metric(
                "latency_seconds",
                latency_seconds,
            )
            mlflow.log_metric(
                "retrieved_document_count",
                len(documents),
            )

            # Track request/response metadata.
            mlflow.set_tag("question", question)
            mlflow.set_tag("answer", answer)

            return answer
"""End-to-end RAG pipeline."""

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

    def answer(self, question: str) -> str:
        """Answer a question using retrieved enterprise knowledge."""

        if not isinstance(question, str):
            raise TypeError("Question must be a string")

        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty")

        # 1. Convert the user's question into an embedding.
        query_embedding = self.embedding_service.embed_query(question)

        # 2. Retrieve the most relevant documents from ChromaDB.
        results = self.vector_store.search(
            query_embedding=query_embedding,
            number_of_results=3,
        )

        documents = results.get("documents", [[]])[0]

        if not documents:
            return "I don't have enough information in the provided context."

        # 3. Build a grounded RAG prompt.
        prompt = build_rag_prompt(
            question=question,
            context_documents=documents,
        )

        # 4. Send the grounded prompt to the local LLM.
        answer = self.llm_service.generate(prompt)

        return answer
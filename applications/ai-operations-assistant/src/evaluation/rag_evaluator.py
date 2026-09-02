"""Evaluation utilities for the RAG pipeline."""


class RAGEvaluator:
    """Calculate lightweight evaluation metrics for RAG responses."""

    @staticmethod
    def context_relevance_score(
        question: str,
        documents: list[str],
    ) -> float:
        """Estimate lexical overlap between the question and retrieved context."""

        question_words = set(question.lower().split())

        if not question_words or not documents:
            return 0.0

        context_words = set(
            " ".join(documents).lower().split()
        )

        matching_words = question_words.intersection(context_words)

        return len(matching_words) / len(question_words)

    @staticmethod
    def answer_length(answer: str) -> int:
        """Return the number of words in the generated answer."""

        return len(answer.split())
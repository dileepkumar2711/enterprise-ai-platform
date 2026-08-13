"""Prompt construction for the RAG pipeline."""


def build_rag_prompt(question: str, context_documents: list[str]) -> str:
    """Build a grounded prompt using retrieved documents."""

    if not isinstance(question, str):
        raise TypeError("Question must be a string")

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    if not context_documents:
        raise ValueError("At least one context document is required")

    cleaned_documents = []

    for document in context_documents:
        if not isinstance(document, str):
            raise TypeError("Every context document must be a string")

        document = document.strip()

        if document:
            cleaned_documents.append(document)

    if not cleaned_documents:
        raise ValueError("Context documents cannot be empty")

    context = "\n\n".join(
        f"[Context {index}] {document}"
        for index, document in enumerate(cleaned_documents, start=1)
    )

    prompt = f"""You are an enterprise AI operations assistant.

Answer the user's question using ONLY the supplied context.

If the answer cannot be determined from the context, say:
"I don't have enough information in the provided context."

Do not invent information.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    return prompt
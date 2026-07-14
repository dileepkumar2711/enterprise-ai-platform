"""Semantic-search demonstration for the Enterprise AI Platform."""

from src.embeddings.embedding_service import EmbeddingService
from src.vectorstore.chroma_store import ChromaStore


def seed_vector_database(
    embedding_service: EmbeddingService,
    vector_store: ChromaStore,
) -> None:
    """Insert demonstration documents into ChromaDB."""
    documents = [
        "Azure Kubernetes Service provides managed Kubernetes clusters.",
        "Azure Key Vault securely stores passwords, secrets and certificates.",
        "Terraform is used to define cloud infrastructure as code.",
        "Prometheus collects metrics from applications and infrastructure.",
        "GitHub Actions automates build, test and deployment workflows.",
    ]

    ids = [
        "demo-aks-001",
        "demo-keyvault-001",
        "demo-terraform-001",
        "demo-prometheus-001",
        "demo-github-actions-001",
    ]

    metadatas = [
        {"source": "demo", "topic": "aks"},
        {"source": "demo", "topic": "key-vault"},
        {"source": "demo", "topic": "terraform"},
        {"source": "demo", "topic": "prometheus"},
        {"source": "demo", "topic": "github-actions"},
    ]

    embeddings = embedding_service.embed_texts(documents)

    vector_store.add_documents(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def display_results(results: dict) -> None:
    """Print ChromaDB query results in a readable format."""
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        print("No matching documents were found.")
        return

    for position, document in enumerate(documents, start=1):
        metadata = metadatas[position - 1]
        distance = distances[position - 1]

        print("-" * 70)
        print(f"Result: {position}")
        print(f"Document: {document}")
        print(f"Metadata: {metadata}")
        print(f"Distance: {distance}")


def main() -> None:
    """Run the semantic-search demonstration."""
    embedding_service = EmbeddingService()
    vector_store = ChromaStore()

    seed_vector_database(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    print(f"Documents stored: {vector_store.count()}")

    query = "Where should I securely save application passwords?"
    query_embedding = embedding_service.embed_query(query)

    results = vector_store.search(
        query_embedding=query_embedding,
        number_of_results=3,
    )

    print(f"\nQuestion: {query}")
    display_results(results)


if __name__ == "__main__":
    main()
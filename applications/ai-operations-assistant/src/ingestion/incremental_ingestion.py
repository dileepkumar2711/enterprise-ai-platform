"""Incremental document ingestion for the AI Operations Assistant."""

import hashlib
import json
from src.pdf_loader import load_pdf
from src.text_chunker import chunk_pages
from src.embeddings.embedding_service import EmbeddingService
from src.vectorstore.chroma_store import ChromaStore
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
STATE_FILE = DATA_DIR / "ingestion_state.json"


def calculate_file_hash(file_path: Path) -> str:
    """Calculate a SHA-256 fingerprint for a file."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_ingestion_state() -> dict[str, Any]:
    """Load previously stored document fingerprints."""
    if not STATE_FILE.exists():
        return {}

    with STATE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_ingestion_state(state: dict[str, Any]) -> None:
    """Persist document fingerprints for the next ingestion run."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)

def ingest_pdf(
    file_path: Path,
    embedding_service: EmbeddingService,
    vector_store: ChromaStore,
    state: dict[str, Any],
) -> str:
    """Incrementally ingest one PDF document."""

    source = file_path.name
    current_hash = calculate_file_hash(file_path)
    previous_hash = state.get(source)

    if previous_hash == current_hash:
        print(f"UNCHANGED: {source} - skipping")
        return "unchanged"

    if previous_hash is None:
        status = "NEW"
    else:
        status = "CHANGED"
        vector_store.delete_by_source(source)

    print(f"{status}: {source} - processing")

    pages = load_pdf(file_path)

    chunks = chunk_pages(
        pages,
        chunk_size=800,
        chunk_overlap=150,
    )

    if not chunks:
        print(f"EMPTY: {source} - no text chunks generated")
        return "empty"

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_service.embed_texts(texts)

    ids = [
        f"{source}-chunk-{chunk['chunk_id']}"
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": source,
            "page_number": chunk["page_number"],
            "chunk_id": chunk["chunk_id"],
        }
        for chunk in chunks
    ]

    vector_store.add_documents(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    state[source] = current_hash

    print(f"INGESTED: {source} - {len(chunks)} chunks")

    return status.lower()
def run_incremental_ingestion() -> None:
    """Process PDFs incrementally and remove deleted sources."""

    state = load_ingestion_state()
    embedding_service = EmbeddingService()
    vector_store = ChromaStore()

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))
    current_sources = {file_path.name for file_path in pdf_files}

    # Detect documents that existed previously but were deleted from disk.
    deleted_sources = set(state.keys()) - current_sources

    for source in deleted_sources:
        print(f"DELETED: {source} - removing vectors")
        vector_store.delete_by_source(source)
        del state[source]

    if not pdf_files:
        save_ingestion_state(state)
        print("No PDF files found.")
        print(f"Vector store records: {vector_store.count()}")
        return

    for file_path in pdf_files:
        ingest_pdf(
            file_path=file_path,
            embedding_service=embedding_service,
            vector_store=vector_store,
            state=state,
        )

    save_ingestion_state(state)

    print(f"Vector store records: {vector_store.count()}")
    print("Incremental ingestion completed.")

if __name__ == "__main__":
    run_incremental_ingestion()
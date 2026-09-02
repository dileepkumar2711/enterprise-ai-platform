# Enterprise AI Platform

## Module 1 — AI Operations Assistant

The AI Operations Assistant is a local, containerized Retrieval-Augmented Generation (RAG) application designed to answer questions using enterprise documents as its knowledge source.

Instead of relying only on the LLM's general knowledge, the application retrieves relevant information from an enterprise knowledge base and supplies that context to a locally running LLM.

---

## Architecture

```text
Enterprise Documents
        |
        v
    PDF Loader
        |
        v
 Document Chunking
        |
        v
Sentence Transformer
        |
        v
    Embeddings
        |
        v
     ChromaDB
        |
        v
 Semantic Retrieval
        |
        v
   Prompt Builder
        |
        v
    RAG Pipeline
        |
        v
 Ollama / Llama 3.2
        |
        v
 Grounded Answer
        |
        v
 FastAPI /ask
        |
        v
       User
```

---

## RAG Workflow

1. Enterprise documents are loaded and divided into smaller chunks.
2. Sentence Transformer converts the chunks into vector embeddings.
3. Embeddings and document metadata are stored in ChromaDB.
4. A user sends a question through the FastAPI `/ask` endpoint.
5. The query is converted into an embedding.
6. ChromaDB performs semantic similarity search.
7. Relevant document chunks are retrieved.
8. The Prompt Builder combines the retrieved context with the user's question.
9. The prompt is sent to the locally running Ollama LLM.
10. The LLM generates a grounded response using the retrieved enterprise context.

---

## Docker Architecture

```text
Windows Host
|
+-- Ollama
|     Llama 3.2
|     Port 11434
|
+-- Docker Desktop
      |
      +-- AI Operations Assistant Container
             |
             +-- FastAPI :8000
             +-- RAG Pipeline
             +-- Embedding Service
             +-- ChromaDB Client
             |
             +-- /app/chroma_db
                    |
                    v
             Persistent ChromaDB Data
```

The container communicates with Ollama running on the Windows host through:

```text
http://host.docker.internal:11434
```

The Ollama endpoint is configurable through the `OLLAMA_BASE_URL` environment variable.

---

## Technology Stack

- Python 3.11
- FastAPI
- Uvicorn
- Sentence Transformers
- ChromaDB
- Ollama
- Llama 3.2
- Docker
- Pytest
- Git / GitHub
- VS Code

---

## Implemented Components

### Sprint 1 — Document Processing

- Project structure
- Python environment
- PDF loading
- Document chunking
- Git/GitHub integration

### Sprint 2 — Embeddings and Vector Search

- Sentence Transformer embedding service
- Document embeddings
- Query embeddings
- ChromaDB vector database
- Persistent vector storage
- Semantic similarity search
- Enterprise document collection

### Sprint 3 — RAG and Local LLM

- Prompt Builder
- Context grounding
- RAG pipeline
- Ollama service
- Llama 3.2 integration
- FastAPI REST API
- `/health` endpoint
- `/ask` endpoint
- Input validation
- Error handling
- Grounded fallback response

### Containerization

- Dockerfile
- `.dockerignore`
- Python 3.11 slim container
- FastAPI containerization
- Host-to-container Ollama connectivity
- Persistent ChromaDB volume

### Testing

Automated tests cover:

- API health endpoint
- Ask endpoint
- Request validation
- Embedding generation
- Empty-query validation
- Ollama response handling
- Ollama prompt validation
- Prompt construction
- Context grounding
- RAG pipeline behavior

Current verified test result:

```text
13 passed
```

---

## API

### Health Check

```http
GET /health
```

Used to verify that the API service is available.

### Ask Question

```http
POST /ask
Content-Type: application/json
```

Example request:

```json
{
  "question": "Where should I securely store application passwords?"
}
```

Example grounded response:

```json
{
  "answer": "Azure Key Vault."
}
```

If the retrieved enterprise context does not contain sufficient information, the application is designed to return a grounded fallback rather than fabricate an answer.

Example:

```json
{
  "answer": "I don't have enough information in the provided context."
}
```

---

## Running Locally

The application requires Ollama and the configured Llama model to be available.

Start the API using the project environment and access the interactive API documentation at:

```text
http://localhost:8000/docs
```

---

## Running with Docker

Build the image:

```powershell
docker build -t ai-operations-assistant:1.1 .
```

Run the container with access to the host Ollama service and persistent ChromaDB storage:

```powershell
docker run -d `
  --name ai-operations-assistant `
  -p 8000:8000 `
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 `
  -v "${PWD}\chroma_db:/app/chroma_db" `
  ai-operations-assistant:1.1
```

Then open:

```text
http://localhost:8000/docs
```

---

## Key Engineering Concepts Demonstrated

This module demonstrates practical implementation of:

- Retrieval-Augmented Generation (RAG)
- Embeddings
- Vector databases
- Semantic search
- Context retrieval
- Prompt engineering
- LLM grounding
- Hallucination reduction
- Local LLM inference
- REST API development
- Docker containerization
- Persistent application data
- Environment-based configuration
- Automated testing

---

## Current Status

**AI Operations Assistant — Local RAG implementation completed and containerized.**

Implemented flow:

```text
Documents
   -> Chunking
   -> Embeddings
   -> ChromaDB
   -> Semantic Retrieval
   -> Prompt Builder
   -> RAG Pipeline
   -> Ollama / Llama 3.2
   -> FastAPI
   -> Docker
```

---

The broader Enterprise AI Platform roadmap includes:

- MLflow / LLMOps
- CI/CD
- Azure DevOps / GitHub Actions
- Kubernetes / AKS
- Terraform
- Azure AI services
- AWS deployment
- DevSecOps
- Observability
- Agentic AI
- MCP integration

These capabilities will be added incrementally as separate implementation milestones.

---
## MLflow / LLMOps
## Project 2 - MLOps / LLMOps

### Milestone 1 - MLflow RAG Run Tracking

MLflow has been integrated with the AI Operations Assistant to provide experiment and execution tracking for the RAG pipeline.

Each RAG request is recorded as an MLflow run under the experiment:

`AI-Operations-Assistant-LLMOps`

The current implementation tracks:

- **Parameters**
  - LLM model
  - Retrieval `k`

- **Metrics**
  - End-to-end RAG latency in seconds
  - Number of retrieved documents

- **Development metadata**
  - User question
  - Generated answer

> Question and answer values are logged as tags for local development and learning only. Production environments should apply appropriate privacy, security, redaction, and governance controls before logging request or response content.

### MLflow Tracking Flow

```text
User Question
     |
     v
FastAPI /ask
     |
     v
RAG Pipeline
     |
     +----> MLflow Run
     |        |
     |        +--> Parameters
     |        |     - model
     |        |     - retrieval_k
     |        |
     |        +--> Metrics
     |        |     - latency_seconds
     |        |     - retrieved_document_count
     |        |
     |        +--> Development Metadata
     |              - question
     |              - answer
     |
     v
Embedding
     |
     v
ChromaDB Retrieval
     |
     v
Prompt Builder
     |
     v
Ollama / Llama 3.2
     |
     v
Grounded Answer
from fastapi import FastAPI
from pydantic import BaseModel

from src.rag.rag_pipeline import RAGPipeline


app = FastAPI(
    title="AI Operations Assistant",
    description="Enterprise RAG API powered by ChromaDB and Ollama",
    version="0.1.0",
)

rag = RAGPipeline()


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest) -> AnswerResponse:
    answer = rag.answer(request.question)
    return AnswerResponse(answer=answer)
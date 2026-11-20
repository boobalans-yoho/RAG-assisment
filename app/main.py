
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .models import (
    AskRequest,
    AskResponse,
    SearchRequest,
    SearchResponse,
    Source,
)
from .ingestion import build_chunks
from .vector_store import VectorStore
from .retrieval import retrieve
from .context_builder import fit_context
from .generation import generate_answer
from .citations import extract_citations, validate_citations


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise Knowledge Assistant - RAG API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is missing",
        )

    import secrets

    if not secrets.compare_digest(x_api_key, settings.API_KEY):
        raise HTTPException(
            status_code=403,
            detail="Invalid API key",
        )

    return True


def get_store():
    store = VectorStore(index_dir=settings.INDEX_DIR)
    store.load()
    return store


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
    }


@app.post("/admin/reindex")
def reindex(
    authenticated: bool = Depends(verify_api_key),
):
    try:
        chunks = build_chunks(Path(settings.DATA_DIR))

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No documents found in data directory",
            )

        store = get_store()

        inserted = store.add_chunks(chunks)

        return {
            "status": "success",
            "documents_processed": len(chunks),
            "chunks_inserted": inserted,
            "message": "Documents indexed successfully",
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Reindex failed: {str(exc)}",
        )


@app.post("/search", response_model=SearchResponse)
def search(
    request: SearchRequest,
    authenticated: bool = Depends(verify_api_key),
):
    try:
        store = get_store()

        results = retrieve(
            query=request.question,
            store=store,
            k=request.top_k or settings.DEFAULT_TOP_K,
            department=request.filters.get("department"),
            year=request.filters.get("year"),
        )

        sources = [
            Source(
                id=str(item.get("id", "")),
                text=item.get("text", ""),
                score=item.get("score"),
                metadata=item.get("metadata", {}),
            )
            for item in results
        ]

        return SearchResponse(
            query=request.question,
            results=sources,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(exc)}",
        )


@app.post("/ask", response_model=AskResponse)
def ask(
    request: AskRequest,
    authenticated: bool = Depends(verify_api_key),
):
    try:
        store = get_store()

        results = retrieve(
            query=request.question,
            store=store,
            k=request.top_k or settings.DEFAULT_TOP_K,
            department=request.filters.get("department"),
            year=request.filters.get("year"),
        )

        if not results:
            return AskResponse(
                question=request.question,
                answer="I could not find relevant information in the available documents.",
                sources=[],
                fallback=True,
            )

        threshold = settings.SCORE_THRESHOLD

        relevant_results = [
            item for item in results
            if float(item.get("score", 0)) >= threshold
        ]

        if not relevant_results:
            return AskResponse(
                question=request.question,
                answer="I could not find sufficient information in the available documents.",
                sources=[],
                fallback=True,
            )

        context_chunks = fit_context(
            relevant_results,
            budget=settings.CONTEXT_TOKEN_BUDGET,
        )

        answer = generate_answer(
            question=request.question,
            chunks=context_chunks,
        )

        citations = extract_citations(answer)

        if not validate_citations(answer, context_chunks):
            answer = (
                "I could not provide a verified answer from the available sources."
            )

        sources = [
            Source(
                id=str(item.get("id", "")),
                text=item.get("text", ""),
                score=item.get("score"),
                metadata=item.get("metadata", {}),
            )
            for item in context_chunks
        ]

        return AskResponse(
            question=request.question,
            answer=answer,
            sources=sources,
            fallback=False,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Ask failed: {str(exc)}",
        )

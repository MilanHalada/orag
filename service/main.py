import json
from pathlib import Path
from typing import Iterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from service.api_models import StatsResponse, SourceResponse, AskResponse, AskRequest, FileRequest
from service.chunking import documents_to_chunks, images_to_chunks
from service.config import KB_PATH, INDEX_PATH
from service.image_loader import load_images
from service.index_store import get_or_build_index
from service.lmstudio_client import create_client
from service.markdown_loader import load_markdown_documents, load_markdown_document
from service.models import Chunk
from service.rag_chat import ask_with_context_stream
from service.retrieval import search


app = FastAPI(title="ORAG Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup() -> None:
    global documents_count
    global images_count
    global chunk_count
    global indexed_chunks
    global indexed_chunk_count

    client = create_client()

    print("Loading documents and images...")
    documents = load_markdown_documents(KB_PATH)
    documents_count = len(documents)
    print(f"Loaded {documents_count} documents")

    print("Loading images...")
    images = load_images(KB_PATH)
    images_count = len(images)
    print(f"Loaded {images_count} images")

    md_chunks = documents_to_chunks(documents)
    image_chunks = images_to_chunks(client, images, max_images=999)

    chunks = md_chunks + image_chunks
    chunk_count = len(chunks)
    print(f"Loaded {chunk_count} chunks - {len(md_chunks)} markdown chunks, {len(image_chunks)} image chunks")

    print("Building index...")
    indexed_chunks = get_or_build_index(client, chunks, INDEX_PATH)
    indexed_chunk_count = len(indexed_chunks)
    print(f"Built index with {indexed_chunk_count} chunks")



@app.get("/health", operation_id="health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/stats", operation_id="stats")
def stats() -> StatsResponse:
    return StatsResponse(
        documents_count=documents_count,
        images_count=images_count,
        chunk_count=chunk_count,
        indexed_chunk_count=indexed_chunk_count,
    )

@app.post("/ask", response_model=AskResponse, operation_id="ask")
def ask(request: AskRequest) -> AskResponse:
    client = create_client()

    # Search for relevant chunks
    results = search(
        client=client,
        indexed_chunks=indexed_chunks,
        query=request.question,
        top_k=request.top_k,
    )

    # Call llm with best chunks
    answer = "".join(
        ask_with_context_stream(
            client=client,
            question=request.question,
            results=results,
        )
    )

    return AskResponse(
        answer=answer,
        sources=results_to_sources(results),
    )

@app.post("/ask/stream", operation_id="ask_stream")
def ask_stream(request: AskRequest) -> StreamingResponse:
    return StreamingResponse(
        ask_stream_generator(request),
        media_type="text/event-stream",
    )

@app.post("/view_file_content", operation_id="view_file_content")
def get_files(request: FileRequest) -> str:

    if not request.file:
        return "File path is required"

    pathFile = Path(request.file)

    if not pathFile.exists():
        return "File not found"

    print(f"Loading file {request.file} - {KB_PATH.resolve()}")


    if not pathFile.is_relative_to(KB_PATH.resolve()):
        return "File must be in KB_PATH"


    result = load_markdown_document(Path(request.file))
    return result

def results_to_sources(results: list[tuple[float, Chunk]]) -> list[SourceResponse]:
    sources: list[SourceResponse] = []

    for score, chunk in results:
        sources.append(
            SourceResponse(
                title=chunk.title,
                source=chunk.source,
                chunk_index=chunk.chunk_index,
                content_type=chunk.content_type,
                score=score,
                text=chunk.text,
            )
        )

    return sources

def sse_event(event: str, data: object) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

def ask_stream_generator(request: AskRequest) -> Iterator[str]:
    if not indexed_chunks:
        yield sse_event("error", {"message": "Index is empty"})
        return

    client = create_client()

    results = search(
        client=client,
        indexed_chunks=indexed_chunks,
        query=request.question,
        top_k=request.top_k,
    )

    sources = results_to_sources(results)

    yield sse_event(
        "sources",
        [source.model_dump() for source in sources]
    )

    try:
        for token in ask_with_context_stream(
            client=client,
            question=request.question,
            results=results,
        ):
            yield sse_event("token", token)

        yield sse_event("done", {})
    except Exception as error:
        yield sse_event(
            "error",
            {"message": str(error)}
        )

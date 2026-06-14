from dataclasses import dataclass


@dataclass
class Chunk:
    title: str
    source: str
    text: str
    chunk_index: int
    content_type: str = "markdown"


@dataclass
class Document:
    title: str
    source: str
    text: str


@dataclass
class IndexedChunk:
    chunk: Chunk
    embedding: list[float]

@dataclass
class IndexData:
    content_hash: str
    indexed_chunks: list[IndexedChunk]
import pickle

from pathlib import Path
from openai import OpenAI

from models import Chunk, IndexedChunk, IndexData
from embeddings import get_embedding
from chunking import calculate_chunks_hash

def save_index(indexed_data: IndexData, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open( "wb") as file:
        pickle.dump(indexed_data, file)


def load_index(path: Path) -> IndexData:
    with path.open("rb") as file:
        return pickle.load(file)


def build_index(client: OpenAI, chunks: list[Chunk]) -> list[IndexedChunk]:
    indexed_chunks: list[IndexedChunk] = []

    for chunk in chunks:
        embedding = get_embedding(client, chunk.text)
        indexed_chunks.append(
            IndexedChunk(chunk, embedding)
        )

    return indexed_chunks


def get_or_build_index(
    client: OpenAI,
    chunks: list[Chunk],
    path: Path,
) -> list[IndexedChunk]:
    current_hash = calculate_chunks_hash(chunks)

    if path.exists():
        print(f"Načítavam index z {path}")
        index_data = load_index(path)


        if index_data.content_hash == current_hash:
            print("Index je aktuálny, nevytváram nový...")
            return index_data.indexed_chunks

        print("Index je neaktuálny, vytváram nový...")
    else:
        print("Index neexistuje, vytváram nový...")

    indexed_chunks = build_index(client, chunks)

    indexed_data = IndexData(current_hash, indexed_chunks)

    save_index(indexed_data, path)

    print(f"Index uložený do {path}")
    return indexed_chunks

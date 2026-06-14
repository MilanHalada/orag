import hashlib
import re
from pathlib import Path

from openai import OpenAI

from models import Document, Chunk
from config import EMBEDDING_MODEL
from vision import describe_image_cached


def split_text(text: str, max_chars: int = 800, overlap: int = 150) -> list[str]:
    chunks: list[str] = []

    start = 0

    while start < len(text):
        end = start + max_chars
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += max_chars - overlap

    return chunks


def split_markdown_by_headings(text: str) -> list[str]:
    sections: list[str] = []
    current_lines: list[str] = []

    for line in text.splitlines():
        is_heading = re.match(r"^#{1,6}\s+", line) is not None

        if is_heading and current_lines:
            section = "\n".join(current_lines).strip()
            if section:
                sections.append(section)

            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        section = "\n".join(current_lines).strip()
        if section:
            sections.append(section)

    return sections


def split_markdown_text(
    text: str,
    max_chars: int = 1200,
    overlap: int = 200,
) -> list[str]:
    final_chunks: list[str] = []
    sections = split_markdown_by_headings(text)

    for section in sections:
        if len(section) <= max_chars:
            final_chunks.append(section)
            continue

        final_chunks.extend(
            split_text(
                section,
                max_chars=max_chars,
                overlap=overlap,
            )
        )

    return final_chunks


def documents_to_chunks(documents: list[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []

    for document in documents:
        text_chunks = split_text(document.text)

        for index, text_chunk in enumerate(text_chunks):
            chunks.append(
                Chunk(
                    title=document.title,
                    source=document.source,
                    text=text_chunk,
                    chunk_index=index,
                    content_type="markdown",
                )
            )

    return chunks

def images_to_chunks(client: OpenAI, images: list[Path], max_images: int = 10) -> list[Chunk]:
    chunks: list[Chunk] = []

    for index, image_path in enumerate(images):
        if index >= max_images:
            break

        description = describe_image_cached(client, image_path)

        if not description.strip():
            continue

        chunks.append(
            Chunk(
                title=f"Obrázok: {image_path.stem}",
                source=str(image_path),
                text=description,
                chunk_index=index,
                content_type="image_vision",
            )
        )

    return chunks


def calculate_chunks_hash(chunks: list[Chunk]) -> str:
    hasher = hashlib.sha256()

    for chunk in chunks:
        hasher.update(chunk.text.encode("utf-8"))
        hasher.update(str(chunk.chunk_index).encode("utf-8"))
        hasher.update(chunk.title.encode("utf-8"))
        hasher.update(chunk.source.encode("utf-8"))

    hasher.update(EMBEDDING_MODEL.encode("utf-8"))

    return hasher.hexdigest()
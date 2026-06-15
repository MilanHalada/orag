from pathlib import Path

from service.config import IGNORED_DIR_NAMES
from service.models import Document


def should_ignore_path(path: Path) -> bool:
    return any(part in IGNORED_DIR_NAMES for part in path.parts)


def load_markdown_documents(folder: Path) -> list[Document]:
    documents: list[Document] = []

    for path in folder.rglob("*.md"):

        if should_ignore_path(path):
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

        if not text.strip():
            continue

        documents.append(
            Document(
                title=path.stem,
                source=str(path),
                text=text,
            )
        )

    return documents

def load_markdown_document(file: Path) -> str:

    text = file.read_text(encoding="utf-8", errors="ignore")

    return text
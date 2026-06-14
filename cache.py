import hashlib
from pathlib import Path


def file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            hasher.update(block)

    return hasher.hexdigest()


def read_text_cache(cache_path: Path) -> str | None:
    if not cache_path.exists():
        return None

    return cache_path.read_text()


def write_text_cache(cache_path: Path, text: str) -> None:

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(text, encoding="utf-8")


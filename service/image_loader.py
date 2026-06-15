from pathlib import Path

from service.config import IGNORED_DIR_NAMES, VISION_SUPPORTED_SUFFIXES


def should_ignore_path(path: Path) -> bool:
    return any(part in IGNORED_DIR_NAMES for part in path.parts)


def load_images(folder: Path) -> list[Path]:
    images = [
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in VISION_SUPPORTED_SUFFIXES and not should_ignore_path(path)
    ]

    return images
from pathlib import Path

LMSTUDIO_API_KEY = "lm-studio"
LMSTUDIO_BASE_URL = "http://192.168.100.8:1234/v1"

CHAT_MODEL = "google/gemma-4-e4b"
EMBEDDING_MODEL = "text-embedding-bge-m3"
VISION_MODEL = "qwen/qwen2.5-vl-7b"

INDEX_PATH = Path("data/index.pkl")
KB_PATH = Path("/home/milan/dev/notes/Notes")
VISION_CACHE_PATH = Path("data/vision_cache")

IGNORED_DIR_NAMES = {
    ".obsidian",
    ".trash",
    ".git",
    "node_modules",
}


VISION_SUPPORTED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
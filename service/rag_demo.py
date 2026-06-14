from chunking import documents_to_chunks, images_to_chunks
from config import INDEX_PATH,KB_PATH
from image_loader import load_images
from index_store import get_or_build_index
from lmstudio_client import create_client
from markdown_loader import load_markdown_documents
from rag_chat import print_sources, ask_with_context_stream
from retrieval import search


def main() -> None:
    client = create_client()

    documents = load_markdown_documents(KB_PATH)
    print(f"Načítaných dokumentov: {len(documents)}")


    images = load_images(KB_PATH)
    print(f"Načítaných obrazkov: {len(images)}")

    md_chunks = documents_to_chunks(documents)
    image_chunks = images_to_chunks(client, images, max_images=10)

    chunks = md_chunks + image_chunks
    print(f"Načítaných chunkov: {len(chunks)}")

    indexed_documents = get_or_build_index(client, chunks, INDEX_PATH)


    while True:
        question = input("\nOtázka > ").strip()

        if question.lower() in {"q", "quit", "exit"}:
            break

        if not question:
            continue

        results = search(client, indexed_documents, question, top_k=3)

        print()
        print_sources(results)

        print("Odpoveď:")
        for token in ask_with_context_stream(client, question, results):
            print(token, end="", flush=True)

        print()

if __name__ == "__main__":
    main()
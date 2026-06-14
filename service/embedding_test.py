import config
from lmstudio_client import create_client


def main() -> None:
    client = create_client()

    text = "RAG vyhľadá relevantné informácie a použije ich ako kontext pre jazykový model."

    response = client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=text,
    )

    embedding = response.data[0].embedding

    print(f"Text: {text}")
    print(f"Počet čísel vo vektore: {len(embedding)}")
    print("Prvých 10 čísel:")
    print(embedding[:10])


if __name__ == "__main__":
    main()
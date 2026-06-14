from openai import OpenAI
from config import EMBEDDING_MODEL


def get_embedding(client: OpenAI, text: str) -> list[float]:

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding
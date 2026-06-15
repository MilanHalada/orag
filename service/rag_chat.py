from openai import OpenAI
from typing import Iterator

from service.config import CHAT_MODEL
from service.models import Chunk

def build_context(results: list[tuple[float, Chunk]]) -> str:
    context_parts: list[str] = []

    for index, (score, chunk) in enumerate(results, start=1):
        context_parts.append(
            f"[Zdroj {index}]\n"
            f"Názov: {chunk.title}\n"
            f"Súbor: {chunk.source}\n"
            f"Chunk: {chunk.chunk_index}\n"
            f"Skóre: {score:.4f}\n"
            f"Text:\n{chunk.text}"
        )

    return "\n\n---\n\n".join(context_parts)


def ask_with_context_stream(
    client: OpenAI,
    question: str,
    results: list[tuple[float, Chunk]],
) -> Iterator[str]:

    context = build_context(results)

    system_prompt = (
        "Si asistent, ktorý odpovedá iba na základe poskytnutého kontextu. "
        "Ak odpoveď v kontexte nie je, povedz, že ju v kontexte nevidíš. "
        "Odpovedaj po slovensky a stručne."
    )

    user_prompt = (
        f"Otázka:\n{question}\n\n"
        f"Kontext:\n{context}"
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
        stream=True
    )

    for chunk in response:
        token = chunk.choices[0].delta.content
        if token:
            yield token

def print_sources(results: list[tuple[float, Chunk]]) -> None:
    print("Nájdené zdroje:")

    for score, chunk in results:
        print(f"- {chunk.title} / chunk {chunk.chunk_index} ({score:.4f})")
        print(f"  source: {chunk.source}")
        print(f"  text: {chunk.text}")
        print()
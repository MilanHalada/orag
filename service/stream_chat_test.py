from config import CHAT_MODEL
from lmstudio_client import create_client

def main() -> None:
    client = create_client()
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Si stručný technický asistent. Odpovedaj po slovensky, a stručne.",
            },
            {
                "role": "user",
                "content": "V jednej vete vysvetli, čo je RAG.",
            },
        ],
        temperature=0.2,
        stream=True
    )

    for chunk in response:
        token = chunk.choices[0].delta.content
        if token:
            print(token, end="", flush=True)



if __name__ == "__main__":
    main()

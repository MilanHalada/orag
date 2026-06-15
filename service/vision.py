import base64
from io import BytesIO
from pathlib import Path

from openai import OpenAI
from PIL import Image

from service.cache import file_sha256, write_text_cache, read_text_cache
from service.config import VISION_MODEL, VISION_CACHE_PATH


def image_to_png_base64(image_path: Path) -> str:
    """Convert image to PNG and return base64 string."""
    with Image.open(image_path) as image:
        image = image.convert("RGB")

        buffer = BytesIO()
        image.save(buffer, format="PNG")

    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{encoded}"

def image_to_data_url(image_path: Path):
    suffix = image_path.suffix.lower()

    mime_type = "image/png"

    match suffix:
        case ".jpg" | ".jpeg":
            mime_type = "image/jpeg"

    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def describe_image(
    client: OpenAI,
    image_path: Path
) -> str:
    """Describe image content for use in RAG indexing"""
    image_url = image_to_png_base64(image_path)

    prompt = (
        "Analyzuj tento obrázok pre účely RAG indexovania osobných poznámok.\n\n"
        "Odpovedaj výhradne po slovensky.\n"
        "Buď vecný, stručný a štruktúrovaný.\n"
        "Nevypisuj žiadne úvodné vety typu 'na obrázku vidím' alebo 'môj obrázok je'.\n"
        "Nevymýšľaj si. Ak si niečím nie si istý, uveď neistotu.\n\n"
        "Vráť presne tieto sekcie:\n"
        "Typ obrázka:\n"
        "Krátky popis:\n"
        "Viditeľný text:\n"
        "Dôležité objekty:\n"
        "Technické detaily:\n"
        "Kľúčové slová:\n\n"
        "Ak je na obrázku text, prepíš ho čo najpresnejšie.\n"
        "Ak je to screenshot, popíš aplikáciu, chyby, tlačidlá, tabuľky alebo formuláre.\n"
        "Ak je to technická fotka, popíš zariadenia, káble, štítky, súčiastky a nastavenia.\n"
        "Ak je to komiks, meme alebo ilustračný obrázok, popíš scény, texty a hlavné motívy."
    )

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        temperature=0.1,
    )

    answer = response.choices[0].message.content

    if answer is None:
        return ""

    return answer.strip()

def describe_image_cached(
    client: OpenAI,
    image_path: Path
) -> str:
    image_hash = file_sha256(image_path)
    cache_path = VISION_CACHE_PATH / f"{image_hash}.txt"

    cached_text = read_text_cache(cache_path)

    if cached_text is not None:
        return cached_text

    description = describe_image(client, image_path)
    write_text_cache(cache_path, description)

    return description


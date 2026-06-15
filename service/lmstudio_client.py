from openai import OpenAI
from service.config import LMSTUDIO_BASE_URL, LMSTUDIO_API_KEY

def create_client() -> OpenAI:
    return OpenAI(
        base_url=LMSTUDIO_BASE_URL,
        api_key=LMSTUDIO_API_KEY
    )

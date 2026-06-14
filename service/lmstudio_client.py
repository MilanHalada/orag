from openai import OpenAI
import config

def create_client() -> OpenAI:
    return OpenAI(
        base_url=config.LMSTUDIO_BASE_URL,
        api_key=config.LMSTUDIO_API_KEY
    )

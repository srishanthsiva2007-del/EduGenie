import os
import time
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

@lru_cache(maxsize=1)
def get_client():
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to your .env file.")
    return genai.Client(api_key=api_key)

def generate(prompt: str, *, system_instruction: str | None = None, json_mode: bool = False) -> str:
    from google.genai import types
    config = types.GenerateContentConfig(
        temperature=0.3,
        max_output_tokens=2048,
        system_instruction=system_instruction,
    )
    if json_mode:
        config.response_mime_type = "application/json"
    for attempt in range(3):
        try:
            response = get_client().models.generate_content(model=MODEL, contents=prompt, config=config)
            break
        except Exception as exc:
            is_unavailable = "503" in str(exc) or "UNAVAILABLE" in str(exc)
            if not is_unavailable or attempt == 2:
                raise
            time.sleep(2 ** attempt)

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()

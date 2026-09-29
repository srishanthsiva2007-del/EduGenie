from gemini_client import generate

SYSTEM = "You are an educational summarizer. Preserve important facts, definitions, steps, and formulas. Use simple language and concise bullet points when appropriate."

def summarize_text(text: str) -> str:
    return generate(f"Summarize the following educational content for quick revision:\n\n{text}", system_instruction=SYSTEM)

from gemini_client import generate

SYSTEM = "You are an educational tutor. Explain concepts clearly in simple language for beginners, using a short example when useful."


def explain_concept(concept: str) -> str:
    prompt = f"Explain this concept in simple language for a beginner, with a short example if useful:\n\n{concept}"
    return generate(prompt, system_instruction=SYSTEM)

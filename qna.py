from gemini_client import generate

SYSTEM = "You are EduGenie, a helpful educational tutor. Answer accurately and concisely. Explain technical terms simply and use examples when useful."

def answer_question(question: str) -> str:
    return generate(f"Answer this student question:\n\n{question}", system_instruction=SYSTEM)

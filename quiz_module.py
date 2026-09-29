import json
from gemini_client import generate

QUIZ_SCHEMA = """Return a JSON array of exactly 3 objects. Each object must have: question (string), options (array of exactly 4 strings), correct_answer (string matching one option), explanation (string)."""

def generate_quiz(text: str):
    prompt = f"""Create a quiz from the educational content below. {QUIZ_SCHEMA}\n\nContent:\n{text}"""
    raw = generate(prompt, system_instruction="You create accurate educational multiple-choice quizzes.", json_mode=True)
    data = json.loads(raw)
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Gemini did not return exactly 3 questions.")
    for item in data:
        if not all(k in item for k in ("question", "options", "correct_answer", "explanation")):
            raise ValueError("Quiz item has missing fields.")
        if len(item["options"]) != 4 or item["correct_answer"] not in item["options"]:
            raise ValueError("Quiz item must contain 4 options and a valid correct answer.")
    return data

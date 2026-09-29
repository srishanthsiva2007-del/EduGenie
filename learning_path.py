from gemini_client import generate

SYSTEM = "You are an educational planner. Create practical learning paths from beginner to advanced level. Keep the structure clear and realistic. Include concepts, suggested practice, approximate timeline, and resource types (not invented URLs)."

def generate_learning_path(topic: str) -> str:
    prompt = f"Create a structured learning path for: {topic}\nInclude Beginner, Intermediate, and Advanced stages, with topics, practice ideas, approximate timelines, and suggested resource types."
    return generate(prompt, system_instruction=SYSTEM)

from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="EduGenie", version="1.0.0", description="Gemini-powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}

@app.post("/qa")
async def qa(payload: QuestionRequest):
    try:
        return {"result": answer_question(payload.question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Q&A failed: {exc}")

@app.post("/explain")
async def explain(payload: QuestionRequest):
    try:
        return {"result": explain_concept(payload.question)}
    except Exception as exc:
        if "503" in str(exc) or "UNAVAILABLE" in str(exc).upper():
            raise HTTPException(
                status_code=503,
                detail="The AI service is experiencing high demand. Please try again later.",
            )
        raise HTTPException(status_code=502, detail=f"Explanation failed: {exc}")

@app.post("/quiz")
async def quiz(payload: TextRequest):
    try:
        return {"quiz": generate_quiz(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Quiz generation failed: {exc}")

@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        return {"result": summarize_text(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Summary failed: {exc}")

@app.post("/learn/recommendations")
async def recommendations(payload: QuestionRequest):
    try:
        return {"result": generate_learning_path(payload.question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Learning path failed: {exc}")

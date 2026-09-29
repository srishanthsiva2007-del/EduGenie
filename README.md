# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational web application built with FastAPI, HTML, CSS, JavaScript, and the Google Gemini API. Gemini powers every AI feature, including concept explanations, so the application does not need to download a large local language model.

## Features
- Question & Answer: `POST /qa`
- Concept Explanation: `POST /explain`
- Quiz generation: `POST /quiz` — exactly 3 MCQs, 4 options each
- Summarization: `POST /summarize`
- Learning recommendations: `POST /learn/recommendations`
- Browser UI at `/`
- Health check at `/health`

## 1. Requirements
- Python 3.10+
- VS Code
- Gemini API key from Google AI Studio
- Internet connection for Gemini API requests

## 2. Setup in VS Code (Windows)
Open this folder in VS Code, then Terminal → New Terminal.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace `your_gemini_api_key_here` with a key created in [Google AI Studio](https://aistudio.google.com/app/apikey). Keep this file private.

If PowerShell blocks activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 3. Run
```powershell
python -m uvicorn main:app --reload --port 8000
```

Open http://127.0.0.1:8000

FastAPI docs are at http://127.0.0.1:8000/docs

## 4. Test
Run automated tests:
```powershell
python -m pytest -q
```

Manual API test examples:
```powershell
curl.exe -X POST http://127.0.0.1:8000/qa -H "Content-Type: application/json" -d "{\"question\":\"What is Python?\"}"
```

Gemini requests automatically retry temporary `503 UNAVAILABLE` capacity errors. Invalid keys and quota errors are still reported so they can be corrected in Google AI Studio.

## 5. Project structure
```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_api.py
```

## Security
Never put the Gemini API key in HTML, JavaScript, or Git. Keep it in `.env`, which is ignored by Git. If a key is exposed, rotate/revoke it in Google AI Studio.

## Troubleshooting
- `GEMINI_API_KEY is not configured`: verify `.env` exists and the terminal was started from the project directory.
- `429` or quota errors: check your Gemini API quota/billing and model availability.
- `503 UNAVAILABLE`: Gemini is temporarily busy; the application retries automatically. Try again after a short wait if it persists.
- `Failed to fetch`: make sure Uvicorn is running and open `http://127.0.0.1:8000/`; do not open `index.html` directly from the file system.
- `pip`, `pytest`, or `uvicorn` is not recognized: activate `.venv`, or run each command through `python -m` as shown above.

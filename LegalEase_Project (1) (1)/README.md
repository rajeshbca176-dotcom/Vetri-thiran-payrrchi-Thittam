# LegalEase — AI-Powered Legal Document Generator

LegalEase is a local Streamlit + FastAPI application that generates editable legal-document drafts with Google Gemini and exports them to TXT, DOCX, and PDF.

> **Important:** This application generates drafts for informational/educational use. It is not a substitute for a qualified lawyer or legal advice. Users should review documents for their jurisdiction and circumstances before relying on them.

## Architecture

- **Frontend:** Streamlit (`frontend/app.py`)
- **Backend:** FastAPI (`main.py`, `routes.py`)
- **AI:** Google Gemini through the modern `google-genai` SDK (`ai_core/gemini_generator.py`)
- **Formatting:** `python-docx` and `fpdf2` (`formatters/`)
- **Config:** `.env` via `python-dotenv`

The supplied documentation specifies FastAPI, Streamlit, Gemini, editable preview, and TXT/DOCX/PDF exports. This implementation keeps that architecture while using the current Google GenAI Python SDK rather than the older `google-generativeai` package.

## Requirements

- Windows 10/11, macOS, or Linux
- Python 3.10+
- A Google Gemini API key
- VS Code (recommended)

## 1. Open in VS Code

Extract the ZIP and open the `LegalEase_Project` folder in VS Code.

## 2. Create a virtual environment

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env` and put your own key in it:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
BACKEND_URL=http://127.0.0.1:8000
```

The API key is only read by the backend. Do not commit `.env` to Git.

## 5. Start the backend

Terminal 1:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Check:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 6. Start the frontend

Terminal 2:

```bash
streamlit run frontend/app.py
```

Open the local Streamlit URL shown in the terminal, normally `http://localhost:8501`.

## 7. Test without calling Gemini

Run:

```bash
python -m pytest -q
```

These tests cover validation, sanitization, and document-format generation without requiring an API call.

## 8. End-to-end test

1. Start FastAPI.
2. Start Streamlit.
3. Select a document type.
4. Enter parties, terms, and effective date.
5. Click **Generate Document**.
6. Review/edit the generated draft.
7. Download TXT, DOCX, and PDF.

If the Gemini key is missing or invalid, the UI shows a clear error rather than silently generating fake legal text.

## Windows administrative execution

You normally **do not need Administrator privileges**. Use a normal VS Code terminal. If your Windows setup specifically requires an elevated terminal, open **PowerShell/Windows Terminal as Administrator** and run the same commands. The project itself does not request elevation and does not contain any code that attempts to bypass Windows security.

## Project tree

```text
LegalEase_Project/
├── .env.example
├── .gitignore
├── Dockerfile
├── Procfile
├── README.md
├── requirements.txt
├── main.py
├── routes.py
├── schemas.py
├── config.py
├── utils.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── formatters/
│   ├── __init__.py
│   ├── docx_formatter.py
│   ├── pdf_formatter.py
│   └── txt_formatter.py
├── frontend/
│   ├── __init__.py
│   └── app.py
├── assets/
│   └── legalease_logo.svg
└── tests/
    ├── __init__.py
    ├── test_api.py
    └── test_formatters.py
```

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiConfigurationError(RuntimeError):
    pass


class GeminiDocumentGenerator:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = (api_key or GEMINI_API_KEY).strip()
        self.model = (model or GEMINI_MODEL).strip()
        if not self.api_key:
            raise GeminiConfigurationError(
                "GEMINI_API_KEY is not configured. Add it to your .env file."
            )
        try:
            from google import genai
        except ImportError as exc:
            raise GeminiConfigurationError(
                "The google-genai package is not installed. Run: pip install -r requirements.txt"
            ) from exc
        self.client = genai.Client(api_key=self.api_key)

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        from google.genai import types
        prompt = f"""You are a careful legal-document drafting assistant.

Create a professional DRAFT of the requested legal document using only the facts supplied by the user.
Do not invent names, addresses, amounts, governing laws, dates, or obligations that were not supplied.
Where a necessary detail is missing, use a clearly marked placeholder such as [TO BE COMPLETED].
Use plain but formal language and organize the result with a title, numbered sections, and signature blocks.
Do not claim that the document is legally valid, jurisdiction-compliant, or reviewed by a lawyer.

Document type:
{document_type}

Parties:
{parties}

Effective date / dates:
{dates}

Terms and conditions:
{terms}

Return only the document draft, with no Markdown code fences and no commentary before or after it.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=5000),
        )
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty document.")
        return text

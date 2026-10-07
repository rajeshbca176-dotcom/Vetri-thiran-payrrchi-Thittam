from fastapi import APIRouter, HTTPException
from schemas import DocumentRequest
from ai_core.gemini_generator import GeminiConfigurationError, GeminiDocumentGenerator

router = APIRouter()

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()
        document = generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates,
        )
        return {"document": document, "model": generator.model}
    except GeminiConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI generation failed: {exc}") from exc

from pydantic import BaseModel, Field, field_validator
from config import MAX_DATES, MAX_DOCUMENT_TYPE, MAX_PARTIES, MAX_TERMS

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=MAX_DOCUMENT_TYPE)
    parties: str = Field(..., min_length=2, max_length=MAX_PARTIES)
    terms: str = Field(..., min_length=2, max_length=MAX_TERMS)
    dates: str = Field(..., min_length=2, max_length=MAX_DATES)

    @field_validator("document_type", "parties", "terms", "dates")
    @classmethod
    def clean_fields(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value

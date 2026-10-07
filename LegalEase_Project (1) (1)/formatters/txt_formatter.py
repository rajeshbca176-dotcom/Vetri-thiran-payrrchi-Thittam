from utils import sanitize_text

def format_txt(text: str) -> bytes:
    return sanitize_text(text).encode("utf-8")

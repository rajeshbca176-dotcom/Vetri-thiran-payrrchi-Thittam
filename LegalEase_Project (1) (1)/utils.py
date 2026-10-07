import html
import re
from typing import List


def sanitize_text(text: str) -> str:
    """Normalize AI/user text for safe document rendering."""
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text.strip()


def split_terms(terms: str) -> List[str]:
    return [part.strip(" -\t\r\n") for part in terms.split(";") if part.strip()]


def text_to_html(text: str) -> str:
    """Create a safe, readable HTML preview without trusting generated HTML."""
    escaped = html.escape(sanitize_text(text))
    blocks = []
    for paragraph in escaped.split("\n"):
        p = paragraph.strip()
        if not p:
            blocks.append("<div class='spacer'></div>")
        elif re.match(r"^(ARTICLE|SECTION|[0-9]+\.)\b", p, flags=re.I):
            blocks.append(f"<h3>{p}</h3>")
        else:
            blocks.append(f"<p>{p}</p>")
    return "".join(blocks)

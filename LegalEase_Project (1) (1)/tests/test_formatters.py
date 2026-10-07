from docx import Document
from formatters.docx_formatter import format_docx
from formatters.pdf_formatter import format_pdf
from formatters.txt_formatter import format_txt
from utils import sanitize_text, split_terms


def test_sanitize_and_split():
    assert sanitize_text("Hello\u2019s\u2014world") == "Hello's-world"
    assert split_terms("A; B; ; C") == ["A", "B", "C"]


def test_txt():
    assert format_txt("Hello").decode("utf-8") == "Hello"


def test_docx_is_readable():
    data = format_docx("SECTION 1\nHello world", "NDA", "Confidentiality; Payment")
    open('/tmp/test_legalease.docx', 'wb').write(data)
    doc = Document('/tmp/test_legalease.docx')
    assert "Hello world" in "\n".join(p.text for p in doc.paragraphs)


def test_pdf_has_bytes():
    data = format_pdf("SECTION 1\nHello world", "NDA", "Confidentiality")
    assert data.startswith(b"%PDF")

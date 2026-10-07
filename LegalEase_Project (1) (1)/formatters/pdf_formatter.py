from io import BytesIO
from fpdf import FPDF

from utils import sanitize_text, split_terms

class LegalEasePDF(FPDF):
    def __init__(self, doc_type: str):
        super().__init__()
        self.doc_type = sanitize_text(doc_type)
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, "LEGAL EASE", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 8, self.doc_type.upper(), align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, f"LegalEase - AI-generated draft | Page {self.page_no()}", align="C")


def format_pdf(text: str, doc_type: str, terms: str = "") -> bytes:
    pdf = LegalEasePDF(doc_type)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    for raw in sanitize_text(text).splitlines():
        line = raw.strip()
        if not line:
            pdf.ln(4)
            continue
        if line.isupper() or line.startswith("ARTICLE ") or line.startswith("SECTION "):
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(180, 6, line)
            pdf.set_font("Helvetica", size=11)
        else:
            pdf.multi_cell(180, 6, line)
            pdf.ln(1)
    if terms.strip():
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 7, "Key Terms", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=10)
        for i, term in enumerate(split_terms(terms), 1):
            pdf.multi_cell(180, 6, f"{i}. {term}")
    return bytes(pdf.output())

import html
import requests
import streamlit as st

from config import BACKEND_URL
from formatters.docx_formatter import format_docx
from formatters.pdf_formatter import format_pdf
from formatters.txt_formatter import format_txt
from utils import text_to_html

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
.main-title { text-align:center; font-size:2.5rem; font-weight:800; margin-bottom:0.2rem; }
.subtitle { text-align:center; color:#6b7280; margin-bottom:1.5rem; }
.preview { background:#111827; color:#f9fafb; border-radius:14px; padding:24px; max-height:600px; overflow:auto; }
.preview h3 { color:#93c5fd; }
.preview p { line-height:1.65; }
.small-note { color:#6b7280; font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered legal document drafting and export</div>', unsafe_allow_html=True)
st.info("LegalEase creates drafts for informational use. Review the final document with a qualified legal professional for your jurisdiction and situation.")

with st.form("legal_form"):
    col1, col2 = st.columns(2)
    with col1:
        document_type = st.text_input("Document Type", placeholder="Freelance Work Contract")
        dates = st.text_input("Effective Date / Dates", placeholder="April 10, 2025")
    with col2:
        parties = st.text_area("Parties Involved", placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)", height=120)
        terms = st.text_area("Terms & Conditions", placeholder="Payment within 30 days; Confidentiality; 15-day termination notice", height=120)
    submitted = st.form_submit_button("Generate Document", type="primary", use_container_width=True)

if submitted:
    if not all([document_type.strip(), dates.strip(), parties.strip(), terms.strip()]):
        st.error("Please complete all four fields.")
    else:
        payload = {"document_type": document_type, "parties": parties, "terms": terms, "dates": dates}
        try:
            with st.spinner("Generating your document with Gemini..."):
                response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=90)
            if response.ok:
                data = response.json()
                st.session_state.document = data["document"]
                st.session_state.doc_type = document_type
                st.session_state.terms = terms
                st.success("Document generated successfully.")
            else:
                detail = response.json().get("detail", response.text)
                st.error(f"Backend error: {detail}")
        except requests.RequestException as exc:
            st.error(f"Could not connect to FastAPI at {BACKEND_URL}. Start the backend first. Details: {exc}")

if "document" in st.session_state:
    st.divider()
    st.subheader("Document Preview")
    st.markdown(f'<div class="preview">{text_to_html(st.session_state.document)}</div>', unsafe_allow_html=True)

    st.subheader("Edit Document")
    st.session_state.document = st.text_area("Editable document", value=st.session_state.document, height=500, label_visibility="collapsed")

    text_bytes = format_txt(st.session_state.document)
    docx_bytes = format_docx(st.session_state.document, st.session_state.doc_type, st.session_state.terms)
    pdf_bytes = format_pdf(st.session_state.document, st.session_state.doc_type, st.session_state.terms)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("Download TXT", text_bytes, "legalease_document.txt", "text/plain", use_container_width=True)
    with c2:
        st.download_button("Download DOCX", docx_bytes, "legalease_document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with c3:
        st.download_button("Download PDF", pdf_bytes, "legalease_document.pdf", "application/pdf", use_container_width=True)

st.markdown('<p class="small-note">Backend: FastAPI • Frontend: Streamlit • AI: Google Gemini</p>', unsafe_allow_html=True)

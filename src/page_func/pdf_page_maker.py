import streamlit as st
import uuid
from utils import markdown_to_a4_pdf_page

st.title("Markdown Editor → PDF Page")


if "pages" not in st.session_state:
    st.session_state["pages"] = []


col_editor, col_preview = st.columns(2)

with col_editor:
    st.subheader("Write Markdown")

    markdown_text = st.text_area(
        "Markdown Input",
        height=500,
        placeholder=(
            "# Title\n\n"
            "Write **markdown** here.\n\n"
            "- Bullet point\n"
            "- Another point\n\n"
            "[Link](https://example.com)\n\n"
            "![Image](https://via.placeholder.com/300)"
        ),
    )

with col_preview:
    st.subheader("Live Preview")

    if markdown_text.strip():
        st.markdown(markdown_text, unsafe_allow_html=False)
    else:
        st.info("Markdown preview will appear here.")

st.markdown("---")


col_create, col_clear = st.columns([1, 1])

with col_create:
    if st.button("Create PDF Page from Markdown", disabled=(not markdown_text.strip())):
        pdf_bytes = markdown_to_a4_pdf_page(markdown_text)

        st.session_state["pages"].append({
            "id": str(uuid.uuid4()),
            "image": None,            
            "pdf_bytes": pdf_bytes,
            "ocr_text":markdown_text,
            "ocr_applied":True
        })

        st.success("PDF page created and added to document.")

with col_clear:
    if st.button("Clear Editor"):
        st.rerun()

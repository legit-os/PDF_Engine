from utils import merge_pdf_pages
import streamlit as st


st.header("Export")

if st.button("📄 Merge Pages into PDF"):
    merged_pdf = merge_pdf_pages(st.session_state["pages"])
    st.session_state["merged_pdf"] = merged_pdf
    st.success("PDF merged successfully!")

if "merged_pdf" in st.session_state:
    st.download_button(
        label="⬇ Download Final PDF",
        data=st.session_state["merged_pdf"],
        file_name="merged_document.pdf",
        mime="application/pdf"
    )

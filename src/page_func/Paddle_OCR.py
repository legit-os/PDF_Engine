import streamlit as st
from utils import apply_paddle_docker_ocr

st.title("Apply Paddle OCR to All Pages")

if "pages" not in st.session_state:
    st.stop()

if st.button("Run OCR on All Eligible Pages"):
    with st.spinner("Running Paddle OCR Docker..."):
        apply_paddle_docker_ocr(st.session_state["pages"])
    st.success("OCR Applied Successfully")

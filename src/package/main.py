from pathlib import Path
import streamlit as st 

st.set_page_config(layout="wide")

Uploader_Page = st.Page(Path("page_func/uploader_page.py"),title="Uploader")

Reorder_Page = st.Page(Path("page_func/Editor_page.py"),title="Editor")

OCR_page = st.Page(Path("page_func/OCR_Maker.py"),title="OCR Engine")

Compiler_page = st.Page(Path("page_func/downloader_page.py"),title="PDF Downloader")

Markdown_to_PDF_maker_page = st.Page(Path("page_func/pdf_page_maker.py"),title="PDF Writer")

Paddle_OCR_page = st.Page(Path("page_func/Paddle_OCR.py"),title="Paddle_OCR")

Splitter_page = st.Page(Path("page_func/splitter_page.py"))


nav = st.navigation([Uploader_Page,
                     Reorder_Page,
                     OCR_page,
                     Markdown_to_PDF_maker_page,
                     Paddle_OCR_page,
                     Splitter_page,
                     Compiler_page])

nav.run()
from pathlib import Path
import streamlit as st 

Uploader_Page = st.Page(Path("src/page_func/page1.py"),title="Uploader")

Reorder_Page = st.Page(Path("src/page_func/page2.py"),title="Editor")

# PDF_Entry_Page = st.Page(Path("src/page_func/pdf_to_img.py"),title="PDF Uploader")

OCR = st.Page(Path("src/page_func/OCR_Maker.py"),title="OCR Engine")

Compiler_page = st.Page(Path("src/page_func/downloader_page.py"),title="PDF Downloader")


nav = st.navigation([Uploader_Page,Reorder_Page,OCR,Compiler_page])

nav.run()
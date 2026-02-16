from pathlib import Path
import streamlit as st 



Uploader_Page = st.Page(Path("src/page_func/uploader_page.py"),title="Uploader")

Reorder_Page = st.Page(Path("src/page_func/Editor_page.py"),title="Editor")

# PDF_Entry_Page = st.Page(Path("src/page_func/pdf_to_img.py"),title="PDF Uploader")

OCR_page = st.Page(Path("src/page_func/OCR_Maker.py"),title="OCR Engine")

Compiler_page = st.Page(Path("src/page_func/downloader_page.py"),title="PDF Downloader")

Markdown_to_PDF_maker_page = st.Page(Path("src/page_func/pdf_page_maker.py"),title="PDF Writer")

Paddle_OCR_page = st.Page(Path("src/page_func/Paddle_OCR.py"),title="Paddle_OCR")


nav = st.navigation([Uploader_Page,
                     Reorder_Page,
                     OCR_page,
                     Markdown_to_PDF_maker_page,
                     Paddle_OCR_page,
                     Compiler_page])

nav.run()
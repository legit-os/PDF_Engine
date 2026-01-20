from pathlib import Path
import streamlit as st 

Uploader_Page = st.Page(Path("src/page_func/page1.py"),title="Uploader")

Reorder_Page = st.Page(Path("src/page_func/page2.py"),title="Editor")

Compiler_page = st.Page(Path("src/page_func/downloader_page.py"))


nav = st.navigation([Uploader_Page,Reorder_Page,Compiler_page])

nav.run()
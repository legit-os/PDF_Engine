from pathlib import Path
import streamlit as st 

Uploader_Page = st.Page(Path("src/page_func/page1.py"),title="Uploader")

Reorder_Page = st.Page(Path("src/page_func/page2.py"),title="Editor")



nav = st.navigation([Uploader_Page,Reorder_Page])

nav.run()
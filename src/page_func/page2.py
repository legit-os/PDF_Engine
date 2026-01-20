import PIL.Image
import streamlit as st
from utils import image_to_single_page_pdf


st.title("Reorder / Rotate / Delete Images")

pages = st.session_state["pages"]

if not pages:
    st.error("No images uploaded.")
    st.stop()

for i, page in enumerate(pages):
    col1, col2, col3 = st.columns([1.2, 1.2, 6])

    
    with col1:
        if st.button("⬆ Move", key=f"up_{page['id']}") and i > 0:
            pages[i - 1], pages[i] = pages[i], pages[i - 1]
            st.rerun()

        if st.button("🔄 Rotate", key=f"rotate_{page['id']}"):
            page["image"] = page["image"].rotate(-90, expand=True)
            page["pdf_bytes"] = image_to_single_page_pdf(page["image"])
            st.rerun()

  
    with col2:
        if st.button("⬇ Move", key=f"down_{page['id']}") and i < len(pages) - 1:
            pages[i + 1], pages[i] = pages[i], pages[i + 1]
            st.rerun()

        if st.button("🗑 Delete", key=f"delete_{page['id']}"):
            pages.pop(i)
            st.rerun()

    
    with col3:
        st.image(
            page["image"],
            caption=f"Page {i + 1}",
            width="stretch"
        )


import streamlit as st
from PIL import Image
import uuid
from utils import image_to_single_page_pdf


st.title("Upload Images")


st.session_state["pages"] = []


st.warning("Warning: Upload All the images at once, Returning to this Page again will remove all the inserted images or other documents")



uploaded_files = st.file_uploader(
    "Upload one or more images (Right click on files or Hold them to select based on your device type)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        pdf_byte = image_to_single_page_pdf(img)
        st.session_state["pages"].append({
            "id": str(uuid.uuid4()),
            "image": img,
            "pdf_bytes":pdf_byte
        })

    st.success(f"Having {len(st.session_state["pages"])} image(s)")


if st.session_state["pages"]:
    st.subheader("Current Images")
    for i, page in enumerate(st.session_state["pages"]):
        st.image(
            page["image"],
            caption=f"Image {i + 1}",
            width="stretch"
        )

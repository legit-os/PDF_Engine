import streamlit as st
from PIL import Image
import uuid
from utils import image_to_single_page_pdf, pdf_to_pages, PDFPage


st.session_state["pages"] = []


st.warning("Warning: :blue[Upload All the images or pdf at **ONCE**], Returning to this Page again will remove all the inserted images or other documents")

st.title("Upload Images")


uploaded_files = st.file_uploader(
    "Upload one or more images (Right click on files or Drag them here (select based on your device type))",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        pdf_byte = image_to_single_page_pdf(img)

        st.session_state["pages"].append(
            PDFPage(
                page_id=str(uuid.uuid4()),
                image=img,
                pdf_bytes=pdf_byte,
                markdown_text=None,
            )
        )

    st.success(f"Having {len(st.session_state['pages'])} image(s)")


st.title("Upload PDFs")


uploaded_pdfs = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_pdfs:
    total_pages_added = 0

    for pdf_file in uploaded_pdfs:
        pdf_bytes = pdf_file.read()
        pages = pdf_to_pages(pdf_bytes)

        st.session_state["pages"].extend(pages)
        total_pages_added += len(pages)

    st.success(f"Added {total_pages_added} page(s) from PDFs")


if st.session_state["pages"]:
    st.subheader("Current Images")
    for i, page in enumerate(st.session_state["pages"]):
        st.image(
            page["image"],
            caption=f"Image {i + 1}",
            width="stretch"
        )

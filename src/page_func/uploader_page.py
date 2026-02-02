import streamlit as st
from PIL import Image
import uuid
from utils import image_to_single_page_pdf, pdf_to_pages, PDFPage
from utils import get_pdf_uploader_key,get_image_uploader_key,check_up_keys,reset_keys

# -----------------------------------------------------------------------
has_pdf_up, pdf_up_key = check_up_keys("pdf")
has_image_up, image_up_key = check_up_keys("img")

if not has_pdf_up:
    pdf_up_key = get_pdf_uploader_key()

if not has_image_up:
    image_up_key = get_image_uploader_key()

# ---------------------------------------------------------------------

if "pages" not in st.session_state:
    st.session_state["pages"] = []
# ----------------------------------------------
uploader_selected = st.radio("Select what type of files to upload",["Image","PDF"],horizontal=True)

# ----------------------------------------------------------------------------------------
if uploader_selected == "Image":
    st.title("Upload Images")


    uploaded_files = st.file_uploader(
        "Upload one or more images (Right click on files and open or Drag them here )",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False,
        key=image_up_key
    )

    if uploaded_files:
        img = Image.open(uploaded_files).convert("RGB")
        pdf_byte = image_to_single_page_pdf(img)

        st.session_state["pages"].append(
            PDFPage(
                page_id=str(uuid.uuid4()),
                image=img,
                pdf_bytes=pdf_byte,
                markdown_text=None,
                ocr_applied=False
            )
        )

        reset_keys()
        st.rerun()
        # image_up_key = get_image_uploader_key()
        # pdf_up_key = get_pdf_uploader_key()
            
# --------------------------------------------------------------------------
if uploader_selected == "PDF":
    
    st.title("Upload PDFs")


    uploaded_pdfs = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=False,
        key=pdf_up_key
    )

    if uploaded_pdfs:

            pdf_bytes = uploaded_pdfs.read()
            pages = pdf_to_pages(pdf_bytes)

            st.session_state["pages"].extend(pages)

            reset_keys()
            st.rerun()
            # image_up_key = get_image_uploader_key()
            # pdf_up_key = get_pdf_uploader_key()

st.success(f"Having {len(st.session_state['pages'])} pdf pages")

if st.session_state["pages"]:
    st.subheader("Current Images")
    for i, page in enumerate(st.session_state["pages"]):
        st.image(
            page["image"],
            caption=f"Image {i + 1}",
            width="stretch"
        )

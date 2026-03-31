import streamlit as st
from PIL import Image
import uuid
from package.utils import image_to_single_page_pdf, pdf_to_pages, PDFPage,get_pdf_from_pptx_managed
from package.utils import get_uploader_key,check_up_keys,reset_keys

st.set_page_config(layout="wide")
# -----------------------------------------------------------------------
has_pdf_up, pdf_up_key = check_up_keys("pdf")
has_image_up, image_up_key = check_up_keys("image")
has_ppt_up, ppt_up_key = check_up_keys("ppt")

if not has_pdf_up:
    pdf_up_key = get_uploader_key("pdf")

if not has_image_up:
    image_up_key = get_uploader_key("image")

if not has_ppt_up:
    ppt_up_key = get_uploader_key("ppt")

# -----------------
def optimize_image(image:Image.Image, max_width=1200):
    width, height = image.size
    
    if width > max_width:
        ratio = max_width / float(width)
        new_height = int(float(height) * float(ratio))
        
        return image.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    return image

# ---------------------------------------------------------------------

if "pages" not in st.session_state:
    st.session_state["pages"] = []
# ----------------------------------------------
uploader_selected = st.radio("Select what type of files to upload",["Image","PDF","PPTX"],horizontal=True)

logger = st.empty()

# ----------------------------------------------------------------------------------------
if uploader_selected == "Image":
    st.title("Upload Images")


    uploaded_files = st.file_uploader(
        "Upload one (Right click on files and open or Drag them here )",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key=image_up_key
    )
    
    if uploaded_files:
        n = len(uploaded_files)
        for i,file in enumerate(uploaded_files):
            logger.progress(value=(i+1)/n,text=f"Processing image number {i+1}")
            img = Image.open(file)
            img = optimize_image(img)
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
        logger.empty()
            
# --------------------------------------------------------------------------
if uploader_selected == "PDF":
    
    st.title("Upload PDFs")


    uploaded_pdfs = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        accept_multiple_files=False,
        key=pdf_up_key,
        max_upload_size=1000
    )

    if uploaded_pdfs:
        logger.markdown(":green[Processing pdf...]")
        pdf_bytes = uploaded_pdfs.read()
        pages = pdf_to_pages(pdf_bytes,logger=logger)

        st.session_state["pages"].extend(pages)

        reset_keys()
        st.rerun()
        logger.empty()
            
            
if uploader_selected == "PPTX":
    
    st.title("Upload PPT (.pptx files)")


    uploaded_pptx = st.file_uploader(
        "Upload one or more PDF files",
        type=["pptx"],
        accept_multiple_files=False,
        key=ppt_up_key,
        max_upload_size=1000
    )

    if uploaded_pptx:
        logger.markdown(":green[Processing the PPT...]")
        pptx_bytes = uploaded_pptx.read()
        pages = get_pdf_from_pptx_managed(pptx_bytes)
        st.session_state["pages"].extend(pages)
            
        reset_keys()
        st.rerun()
            

st.success(f"Having {len(st.session_state['pages'])} pdf pages")

if st.session_state["pages"]:
    st.subheader("Current Images")
    for i, page in enumerate(st.session_state["pages"]):
        st.image(
            page["image"],
            caption=f"Image {i + 1}",
            width="stretch"
        )

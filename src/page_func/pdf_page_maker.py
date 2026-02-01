import base64
from pathlib import Path
import streamlit as st
import uuid
from utils import markdown_to_a4_pdf_page,markdown_to_pdf_bytes_IMPROVED
from utils.pdf_to_image import get_pages_as_bytes, pdf_to_pages
from utils.pdfpage_Class import PDFPage

st.title("Markdown Editor → PDF Page",help="""
         for images: 
         ![Alt text description](image_url_or_path.jpg "Optional image title")
         for links:
         [Link text goes here](https://www.example.com)
         """)
st.link_button("Markdown/HTML Helper",url="https://www.markdownguide.org/basic-syntax/")

if "markdown_history" not in st.session_state:
    st.session_state["markdown_history"] = []

if "pages" not in st.session_state:
    st.session_state["pages"] = []


col_editor, col_preview = st.columns(2)

with col_editor:
    st.subheader("Write Markdown")
    
    
    with st.popover("See History"):
        st.subheader("all markdown history :material/arrow_downward:")
        for his in st.session_state["markdown_history"]:
            st.markdown("---")
            st.code(his)
            
            
    markdown_text = st.text_area(
        "Markdown Input",
        height=500,
        placeholder=(
            "# Title\n\n"
            "Write **markdown** here.\n\n"
            "- Bullet point\n"
            "- Another point\n\n"
            "[Link](https://example.com)\n\n"
            "![Image](https://via.placeholder.com/300)"
        ),
    )

with col_preview:
    st.subheader("Live Preview")

    if markdown_text.strip():
        st.session_state["markdown_history"].append(markdown_text)
        st.markdown(markdown_text, unsafe_allow_html=False)
    else:
        st.info("Markdown preview will appear here.")

st.markdown("---")


col_create, col_clear = st.columns([1, 1])

with col_create:
    if st.button("Create PDF Page from Markdown", disabled=(not markdown_text.strip())):
        pdf_bytes = markdown_to_pdf_bytes_IMPROVED(markdown_text)
        pages_bytes = get_pages_as_bytes(pdf_bytes)
        if len(pages_bytes) > 1:
            st.error("Overflow Error, This markdown is too large to fit in one page. Try writing smaller markdown so that it fits in a single pdf A4 page, save it and write the rest of the markdown in another page.")
        else:
            st.session_state["pages"].append(
                PDFPage({
                "page_id": str(uuid.uuid4()),
                "image": None,            
                "pdf_bytes": pdf_bytes,
                "markdown_text":markdown_text,
                "ocr_applied":True
            }))

            st.success("PDF page created and added to document.")

with col_clear:
    if st.button("Clear Editor"):
        st.rerun()



def streamlit_img_to_markdown(uploaded_file):
    if uploaded_file is not None:
        
        file_bytes = uploaded_file.getvalue()
        
        mime_type = uploaded_file.type
        
        base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
        
        markdown_tag = f'![{uploaded_file.name}](data:{mime_type};base64,{base64_encoded})'
        
        return markdown_tag.encode('utf-8')


with st.popover("Bytes utility for images"):
    image_file = st.file_uploader("Upload image here",accept_multiple_files=False,type=["jpg","jpeg","png"])
    bt = st.button("get bytes string")
    if bt:
        st.code(streamlit_img_to_markdown(image_file))
    
    
import PIL.Image
import streamlit as st
from utils import image_to_single_page_pdf, compress_image_for_pdf,pdf_page_to_image
from utils import markdown_to_a4_pdf_page

st.set_page_config(layout="wide")

st.title("Reorder / Rotate / Delete Images")

pages = st.session_state["pages"]

if not pages:
    st.error("No images uploaded.")
    st.stop()

for i, page in enumerate(pages):
    st.markdown("---")
    col1, col2, col3 = st.columns([1.2, 1.2, 6])

    
    with col1:
        if st.button(":material/arrow_upward: Move", key=f"up_{page['id']}") and i > 0:
            pages[i - 1], pages[i] = pages[i], pages[i - 1]
            st.rerun()

        if st.button(":material/sync: Rotate", key=f"rotate_{page['id']}"):
            page["image"] = page["image"].rotate(-90, expand=True)
            page["pdf_bytes"] = image_to_single_page_pdf(page["image"])
            st.rerun()
        
        if st.button("Compress", key=f"compress_{page['id']}"):
            page["image"] = compress_image_for_pdf(page["image"])
            page["pdf_bytes"] = image_to_single_page_pdf(page["image"])
            st.success("Image compressed")
            st.rerun()

  
    with col2:
        if st.button(":material/arrow_downward: Move", key=f"down_{page['id']}") and i < len(pages) - 1:
            pages[i + 1], pages[i] = pages[i], pages[i + 1]
            st.rerun()

        if st.button(":material/delete: Delete", key=f"delete_{page['id']}"):
            pages.pop(i)
            st.rerun()
            
                
        ocr_applied = page.get("ocr_applied", False)

        if st.button(
            "View OCR Page",
            key=f"view_ocr_{page['id']}",
            disabled=not ocr_applied
        ):
            
            md_pdf_bytes = markdown_to_a4_pdf_page(page["ocr_text"])
            
            md_image = pdf_page_to_image(md_pdf_bytes)

            st.session_state[f"preview_override_{page['id']}"] = md_image

            st.rerun()

        
    with col3:
        override_key = f"preview_override_{page['id']}"

        if override_key in st.session_state:
            st.image(
                st.session_state[override_key],
                caption=f"Page {i + 1} (OCR / Markdown view)",
            )

            if st.button("Back to Original View", key=f"back_{page['id']}"):
                del st.session_state[override_key]
                st.rerun()

        elif page.get("image",False):
            st.image(
                page["image"],
                caption=f"Page {i + 1}",
                width="content"
            )
        
        else:
            st.info(f"Image preview is not available for this Page, You can click the :green[View OCR page] to see the Page")



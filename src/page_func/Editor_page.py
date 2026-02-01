import PIL.Image
import streamlit as st
from utils import (
    image_to_single_page_pdf,
    compress_image_for_pdf,
    pdf_page_to_image,
    markdown_to_pdf_bytes_IMPROVED,
    PDFPage,
)

st.set_page_config(layout="wide")

st.title("Reorder / Rotate / Delete Images")

pages: list[PDFPage] = st.session_state["pages"]

if not pages:
    st.error("No images uploaded.")
    st.stop()

for i, page in enumerate(pages):
    st.markdown("---")
    col1, col2, col3 = st.columns([1.2, 1.2, 6])

    has_markdown = page["markdown_text"] is not None
    has_image = page["image"] is not None

    if not has_image and not has_markdown:
        st.info(":red[Invalid page state: both image and markdown are missing.]")
        continue

    with col1:
        if st.button(":material/arrow_upward: Move", key=f"up_{page['page_id']}") and i > 0:
            pages[i - 1], pages[i] = pages[i], pages[i - 1]
            st.rerun()

        if st.button(
            ":material/sync: Rotate",
            key=f"rotate_{page['page_id']}",
            disabled=has_markdown,
        ):
            page["image"] = page["image"].rotate(-90, expand=True)
            page["pdf_bytes"] = image_to_single_page_pdf(page["image"])
            st.rerun()

        if st.button(
            "Compress",
            key=f"compress_{page['page_id']}",
            disabled=has_markdown,
        ):
            page["image"] = compress_image_for_pdf(page["image"])
            page["pdf_bytes"] = image_to_single_page_pdf(page["image"])
            st.success("Image compressed")
            st.rerun()

    with col2:
        if st.button(":material/arrow_downward: Move", key=f"down_{page['page_id']}") and i < len(pages) - 1:
            pages[i + 1], pages[i] = pages[i], pages[i + 1]
            st.rerun()

        if st.button(":material/delete: Delete", key=f"delete_{page['page_id']}"):
            pages.pop(i)
            st.rerun()

        if st.button(
            "View OCR Page",
            key=f"view_ocr_{page['page_id']}",
            disabled=not has_markdown,
        ):
            if not page["ocr_applied"]:
                md_pdf_bytes = markdown_to_pdf_bytes_IMPROVED(page["markdown_text"])
            else:
                md_pdf_bytes = page["pdf_bytes"]
            md_image = pdf_page_to_image(md_pdf_bytes)
            st.session_state[f"preview_override_{page['page_id']}"] = md_image
            st.rerun()

    with col3:
        override_key = f"preview_override_{page['page_id']}"

        if override_key in st.session_state:
            st.image(
                st.session_state[override_key],
                caption=None,
            )

            if st.button("Back to Original View", key=f"back_{page['page_id']}"):
                del st.session_state[override_key]
                st.rerun()

        elif has_image:
            st.image(
                page["image"],
                caption=f"Page {i + 1}",
                width="content",
            )

        else:
            st.info(
                """Image preview is not available for this page. 
                You can click the View OCR Page button to see the page."""
            )

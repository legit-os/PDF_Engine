import streamlit as st
from utils import (
    deepseek_ocr_ollama,
    markdown_to_pdf_bytes_IMPROVED,
    get_pages_as_bytes,
    PDFPage,
)

st.title("OCR Review & Apply")

if "pages" not in st.session_state or not st.session_state["pages"]:
    st.warning("No pages available.")
    st.stop()

pages: list[PDFPage] = st.session_state["pages"]

st.info("Compare original pages with OCR output. Apply OCR when satisfied.")

for idx, page in enumerate(pages):
    st.markdown("---")
    st.subheader(f"Page {idx + 1}")

    has_image = page.image is not None
    has_markdown = page.markdown_text is not None

    if not has_image and not has_markdown:
        st.error("Invalid page state: both image and markdown are missing.")
        continue

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Original")
        if has_image:
            st.image(page.image)
        else:
            st.info("This page has no image. OCR cannot be applied.")
            continue

    with col_right:
        st.markdown("### OCR Output")

        if has_markdown:
            st.text_area(
                "OCR Preview",
                page.markdown_text,
                height=300,
            )
        else:
            st.info("OCR not generated yet.")

        col_run, col_apply, col_clear = st.columns(3)

        with col_run:
            if st.button(
                "Run OCR",
                key=f"run_{page.page_id}",
            ):
                with st.spinner("Running DeepSeek-OCR..."):
                    page.markdown_text = deepseek_ocr_ollama(
                        page.image,
                        instruction="Free OCR.",
                    )
                st.success("OCR completed")
                st.rerun()

        with col_apply:
            if has_markdown:
                if st.button(":green[Apply OCR]", key=f"apply_{page.page_id}"):
                    merged_pdf = markdown_to_pdf_bytes_IMPROVED(page.markdown_text)
                    pdf_pages = get_pages_as_bytes(merged_pdf)

                    new_pages = [
                        PDFPage(
                            page_id=page.page_id,
                            image=None,
                            pdf_bytes=pdf_bytes,
                            markdown_text=page.markdown_text,
                        )
                        for pdf_bytes in pdf_pages
                    ]

                    pages.pop(idx)
                    for offset, new_page in enumerate(new_pages):
                        pages.insert(idx + offset, new_page)

                    st.success("OCR applied to PDF page(s)")
                    st.rerun()

        with col_clear:
            if has_markdown:
                if st.button("Clear OCR", key=f"clear_{page.page_id}"):
                    page.markdown_text = None
                    st.info("OCR cleared")
                    st.rerun()

    if has_markdown:
        st.success(":green[OCR text present for this page]")
    else:
        st.warning(":red[OCR not applied]")

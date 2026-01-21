import streamlit as st
from utils import deepseek_ocr_ollama
from utils.ocr_engine import markdown_to_a4_pdf_page  

st.title("OCR Review & Apply")

if "pages" not in st.session_state or not st.session_state["pages"]:
    st.warning("No pages available.")
    st.stop()

pages = st.session_state["pages"]


# if st.button("debug"):
#     text = deepseek_ocr_ollama(
#         st.session_state["pages"][0]["image"],"""
#     Free OCR."""
#     )
#     st.text_area("OCR Output", text, height=300)



st.info("Compare original pages with OCR output. Apply OCR only when satisfied.")



for idx, page in enumerate(pages):
    st.markdown("---")
    st.subheader(f"Page {idx + 1}")

    col_left, col_right = st.columns(2)

    
    with col_left:
        st.markdown("### Original")
        st.image(page["image"])

    
    with col_right:
        st.markdown("### OCR Output")

        ocr_key = f"ocr_text_{page['id']}"

        if ocr_key not in st.session_state:
            st.info("OCR not generated yet.")

        else:
            st.text_area(
                "OCR Preview",
                st.session_state[ocr_key],
                height=300
            )

        
        col_run, col_apply, col_clear = st.columns(3)

        with col_run:
            if st.button("Run OCR", key=f"run_{page['id']}"):
                with st.spinner("Running DeepSeek-OCR..."):
                    ocr_text = deepseek_ocr_ollama(
                        page["image"],
                        instruction="Free OCR."
                    )
                st.session_state[ocr_key] = ocr_text
                st.success("OCR completed")
                st.rerun()

        with col_apply:
            if ocr_key in st.session_state:
                if st.button(":green[Apply OCR]", key=f"apply_{page['id']}"):
                    page["pdf_bytes"] = markdown_to_a4_pdf_page(
                        st.session_state[ocr_key]
                    )
                    page["ocr_text"] = st.session_state[ocr_key]
                    page["ocr_applied"] = True
                    st.success("OCR applied to PDF page")
                    st.rerun()

        with col_clear:
            if ocr_key in st.session_state:
                if st.button("Clear OCR", key=f"clear_{page['id']}"):
                    del st.session_state[ocr_key]
                    st.info("OCR cleared")
                    st.rerun()


    if page.get("ocr_applied"):
        st.success(":green[OCR applied to this page]")
    else:
        st.warning(":red[OCR not applied]")

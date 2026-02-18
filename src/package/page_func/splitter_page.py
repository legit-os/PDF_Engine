import streamlit as st
from package.utils.splitter import split_pdf_spread_bytes

st.set_page_config(layout="wide")

st.title("Convert 2-in-1 Pages to Single Pages")

if "pages" not in st.session_state or not st.session_state["pages"]:
    st.warning("No pages available.")
    st.stop()

pages = st.session_state["pages"]
total_pages = len(pages)

st.info(f"Total Pages: {total_pages}")

start, end = st.slider(
    "Select Page Range (inclusive)",
    min_value=1,
    max_value=total_pages,
    value=(1, total_pages),
)

st.markdown("---")

if st.button("Split Selected Pages"):
    log_container = st.empty()
    
    with st.spinner("Splitting pages..."):

        start_idx = start - 1
        end_idx = end - 1

        for i in range(end_idx, start_idx - 1, -1):
            original_page = pages[i]
            log_container.progress((end_idx-i)/(end_idx-start_idx),f"Processing page number {i}")

            split_pages = split_pdf_spread_bytes(original_page["pdf_bytes"])

            pages.pop(i)

            for offset, new_page in enumerate(split_pages):
                pages.insert(i + offset, new_page)

    log_container.empty()
    
    st.success("Selected pages converted successfully.")
    st.rerun()

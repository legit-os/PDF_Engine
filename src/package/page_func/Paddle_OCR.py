import re

import streamlit as st

from package.utils import apply_paddle_docker_ocr

st.title("Apply Paddle OCR to Selected Pages")
st.warning("THIS REQUIRES :red[**DOCKER**] ENGINE TO BE RUNNING")

if "pages" not in st.session_state or not st.session_state["pages"]:
    st.error("No pages in session")
    st.stop()

pages = st.session_state["pages"]
page_count = len(pages)
page_ranges = st.text_input(
    "Page numbers or ranges to process",
    placeholder="1-15,19,37",
    help="Leave blank to process every page. Otherwise enter 1-based page numbers and inclusive ranges, separated by commas.",
    key="paddle_ocr_page_ranges",
)

selected_indices: set[int] = set()
range_error = None

if page_ranges.strip():
    for part in page_ranges.split(","):
        token = part.strip()
        match = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?", token)
        if not match:
            range_error = f"'{token}' is invalid. Use page numbers and ranges like 1-15,19,37."
            break

        start = int(match.group(1))
        end = int(match.group(2) or start)
        if start < 1 or end < 1 or start > page_count or end > page_count:
            range_error = f"Page numbers must be between 1 and {page_count}."
            break
        if start > end:
            range_error = f"Range '{token}' must start with the smaller page number."
            break

        selected_indices.update(range(start - 1, end))

if range_error:
    st.error(range_error)
    selected_pages = []
else:
    selected_pages = [
        page for index, page in enumerate(pages)
        if not page_ranges.strip() or index in selected_indices
    ]
    eligible_count = sum(
        page["image"] is not None and page["markdown_text"] is None
        for page in selected_pages
    )
    st.caption(f"{len(selected_pages)} pages selected; {eligible_count} eligible for OCR.")

if st.button(
    "Run OCR on Selected Pages",
    disabled=bool(range_error) or not selected_pages or eligible_count == 0,
):
    with st.spinner("Running Paddle OCR Docker..."):
        apply_paddle_docker_ocr(selected_pages)
    st.success("Paddle OCR applied to eligible selected pages.")

import re

import streamlit as st

from package.utils import merge_pdf_pages, reset_keys
from package.utils.image_compressor import compress_pdf

reset_keys()

if "pages" not in st.session_state:
    st.error("Go to the Uploader page and Upload documents to create to pdf")
    st.stop()
elif len(st.session_state["pages"]) == 0:
    st.error("No pdfs or images uploaded")
    st.stop()

st.header("Export")

st.subheader("Select Pages")
page_ranges = st.text_input(
    "Page numbers or ranges to include",
    placeholder="1-15,19,37",
    help="Leave blank to include every page. Otherwise enter 1-based page numbers and inclusive ranges, separated by commas.",
    key="pages_to_include",
)

all_pages = st.session_state["pages"]
page_count = len(all_pages)
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
        page for index, page in enumerate(all_pages)
        if not page_ranges.strip() or index in selected_indices
    ]
    st.caption(f"{len(selected_pages)} of {page_count} pages selected.")

st.subheader("Merge")
if st.button("Merge Selected Pages", disabled=bool(range_error)):
    merged_pdf = merge_pdf_pages(selected_pages)
    st.session_state["merged_pdf"] = merged_pdf
    st.session_state["comp_pdf"] = merged_pdf
    st.session_state["merged_page_ids"] = tuple(page["page_id"] for page in selected_pages)
    st.success(f"{len(selected_pages)} pages merged successfully.")
    st.info(f"Pdf size : {(len(merged_pdf) / 1024):.2f} KBs")
    st.info(f"Pdf size in MBs : {(len(merged_pdf) / (1024*1024)):.2f} MBs")

current_page_ids = tuple(page["page_id"] for page in selected_pages)
has_current_merge = (
    not range_error
    and "merged_pdf" in st.session_state
    and st.session_state.get("merged_page_ids") == current_page_ids
)

if has_current_merge:
    st.subheader("Compress")
    unit = st.radio("Unit", ["KBs", "MBs"], index=1)
    size = st.number_input(
        "Size of the pdf in the selected unit",
        min_value=0.0001,
        value=(len(st.session_state["merged_pdf"]) / (1024*1024)),
    )
    if unit == "MBs":
        size *= 1024
    quality = st.slider(label="Quality of the pdf", min_value=1, max_value=99, value=85)

    if st.button("Compress PDF"):
        st.session_state["comp_pdf"], final_size = compress_pdf(
            st.session_state["merged_pdf"],
            target_size_kb=size,
            quality=quality,
        )
        st.success(f"PDF Compressed to {final_size:.2f} KBs or {(final_size / 1024):.2f} MBs")

    st.subheader("Download")
    st.download_button(
        label="Download Final PDF",
        data=st.session_state["comp_pdf"],
        file_name="merged_document.pdf",
        mime="application/pdf",
    )
elif not range_error and "merged_pdf" in st.session_state:
    st.caption("Merge the current page selection to continue to compression and download.")

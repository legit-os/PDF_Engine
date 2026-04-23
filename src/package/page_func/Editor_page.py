import io
import uuid
from PIL import Image
import streamlit as st
from package.utils import (
    image_to_single_page_pdf,
    compress_image_for_pdf,
    pdf_page_to_image,
    markdown_to_pdf_bytes_IMPROVED,
    PDFPage,
    get_compressed_image,
    get_image_filesize
)
from package.utils.pdf_to_text import extract_text_from_pdf_bytes
from package.utils import reset_keys

reset_keys()

st.set_page_config(layout="wide")

st.title("Reorder / Rotate / Delete Images")

pages: list[PDFPage] = st.session_state["pages"]

if not pages:
    st.error("No images uploaded.")
    st.stop()

st.subheader("Delete Pages")
col_del_1, col_del_2 = st.columns([4, 1])
with col_del_1:
    to_delete = st.multiselect(
        "Select pages to delete",
        options=range(len(pages)),
        format_func=lambda i: f"Page {i+1}",
        key="bulk_delete_select"
    )
with col_del_2:
    st.write("##") 
    if st.button("Delete Selected", type="primary", use_container_width=True):
        if to_delete:
            st.session_state["pages"] = [p for i, p in enumerate(pages) if i not in to_delete]
            st.rerun()
        else:
            st.warning("No pages selected.")

st.markdown("---")
st.subheader("Move Pages")
move_col1, move_col2, move_col3 = st.columns([2, 1, 1])

with move_col1:
    to_move = st.multiselect(
        "Select pages to move",
        options=range(len(pages)),
        format_func=lambda i: f"Page {i+1}",
        key="bulk_move_select"
    )

with move_col2:
    move_pos = st.selectbox(
        "Move to",
        options=["Start", "End", "Before Page", "After Page"],
        key="move_position_select"
    )

target_page = None
if move_pos in ["Before Page", "After Page"]:
    with move_col3:
        target_page = st.number_input(
            "Target Page Number",
            min_value=1,
            max_value=len(pages),
            value=1,
            key="move_target_input"
        )

if st.button("Move Selected", type="secondary", use_container_width=True):
    if not to_move:
        st.warning("Please select pages to move.")
    else:
        selected_indices = sorted(to_move)
        moved_pages = [pages[i] for i in selected_indices]
        remaining_pages = [p for i, p in enumerate(pages) if i not in selected_indices]
        
        target_idx = 0
        if move_pos == "Start":
            target_idx = 0
        elif move_pos == "End":
            target_idx = len(remaining_pages)
        else:
            ref_idx = target_page - 1
            if ref_idx in selected_indices:
                st.error("Target page cannot be one of the pages you are moving.")
            elif ref_idx < 0 or ref_idx >= len(pages):
                st.error("Invalid target page number.")
            else:
                ref_page_obj = pages[ref_idx]
                try:
                    new_ref_idx = remaining_pages.index(ref_page_obj)
                    if move_pos == "Before Page":
                        target_idx = new_ref_idx
                    else: # After Page
                        target_idx = new_ref_idx + 1
                except ValueError:
                    st.error("Target page mapping error.")
                    st.stop()
        
        if not st.session_state.get("error_flag", False):
            st.session_state["pages"] = (
                remaining_pages[:target_idx] + 
                moved_pages + 
                remaining_pages[target_idx:]
            )
            st.rerun()

st.markdown("---")

@st.fragment()
def editor_object(i:int,page):
    st.markdown("---")
    col1, col2, col3 = st.columns([1.2, 1.2, 6])

    has_markdown = page["markdown_text"] is not None
    has_image = page["image"] is not None

    if not has_image and not has_markdown:
        st.info(":red[Invalid page state: both image and markdown are missing.]")
        return None

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
            st.rerun(scope="fragment")

        with st.popover(
            "Compress",
            key=f"compress_{page['page_id']}",
            disabled=has_markdown,
        ):
            st.warning("Image file sizes displayed are generally very different from the real size on you file system")
            size_kb, size_mb = get_image_filesize(page["image"])
            st.info(f"Size of the image is {size_kb} KBs, or {size_mb} MBs")
            quality = st.slider("Quality",min_value=50,max_value=99, value=85,key=f"comp_slider{page['page_id']}")
            if st.button("Compress",key=f"compressor_{page['page_id']}"):
                st.session_state[f"{page['page_id']}_compressed"] = get_compressed_image(page["image"],
                                                                                         quality=quality)
            if st.session_state.get(f"{page['page_id']}_compressed",False):
                comp_size_kb, comp_size_mb = get_image_filesize(Image.open(io.BytesIO(st.session_state[f"{page['page_id']}_compressed"])))
                st.info(f"Compressed image size : {comp_size_kb} KBs , {comp_size_mb} MBs")

            if st.session_state.get(f"{page['page_id']}_compressed",False):
                st.download_button("Download compressed image",
                                   data=st.session_state[f"{page['page_id']}_compressed"],
                                   file_name="compressed_image.jpeg",
                                   mime="image/jpeg",
                                   key=f"comp_down_{page['page_id']}"
                                   )
            
            
        with st.popover(
            "Extract Text",
            width="stretch"
        ):
            text = extract_text_from_pdf_bytes(page["pdf_bytes"])
            st.code(text,language="python")
        
            

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
            st.rerun(scope="fragment")

    with col3:
        override_key = f"preview_override_{page['page_id']}"

        if override_key in st.session_state:
            st.image(
                st.session_state[override_key],
                caption=None,
            )

            if st.button("Back to Original View", key=f"back_{page['page_id']}"):
                del st.session_state[override_key]
                st.rerun(scope="fragment")

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



to_edit = st.multiselect(
    "Select pages to display in Editor",
    options=range(len(pages)),
    format_func=lambda i: f"Page {i+1}",
    default=[],
    key="editor_select"
)

for i in to_edit:
    editor_object(i, pages[i])
from package.utils import merge_pdf_pages
import streamlit as st
from package.utils import reset_keys
from package.utils.image_compressor import compress_pdf

reset_keys()


if "pages" not in st.session_state:
    st.error("Go to the Uploader page and Upload documents to create to pdf")
    st.stop()
elif len(st.session_state["pages"]) == 0:
    st.error("No pdfs or images uploaded")
    st.stop()

st.header("Export")


if st.button("Merge Pages into PDF"):
    merged_pdf = merge_pdf_pages(st.session_state["pages"])
    st.session_state["merged_pdf"] = merged_pdf
    st.session_state["comp_pdf"] = st.session_state["merged_pdf"]
    st.success("PDF merged successfully!")
    st.info(f"Pdf size : {(len(merged_pdf) / 1024):.2f} KBs")
    st.info(f"Pdf size in MBs : {(len(merged_pdf) / (1024*1024)):.2f} MBs")





if "merged_pdf" in st.session_state:
    unit = st.radio("Unit",["KBs","MBs"])
    size = st.number_input("Size of the pdf in the selected unit",min_value=0.0001,
                            value=(len(st.session_state["merged_pdf"]) / (1024*1024)))
    if unit == "MBs":
        size *= 1024
    quality = st.slider(label="Quality of the pdf",min_value=1,max_value=99,value=85)
    
    if st.button("Compress PDF"):
        st.session_state["comp_pdf"], final_size = compress_pdf(st.session_state["merged_pdf"],
                                                                  target_size_kb=size,quality=quality)
        
        st.success(f"PDF Compressed to {final_size:.2f} KBs or {(final_size / 1024):.2f} MBs")
    

if "comp_pdf" in st.session_state:
    st.download_button(
        label="Download Final PDF",
        data=st.session_state["comp_pdf"],
        file_name="merged_document.pdf",
        mime="application/pdf"
    )

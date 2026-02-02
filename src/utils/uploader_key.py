from typing import Literal
import uuid
import streamlit as st


def get_uploader_key(key:Literal["image","pdf","ppt"]):
    return f"{key}_uploader_{str(uuid.uuid4())}"


def check_up_keys(search_key:Literal["image","pdf","ppt"]):
    session_keys = st.session_state.keys()
    
    for key in session_keys:
        if key.startswith(f"{search_key}_uploader_"):
            return True,key
    
    return False,None
    
            
def reset_keys():
    has_pdf , pdf_key = check_up_keys("pdf")
    has_img , image_key = check_up_keys("image")
    has_ppt , ppt_key = check_up_keys("ppt")
    
    if has_pdf:
        st.session_state.pop(pdf_key)
    if has_img:
        st.session_state.pop(image_key)
    if has_ppt:
        st.session_state.pop(ppt_key)
    
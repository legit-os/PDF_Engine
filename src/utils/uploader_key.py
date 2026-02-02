from typing import Literal
import uuid
import streamlit as st


def get_pdf_uploader_key():
    return f"pdf_uploader_{str(uuid.uuid4())}"

def get_image_uploader_key():
    return f"image_uploader_{str(uuid.uuid4())}"

def check_up_keys(key:Literal["img","pdf"]):
    session_keys = st.session_state.keys()
    if key == "img":
        for key in session_keys:
            if key.startswith("image_uploader_"):
                return True,key
        
        return False,None
    
    elif key == "pdf":
        for key in session_keys:
            if key.startswith("pdf_uploader_"):
                return True,key
            
        return False,None
            
def reset_keys():
    has_pdf , pdf_key = check_up_keys("pdf")
    has_img , image_key = check_up_keys("img")
    
    if has_pdf:
        st.session_state.pop(pdf_key)
    if has_img:
        st.session_state.pop(image_key)
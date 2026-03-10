# from pypdf import PdfReader
# from io import BytesIO


# def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
#     try:
#         reader = PdfReader(BytesIO(pdf_bytes))

#         extracted_text = []

#         for page in reader.pages:
#             text = page.extract_text()
#             if text:
#                 extracted_text.append(text)

#         full_text = "\n".join(extracted_text).strip()

#         return full_text if full_text else ""

#     except Exception:
#         return ""

from io import BytesIO
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

def extract_text_from_pdf_bytes(pdf_bytes):
    try:
        return extract_text(BytesIO(pdf_bytes),laparams=LAParams(all_texts=True)).strip()
    except:
        return ""

# import io
# import pdfplumber

# def extract_text_from_bytes(pdf_bytes):
#     """
#     Takes PDF bytes and returns the extracted text as a string.
#     """
#     text_output = []
    
#     # Wrap bytes in a file-like object
#     with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
#         for page in pdf.pages:
#             # Extract text from the current page
#             page_text = page.extract_text()
#             if page_text:
#                 text_output.append(page_text)
                
#     # Join all pages with a double newline for readability
#     return "\n\n".join(text_output)

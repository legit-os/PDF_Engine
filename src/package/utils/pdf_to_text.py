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
from ast import List
from os import read
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_bytes
from io import BytesIO
import uuid

from utils.pdfpage_Class import PDFPage


def pdf_to_pages(pdf_bytes, dpi=150):

    reader = PdfReader(BytesIO(pdf_bytes))
    images = convert_from_bytes(pdf_bytes, dpi=dpi)

    pages = []

    for i, (page, img) in enumerate(zip(reader.pages, images)):
        writer = PdfWriter()
        writer.add_page(page)

        buffer = BytesIO()
        writer.write(buffer)
        buffer.seek(0)

        # pages.append({
        #     "id": str(uuid.uuid4()),
        #     "pdf_bytes": buffer.read(),
        #     "image": img.convert("RGB")
        # })

        pages.append(
            PDFPage(
                page_id=str(uuid.uuid4()),
                pdf_bytes= buffer.read(),
                image=img.convert("RGB"),
                markdown_text=None,
                ocr_applied=False
            )
        )

    return pages

from PIL import Image

def pdf_page_to_image(
    pdf_bytes: bytes,
    dpi: int = 150
) -> list[Image.Image]:
    
    images = convert_from_bytes(pdf_bytes, dpi=dpi)

    
    return images


import io
from pypdf import PdfReader, PdfWriter

def get_pages_as_bytes(pdf_bytes):
    
    reader = PdfReader(io.BytesIO(pdf_bytes))
    page_byte_list = []

    for page in reader.pages:
        writer = PdfWriter()
        writer.add_page(page)
        
        with io.BytesIO() as output_stream:
            writer.write(output_stream)
            page_byte_list.append(output_stream.getvalue())
            
    return page_byte_list

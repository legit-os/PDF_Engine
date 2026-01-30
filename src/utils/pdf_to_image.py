from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_bytes
from io import BytesIO
import uuid


def pdf_to_pages(pdf_bytes, dpi=150):
    """
    Takes full PDF bytes
    Returns list of page dicts:
    [{id, pdf_bytes, image}]
    """

    reader = PdfReader(BytesIO(pdf_bytes))
    images = convert_from_bytes(pdf_bytes, dpi=dpi)

    pages = []

    for i, (page, img) in enumerate(zip(reader.pages, images)):
        writer = PdfWriter()
        writer.add_page(page)

        buffer = BytesIO()
        writer.write(buffer)
        buffer.seek(0)

        pages.append({
            "id": str(uuid.uuid4()),
            "pdf_bytes": buffer.read(),
            "image": img.convert("RGB")
        })

    return pages

from PIL import Image

def pdf_page_to_image(
    pdf_bytes: bytes,
    dpi: int = 150
) -> Image.Image:
    
    images = convert_from_bytes(pdf_bytes, dpi=dpi)

    
    return images[0].convert("RGB")

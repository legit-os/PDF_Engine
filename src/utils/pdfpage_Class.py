from typing import TypedDict
from uuid import UUID

class PDFPage(TypedDict):
    page_id: UUID | str
    image: str = None
    pdf_bytes: bytes 
    markdown_text: str = None
    ocr_applied : bool = False
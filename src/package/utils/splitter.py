from pypdf import PdfReader, PdfWriter
from io import BytesIO
import copy
import uuid

from package.utils.pdf_to_image import pdf_page_to_image
from package.utils.pdfpage_Class import PDFPage


def split_pdf_spread_bytes(pdf_bytes: bytes):
    reader = PdfReader(BytesIO(pdf_bytes))
    result_pages = []

    for original_page in reader.pages:
        w = float(original_page.mediabox.width)
        h = float(original_page.mediabox.height)

        # -------- LEFT PAGE --------
        left_writer = PdfWriter()
        left_page = copy.deepcopy(original_page)

        left_page.mediabox.lower_left = (0, 0)
        left_page.mediabox.upper_right = (w / 2, h)

        left_writer.add_page(left_page)

        left_buffer = BytesIO()
        left_writer.write(left_buffer)
        left_buffer.seek(0)
        left_pdf_bytes = left_buffer.read()

        left_image = pdf_page_to_image(left_pdf_bytes)

        result_pages.append(
            PDFPage(
                page_id=uuid.uuid4(),
                image=left_image,
                pdf_bytes=left_pdf_bytes,
                markdown_text=None,
                ocr_applied=False,
            )
        )

        # -------- RIGHT PAGE --------
        right_writer = PdfWriter()
        right_page = copy.deepcopy(original_page)

        right_page.mediabox.lower_left = (w / 2, 0)
        right_page.mediabox.upper_right = (w, h)

        right_writer.add_page(right_page)

        right_buffer = BytesIO()
        right_writer.write(right_buffer)
        right_buffer.seek(0)
        right_pdf_bytes = right_buffer.read()

        right_image = pdf_page_to_image(right_pdf_bytes)

        result_pages.append(
            PDFPage(
                page_id=uuid.uuid4(),
                image=right_image,
                pdf_bytes=right_pdf_bytes,
                markdown_text=None,
                ocr_applied=False,
            )
        )

    return result_pages

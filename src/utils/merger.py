from pypdf import PdfWriter
from io import BytesIO

def merge_pdf_pages(pages):
    """
    pages: list of dicts with key 'pdf_bytes'
    returns: bytes (merged PDF)
    """
    merger = PdfWriter()

    for page in pages:
        merger.append(BytesIO(page["pdf_bytes"]))

    output = BytesIO()
    merger.write(output)
    merger.close()

    output.seek(0)
    return output.read()

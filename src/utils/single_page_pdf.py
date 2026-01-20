from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

def image_to_single_page_pdf(image):
    """
    image: PIL.Image
    returns: bytes (PDF data)
    """
    buffer = BytesIO()

    width, height = image.size
    c = canvas.Canvas(buffer, pagesize=(width, height))

    c.drawImage(
        ImageReader(image),
        0, 0,
        width=width,
        height=height
    )

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()

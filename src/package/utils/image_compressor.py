from PIL import Image

def compress_image_for_pdf(
    image: Image.Image,
    max_width: int = 2480,   
    quality: int = 85
) -> Image.Image:
    """
    Resize + recompress image safely for PDF usage.
    """
    w, h = image.size

    if w > max_width:
        ratio = max_width / w
        image = image.resize(
            (int(w * ratio), int(h * ratio)),
            Image.LANCZOS
        )

    return image

import io
from pypdf import PdfReader, PdfWriter

def compress_pdf(pdf_bytes, target_size_kb=None, quality=80):
    """
    Compresses PDF bytes. If target_size_kb is provided, it tries to 
    reach it by lowering image quality.
    """
    initial_size = len(pdf_bytes) / 1024
    
    current_bytes = pdf_bytes
    current_quality = quality
    
    while True:
        reader = PdfReader(io.BytesIO(current_bytes))
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        
        for page in writer.pages:
            page.compress_content_streams(level=9) 

        for page in writer.pages:
            for img in page.images:
                img.replace(img.image, quality=current_quality)

        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        compressed_data = output_buffer.getvalue()
        
        current_size = len(compressed_data) / 1024
        
        if not target_size_kb or current_size <= target_size_kb or current_quality <= 20:
            return compressed_data, current_size
        
        current_quality -= 20
        current_bytes = compressed_data




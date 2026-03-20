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

import io
from PIL import Image

def get_image_filesize(pil_img, quality=99):
    img_format = pil_img.format if pil_img.format else 'PNG'
    
    buffer = io.BytesIO()
    
    save_img = pil_img
    if img_format.upper() == "JPEG" and pil_img.mode in ("RGBA", "P"):
        save_img = pil_img.convert("RGB")
    
    if img_format.upper() == "JPEG":
        save_img.save(buffer, format="JPEG", quality=quality, optimize=True)
    else:
        save_img.save(buffer, format=img_format, optimize=True)

    size_bytes = len(buffer.getvalue())
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    # buffer.seek(0)
    
    return round(size_kb, 2), round(size_mb, 4)



def get_compressed_image(pil_img:Image.Image, quality=85): 
    if pil_img.mode in ("RGBA", "P"):
        background = Image.new("RGB", pil_img.size, (255, 255, 255))
        mask = pil_img.split()[3] if pil_img.mode == "RGBA" else None
        background.paste(pil_img, mask=mask)
        pil_img = background
    elif pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")

    buffer = io.BytesIO()
    pil_img.save(
        buffer, 
        format="JPEG", 
        quality=quality, 
        optimize=True,      
        progressive=True    
    )
    buffer.seek(0)
    return buffer.getvalue()


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




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

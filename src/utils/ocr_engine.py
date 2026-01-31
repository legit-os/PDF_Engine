import ollama
from PIL import Image
from io import BytesIO

def deepseek_ocr_ollama(
    image: Image.Image,
    instruction: str = "Free OCR."
) -> str:

    prompt = f"<image>\n{instruction}"


    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    response = ollama.chat(
        model="deepseek-ocr:3b",
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [image_bytes],
            }
        ],
    )

    return response["message"]["content"]



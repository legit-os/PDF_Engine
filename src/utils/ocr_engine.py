from typing import Literal
import ollama
from PIL import Image
from io import BytesIO

def deepseek_ocr_ollama(
    image: Image.Image,
    instruction: Literal["Free OCR.","<|grounding|>Convert the document to markdown.",
                         "Parse the figure."] = "Free OCR."
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



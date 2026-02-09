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







def glm_ocr_ollama(pil_image: Image, instruction: str = "Text Recognition:") -> str:
    """
    Uses Ollama's 'glm-ocr' model to convert an image to Markdown.
    
    Supported instruction prefixes:
    - 'Text Recognition:' (General OCR)
    - 'Table Recognition:' (Best for spreadsheets/tables)
    - 'Formula Recognition:' (Best for math/LaTeX)
    """
    # 1. Convert PIL Image to bytes
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()

    # 2. Call the Ollama generate API
    # Note: GLM-OCR typically uses 'generate' with specific prefixes in the prompt
    response = ollama.generate(
        model='glm-ocr',
        prompt=instruction,
        images=[img_bytes],
        options={
            'temperature': 0.1,  # Keep it low for high precision
            'num_ctx': 4096      # Standard context for GLM-OCR
        }
    )

    return response['response']




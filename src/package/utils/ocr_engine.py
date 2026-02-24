from typing import Literal
from httpx import stream
from matplotlib.ticker import StrMethodFormatter
import ollama
from PIL import Image
from io import BytesIO

import streamlit

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
    
    
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()

    response = ollama.generate(
        model='glm-ocr',
        prompt=instruction,
        images=[img_bytes],
        options={
            'temperature': 0.1, 
            'num_ctx': 4096      
        }
    )

    return response['response']

# import numpy as np
# from PIL import Image
# from paddleocr import PaddleOCR
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch

# def paddle_ocr_(pil_image, lang='en'):
#     # Initialize PaddleOCR instance
#     from paddleocr import PaddleOCR
#     ocr = PaddleOCR(
#         use_doc_orientation_classify=False,
#         use_doc_unwarping=False,
#         use_textline_orientation=False)

#     # Run OCR inference on a sample image 
#     result = ocr.predict(
#         input="https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png")

#     # Visualize the results and save the JSON results
#     for res in result:
#         res.print()
#         res.save_to_img("output")
#         res.save_to_json("output")
        
        
        
        
        
        
        
#     pdf_bytes = BytesIO()
#     width, height = pil_image.size
#     c = canvas.Canvas(pdf_bytes, pagesize=(width, height))
    
#     c.drawInlineImage(pil_image, 0, 0, width=width, height=height)
    
#     # Overlay OCR text (invisible layer for searchability)
#     for line in result:
#         box = line[0]     # Bounding box: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
#         text = line[1][0] # Extracted text
        
#         # Bottom-left coordinate of the box
#         # PDF coordinates start from bottom-left (0,0)
#         x = box[0][0]
#         y = height - box[2][1] 
        
#         # Set text parameters (render mode 3 makes text invisible but searchable)
#         c.setTextRenderMode(3) 
#         c.setFont("Helvetica", 10) # Base size; ideally, calculate based on box height
#         c.drawString(x, y, text)
        
#     c.save()
#     return pdf_bytes



# ----------------------------------------------------------------------------

# import io
# import numpy as np
# from PIL import Image
# from paddleocr import PaddleOCR
# from reportlab.pdfgen import canvas
# from reportlab.lib.utils import ImageReader

# # Initialize with current PP-OCRv5 configurations
# # 'lang="ch"' now simultaneously supports English, Japanese, and Pinyin in v5
# ocr_engine = PaddleOCR(
#     ocr_version='PP-OCRv5',
#     use_angle_cls=True,
#     lang='ch',              # Unified multilingual support in v5
# )

# def paddle_ocr__(pil_img):
#     """
#     Converts a PIL image to a searchable PDF using PP-OCRv5 Pipeline.
#     """
#     # 1. Convert PIL to NumPy for the engine
#     img_array = np.array(pil_img.convert("RGB"))
    
#     # 2. Extract OCR results using the modern result iterator
#     # Current API still uses .ocr() for quick tasks but requires 
#     # indexing adjustments for v5's structure
#     ocr_result = ocr_engine.predict(img_array, cls=True)
    
#     # 3. Initialize PDF Canvas
#     pdf_buffer = io.BytesIO()
#     width, height = pil_img.size
#     pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=(width, height))
    
#     # 4. Background: Original Image
#     img_reader = ImageReader(pil_img)
#     pdf_canvas.drawImage(img_reader, 0, 0, width, height)
    
#     # 5. Overlay: Searchable Text Layer
#     if ocr_result and ocr_result[0]:
#         for line in ocr_result[0]:
#             box = line[0]      # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
#             text = line[1][0]   # Recognized text string
            
#             # Coordinate Translation (OCR Top-Left -> PDF Bottom-Left)
#             x_min = box[0][0]
#             y_top = box[0][1]
#             y_bot = box[2][1]
            
#             box_height = abs(y_bot - y_top)
#             pdf_y = height - y_bot  # Flip Y-axis
            
#             # Set Text to 'Invisible' (Mode 3)
#             pdf_canvas.setTextRenderMode(3)
#             # v5 is more accurate; font scaling helps matching selection area
#             pdf_canvas.setFont("Helvetica", max(1, box_height * 0.8))
#             pdf_canvas.drawString(x_min, pdf_y, text)
            
#     pdf_canvas.showPage()
#     pdf_canvas.save()
    
#     pdf_buffer.seek(0)
#     return pdf_buffer.getvalue()







# =========================================================================
import subprocess
import tempfile
import json
import uuid
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO


def apply_paddle_docker_ocr(pages: list):
    streamlit.text("Reading pages...")
    eligible_pages = [
        page for page in pages
        if page["image"] is not None and page["markdown_text"] is None
    ]

    if not eligible_pages:
        return
    
    time_estimate = len(eligible_pages)*20 + len(eligible_pages)*5 + 300
    
    streamlit.info(f"Processing {len(eligible_pages)} pages, Estimated Time=> {time_estimate//3600} hours , {time_estimate//60 - (time_estimate//3600)*60} minutes")
    
    streamlit.text("Setting docker...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        input_dir = tmpdir / "input_path"
        output_dir = tmpdir / "output_path"

        input_dir.mkdir()
        output_dir.mkdir()

        for page in eligible_pages:
            img_path = input_dir / f"{page['page_id']}.png"
            page["image"].save(img_path)
        streamlit.text("Running Docker...")
        subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{input_dir}:/app/io/input_path",
                "-v", f"{output_dir}:/app/io/output_path",
                "--name", "paddleocr-docker",
                "legitos/paddleocr-docker:v1",
            ],
            check=True,
            timeout=time_estimate
        )
        streamlit.text("OCR done, Creating pdf pages...")
        for page in eligible_pages:
            json_path = output_dir / f"{page['page_id']}.json"
            if not json_path.exists():
                continue

            with open(json_path, "r", encoding="utf-8") as f:
                ocr_data = json.load(f)

            image = page["image"]
            width, height = image.size

            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=(width, height))

            c.drawImage(ImageReader(image), 0, 0, width=width, height=height)

            c.setFillColorRGB(0, 0, 0, alpha=0)

            for item in ocr_data:
                text = item.get("text", "")
                box = item.get("box", [])

                if not box or len(box) != 4:
                    continue

                x1, y1, x2, y2 = box

                pdf_x = x1
                pdf_y = height - y2

                font_size = max(6, int(y2 - y1))

                c.setFont("Helvetica", font_size)
                c.drawString(pdf_x, pdf_y, text)

            c.showPage()
            c.save()

            buffer.seek(0)
            page["pdf_bytes"] = buffer.read()
            page["ocr_applied"] = True
            
    subprocess.run(
        [
            "docker","rm","paddleocr-docker"
        ]
    )
    streamlit.text("**Done**")

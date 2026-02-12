def extract_boxes_with_text(ocr_dict: dict):
    boxes = ocr_dict.get("rec_boxes", [])
    texts = ocr_dict.get("rec_texts", [])

    results = []

    for box, text in zip(boxes, texts):
        if not text:
            continue

        results.append({
            "box": box,
            "text": text
        })

    return results




import numpy as np
import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict
import uvicorn

from paddleocr import PaddleOCR 

ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv5_server_det",
    text_recognition_model_name="PP-OCRv5_server_rec",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False, 
    use_textline_orientation=False, 
)

app = FastAPI(title="OCR API")


def run_ocr(image) -> dict:
    
    result = ocr.predict(image)[0]
    
    return result
    


@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()

    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    ocr_output = run_ocr(image)

    results = extract_boxes_with_text(ocr_output)

    return JSONResponse(content=results)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=11000, reload=True)

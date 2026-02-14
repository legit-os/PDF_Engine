import json
from pathlib import Path

import numpy as np
from paddleocr import PaddleOCR  
from PIL import Image

def extract_boxes_with_text(ocr_dict: dict):
    boxes = ocr_dict.get("rec_boxes", [])
    texts = ocr_dict.get("rec_texts", [])

    results = []

    for box, text in zip(boxes, texts):
        if not text:
            continue

        results.append({
            "box": box.tolist(),
            "text": text
        })

    return results

ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv5_server_det",
    text_recognition_model_name="PP-OCRv5_server_rec",
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False, 
    use_textline_orientation=False, 
)


input_path = Path("io/input_path")

output_path = Path("io/output_path")
if not output_path.exists():
    output_path.mkdir()

images:list[tuple[Path,np.ndarray]] = []
outputs = []

for i in input_path.walk():
    path,folders,files = i
    
    if len(files) == 0:
        continue
    
    else:
        for file in files:
            img_path = path / file
            img = Image.open(img_path)
            img_array = np.array(img)
            images.append((img_path,img_array))
        break

results = ocr.predict([i[1] for i in images])

n = len(results)

for i in range(n):
    output_file_name = images[i][0].stem
    
    output_file_path = output_path / f"{output_file_name}.json"
    
    with open(output_file_path, "w") as f:
        json.dump(extract_boxes_with_text(results[i]),f,indent=4)
    
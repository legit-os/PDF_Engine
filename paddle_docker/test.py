# import numpy as np
# from paddleocr import TextDetection
# from PIL import Image
# from io import BytesIO

# # buffer = BytesIO()

# # image = Image.open(r"Quiz 1.jpg.jpeg")

# # image = np.array(image)


# # model = TextDetection(model_name="PP-OCRv5_server_det")
# # output = model.predict(input=image, batch_size=1)
# # for res in output:
# #     res.print()
# #     res.save_to_img(save_path="./output/")
# #     res.save_to_json(save_path="./output/res.json")
    
# # def extract_boxes_with_text(ocr_dict: dict):
# #     boxes = ocr_dict.get("rec_boxes", [])
# #     texts = ocr_dict.get("rec_texts", [])

# #     results = []

# #     for box, text in zip(boxes, texts):
# #         if not text:
# #             continue

# #         results.append({
# #             "box": box.tolist(),
# #             "text": text
# #         })

# #     return results

# import json
# from paddleocr import PaddleOCR  

# ocr = PaddleOCR(
#     text_detection_model_name="PP-OCRv5_server_det",
#     text_recognition_model_name="PP-OCRv5_server_rec",
#     use_doc_orientation_classify=False, # Disables document orientation classification model via this parameter
#     use_doc_unwarping=False, # Disables text image rectification model via this parameter
#     use_textline_orientation=False, # Disables text line orientation classification model via this parameter
#     text_detection_model_dir="model",
#     text_recognition_model_dir="model"
# )
# result = ocr.predict(image)  
# for res in result:  
#     res.print()  
#     # res.save_to_img("ocr")  
#     # res.save_to_json("ocr")
#     with open("out.json","w") as f:
#         json.dump({"ocr":extract_boxes_with_text(res)},f,indent=4)
    
    
from .single_page_pdf import image_to_single_page_pdf
from .merger import merge_pdf_pages
from .pdf_to_image import pdf_to_pages, pdf_page_to_image,get_pages_as_bytes
from .ocr_engine import deepseek_ocr_ollama,glm_ocr_ollama,apply_paddle_docker_ocr
from .image_compressor import compress_image_for_pdf, get_image_filesize, get_compressed_image
from .markdown_to_pdf import markdown_to_a4_pdf_page,markdown_to_pdf_bytes_IMPROVED
from .pdfpage_Class import PDFPage
from .uploader_key import get_uploader_key,check_up_keys,reset_keys
from .ppt_to_pdf import get_pdf_from_pptx,get_pdf_from_pptx_managed

# class PDFPage(TypedDict):
#     page_id: UUID
#     image: str = None
#     pdf_bytes: bytes 
#     markdown_text: str = ""
#     ocr_applied : bool = False
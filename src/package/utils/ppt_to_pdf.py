from spire.presentation.common import *
from spire.presentation import *
from tempfile import TemporaryDirectory
from PIL import Image
import uuid

from .single_page_pdf import image_to_single_page_pdf
from .pdfpage_Class import PDFPage

from spire.presentation.common import *
from spire.presentation import *
from tempfile import TemporaryDirectory


def split_pptx_bytes(pptx_bytes: bytes, chunk_size: int = 9):
    pptx_chunks = []

    with TemporaryDirectory() as tmpdir:
        input_path = f"{tmpdir}/input.pptx"
        with open(input_path, "wb") as f:
            f.write(pptx_bytes)

        source_presentation = Presentation()
        source_presentation.LoadFromFile(input_path)

        total_slides = source_presentation.Slides.Count

        for start in range(0, total_slides, chunk_size):
            chunk_presentation = Presentation()
            chunk_presentation.Slides.RemoveAt(0)

            end = min(start + chunk_size, total_slides)

            for i in range(start, end):
                chunk_presentation.Slides.AppendBySlide(
                    source_presentation.Slides[i]
                )

            chunk_path = f"{tmpdir}/chunk_{start}.pptx"
            chunk_presentation.SaveToFile(chunk_path, FileFormat.Pptx2013)
            chunk_presentation.Dispose()

            with open(chunk_path, "rb") as f:
                pptx_chunks.append(f.read())

        source_presentation.Dispose()

    return pptx_chunks

def get_pdf_from_pptx_managed(pptx_bytes: bytes):
    byte_list = split_pptx_bytes(pptx_bytes=pptx_bytes)
    pages = []
    
    for bytes in byte_list:
        pages.extend(get_pdf_from_pptx(bytes))
        
    return pages

def get_pdf_from_pptx(pptx_file: bytes):
    pages = []

    with TemporaryDirectory() as tmpdir:
        pptx_path = f"{tmpdir}/input.pptx"

        with open(pptx_path, "wb") as f:
            f.write(pptx_file)

        presentation = Presentation()
        presentation.LoadFromFile(pptx_path)

        for i, slide in enumerate(presentation.Slides):
            image_path = f"{tmpdir}/slide_{i}.png"

            image = slide.SaveAsImage()
            image.Save(image_path)
            image.Dispose()

            pil_image = Image.open(image_path).convert("RGB")
            pdf_bytes = image_to_single_page_pdf(pil_image)

            pages.append(
                PDFPage(
                    page_id=str(uuid.uuid4()),
                    image=pil_image,
                    pdf_bytes=pdf_bytes,
                    markdown_text=None,
                    ocr_applied=False
                )
            )

        presentation.Dispose()

    return pages


if __name__ == "__main__":                 # only for testing if spire is working perfectly, since I don't use it

    # Create a Presentation object
    presentation = Presentation()

    # Load a PowerPoint presentation
    presentation.LoadFromFile("example.pptx")

    # Loop through the slides in the presentation
    for i, slide in enumerate(presentation.Slides):
        # Specify the output file name
        fileName ="Output/ToImage_" + str(i) + ".png"
        # Save each slide as a PNG image
        image = slide.SaveAsImage()
        image.Save(fileName)
        image.Dispose()

    presentation.Dispose()
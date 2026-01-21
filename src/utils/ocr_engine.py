

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


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
import re


def markdown_to_a4_pdf_page(markdown_text: str) -> bytes:
    """
    Convert markdown text into a single A4 PDF page.

    Returns:
        pdf_bytes (bytes)
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    
    styles.add(
        ParagraphStyle(
            name="H1",
            fontSize=18,
            leading=22,
            spaceAfter=12,
            spaceBefore=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            fontSize=15,
            leading=18,
            spaceAfter=10,
            spaceBefore=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H3",
            fontSize=13,
            leading=16,
            spaceAfter=8,
            spaceBefore=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontSize=10.5,
            leading=14,
            spaceAfter=6,
        )
    )

    story = []

    lines = markdown_text.splitlines()
    bullet_buffer = []

    def flush_bullets():
        nonlocal bullet_buffer
        if bullet_buffer:
            story.append(
                ListFlowable(
                    [
                        ListItem(
                            Paragraph(item, styles["Body"]),
                            bulletText="•",
                        )
                        for item in bullet_buffer
                    ],
                    start="bullet",
                    leftIndent=12,
                )
            )
            bullet_buffer = []

    for line in lines:
        line = line.strip()

        if not line:
            flush_bullets()
            story.append(Spacer(1, 6))
            continue

        
        if line.startswith("### "):
            flush_bullets()
            story.append(Paragraph(line[4:], styles["H3"]))
        elif line.startswith("## "):
            flush_bullets()
            story.append(Paragraph(line[3:], styles["H2"]))
        elif line.startswith("# "):
            flush_bullets()
            story.append(Paragraph(line[2:], styles["H1"]))

        
        elif line.startswith("- ") or line.startswith("* "):
            bullet_buffer.append(line[2:])

    
        else:
            flush_bullets()
            
            safe_line = (
                line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            story.append(Paragraph(safe_line, styles["Body"]))

    flush_bullets()

    doc.build(story)

    buffer.seek(0)
    return buffer.read()

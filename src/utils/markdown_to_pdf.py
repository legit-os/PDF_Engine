from io import BytesIO
import re

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

import matplotlib.pyplot as plt


def _latex_to_image(latex: str, fontsize=14) -> BytesIO:
    """
    Render LaTeX to an image using matplotlib and return BytesIO.
    """
    buf = BytesIO()
    fig = plt.figure()
    fig.patch.set_alpha(0)

    # Remove $$ if present
    latex = latex.strip()
    if latex.startswith("$$") and latex.endswith("$$"):
        latex = latex[2:-2]

    plt.text(
        0.5,
        0.5,
        f"${latex}$",
        fontsize=fontsize,
        ha="center",
        va="center",
    )
    plt.axis("off")

    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)

    buf.seek(0)
    return buf


def markdown_to_a4_pdf_page(markdown_text: str) -> bytes:
    """
    Convert markdown text into a single A4 PDF page
    with Markdown + LaTeX rendering.
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

    styles.add(ParagraphStyle(name="H1", fontSize=18, leading=22, spaceAfter=12))
    styles.add(ParagraphStyle(name="H2", fontSize=15, leading=18, spaceAfter=10))
    styles.add(ParagraphStyle(name="H3", fontSize=13, leading=16, spaceAfter=8))
    styles.add(ParagraphStyle(name="Body", fontSize=10.5, leading=14, spaceAfter=6))

    story = []
    lines = markdown_text.splitlines()
    bullet_buffer = []

    block_latex_pattern = re.compile(r"^\$\$(.+?)\$\$$")
    inline_latex_pattern = re.compile(r"\$(.+?)\$")

    def flush_bullets():
        nonlocal bullet_buffer
        if bullet_buffer:
            story.append(
                ListFlowable(
                    [
                        ListItem(Paragraph(item, styles["Body"]), bulletText="•")
                        for item in bullet_buffer
                    ],
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

        # ---------- BLOCK LATEX ----------
        block_match = block_latex_pattern.match(line)
        if block_match:
            flush_bullets()
            img_buf = _latex_to_image(block_match.group(1), fontsize=16)
            story.append(Image(img_buf, width=120 * mm, height=30 * mm))
            story.append(Spacer(1, 8))
            continue

        # ---------- HEADINGS ----------
        if line.startswith("### "):
            flush_bullets()
            story.append(Paragraph(line[4:], styles["H3"]))
        elif line.startswith("## "):
            flush_bullets()
            story.append(Paragraph(line[3:], styles["H2"]))
        elif line.startswith("# "):
            flush_bullets()
            story.append(Paragraph(line[2:], styles["H1"]))

        # ---------- BULLETS ----------
        elif line.startswith("- ") or line.startswith("* "):
            bullet_buffer.append(line[2:])

        # ---------- BODY WITH INLINE LATEX ----------
        else:
            flush_bullets()

            parts = []
            last = 0

            for m in inline_latex_pattern.finditer(line):
                if m.start() > last:
                    parts.append(
                        Paragraph(
                            line[last : m.start()]
                            .replace("&", "&amp;")
                            .replace("<", "&lt;")
                            .replace(">", "&gt;"),
                            styles["Body"],
                        )
                    )

                img_buf = _latex_to_image(m.group(1), fontsize=12)
                parts.append(Image(img_buf, width=40 * mm, height=12 * mm))
                last = m.end()

            if last < len(line):
                parts.append(
                    Paragraph(
                        line[last:]
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"),
                        styles["Body"],
                    )
                )

            for p in parts:
                story.append(p)

    flush_bullets()
    doc.build(story)

    buffer.seek(0)
    return buffer.read()









from markdown_pdf import MarkdownPdf, Section
from io import BytesIO


def markdown_to_pdf_bytes_IMPROVED(markdown_text: str) -> bytes:
    pdf = MarkdownPdf(toc_level=4, optimize=True)
    pdf.add_section(Section(markdown_text))
    out = BytesIO()
    pdf.save_bytes(out)
    out.seek(0)
    return out.read()

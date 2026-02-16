# A PDF Engine that allows you to do almost everything with pdfs.

### List of things that you can do with this project:
1. Upload Images, PDFs, PPTs as many as you want and convert or merge them to a single pdf.
2. Reorder, Rotate or Compress any page in the pdf.
3. Use models like PaddleOCR, GLM-OCR and Deepseek-OCR with ollama to convert images or handwritten PDFs to selectable (where you can select and copy text) PDFs.
4. Download the PDF file (and optionally compress it to whatever size it is possible to compress).

## Add this in the directory of this project to run this from anywhere, I haven't set it to be installed by uv because ... I always do that but it felt better when I wrote a bat file for the first time.

```bash
@echo off

REM Absolute path to project root
set PROJECT_ROOT=D:\path to pdf_engine

REM Go to project root ( /d allows drive change )
cd /d "%PROJECT_ROOT%"

REM Run the command
uv run streamlit run main.py
```
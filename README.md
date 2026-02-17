# A PDF Engine that allows you to do almost everything with pdfs.

### List of things that you can do with this project:
1. Upload Images, PDFs, PPTs as many as you want and convert or merge them to a single pdf.
2. Reorder, Rotate or Compress any page in the pdf.
3. Use models like PaddleOCR, GLM-OCR and Deepseek-OCR with ollama to convert images or handwritten PDFs to Searchable PDFs.
4. Download the PDF file (and optionally compress it to whatever size it is possible to compress).

## Requirements: Ensure [UV](https://github.com/astral-sh/uv) is installed on your PC

1. UV tool install method:
   ```bash
   uv tool install git+https://github.com/legit-os/PDF_Engine.git
   ```

2. Manually:
   ### First Clone the repo:

    ```bash
    git clone https://github.com/legit-os/PDF_Engine.git
    cd PDF_Engine
    ```
    ---
    For Windows :

    Run this script in terminal and clone it

    ```bash
    setx PATH "%cd%\scripts;%PATH%"
    ```
    Now reopen the terminal and run: 
    ```bash
    pdfui
    ```

    ---
    For Linux :

    ```bash
    echo 'export PATH="$PWD/scripts:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```
    Open new terminal and run:
    ```bash
    pdfui
    ```
    

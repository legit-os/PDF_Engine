# A PDF Engine that allows you to do almost everything with pdfs.

### List of things that you can do with this project:
1. Upload Images, PDFs, PPTs as many as you want and convert or merge them to a single pdf.
2. Reorder, Rotate or Compress any page in the pdf.
3. Use models like PaddleOCR, GLM-OCR and Deepseek-OCR with ollama to convert images or handwritten PDFs to Searchable PDFs.
4. You can split the pdf pages that are in "two page view" to "one page view".
5. Download the PDF file (and optionally compress it to whatever size it is possible to compress).

## Requirements: 
1. Ensure [UV](https://github.com/astral-sh/uv) is installed on your PC
2. Ensure you have docker engine since it is required by PaddleOCR
3. Poppler
   
   For Windows:
   ```PowerShell
   winget install -e --id oschwartz10612.Poppler
   ```
   For Linux:
   ```bash
   sudo apt-get update
   sudo apt-get install poppler-utils
   ```

## How to Use

3. UV tool install method: (recommended)
   ```bash
   uv tool install git+https://github.com/legit-os/PDF_Engine.git -U
   ```

4. Manually: (it may have problems)
   ### First Clone the repo:

    ```bash
    git clone https://github.com/legit-os/PDF_Engine.git
    cd PDF_Engine
    uv sync
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
    

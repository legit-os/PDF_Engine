@echo off

REM Absolute path to your project root
set PROJECT_ROOT=D:\path to pdf_engine

REM Go to project root ( /d allows drive change )
cd /d "%PROJECT_ROOT%"

REM Run your command
uv run streamlit run main.py


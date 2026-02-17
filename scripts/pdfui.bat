@echo off
setlocal

set SCRIPT_DIR=%~dp0

cd /c "%SCRIPT_DIR%\.."

uv run streamlit run main.py

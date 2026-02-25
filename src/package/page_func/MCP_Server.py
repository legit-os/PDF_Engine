import shutil

import streamlit as st
from pathlib import Path
import json

# Import your DB + text utilities
from package.mcp_server.db_maker import (
    create_engine_with_fts,
    initialize_database,
    upsert_chunk,
)
from package.utils.pdf_to_text import extract_text_from_pdf_bytes


st.set_page_config(layout="wide")
st.title("MCP Server Setup")

DB_PATH = Path(__file__).parent.parent / "mcp_chunks.db"

st.info(f"Database path: {DB_PATH.resolve()}")

import sys
import subprocess
from pathlib import Path
from typing import Optional

def find_root(package_name="src"):
    current_path = Path(__file__).resolve()
    root_path = None
    
    for parent in [current_path] + list(current_path.parents):
        if parent.name == package_name:
            root_path = parent
            break
            
    if not root_path:
        root_path = current_path.parent
    
    return str(root_path)


if st.button("Initialize MCP Server"):
    engine = create_engine_with_fts(str(DB_PATH))
    initialize_database(engine)

    st.success("MCP Database initialized successfully.")

    directory = Path(__file__).parent.parent.parent
    server_path = Path(__file__).parent.parent / "mcp_server" / "server.py"
    uv_path = shutil.which("uv")
    
    schema = {
        "mcpServers": {
            "local-pdf-rag": {
                "command": f"{uv_path}",
                "args": ["--directory",f"{find_root("pdf-engine")}",
                         f"{server_path}"]
            }
        }
    }

    st.subheader("Claude Desktop MCP Config")
    st.code(json.dumps(schema, indent=2), language="json")



import re

def extract_unique_words(
    text: str,
    min_length: int = 2,
    remove_stopwords: bool = False
) -> set[str]:
    if not text:
        return set()

    text = text.lower()

    text = re.sub(r"[^\w\s]", " ", text)

    tokens = text.split()

    STOPWORDS = {
        "the", "is", "a", "an", "of", "and", "or",
        "to", "in", "on", "at", "for", "by", "with"
    }

    unique_words = set()

    for token in tokens:
        if len(token) < min_length:
            continue

        if remove_stopwords and token in STOPWORDS:
            continue

        unique_words.add(token)

    return unique_words



if st.button("Update MCP Index From Session Pages (Add session pages to the mcp server)"):
    if "pages" not in st.session_state or not st.session_state["pages"]:
        st.warning("No pages found in session.")
        st.stop()

    engine = create_engine_with_fts(str(DB_PATH))
    initialize_database(engine)

    pages = st.session_state["pages"]

    progress = st.progress(0)
    total = len(pages)

    for i, page in enumerate(pages):
        text = extract_text_from_pdf_bytes(page["pdf_bytes"]).lower()

        if not text.strip():
            continue

        metadata = {
            "page_id": page["page_id"],
            "has_ocr": page.get("ocr_applied", False),
        }

        upsert_chunk(
            engine=engine,
            page_id=str(page["page_id"]),
            text=text,
            keywords=list(extract_unique_words(text=text,remove_stopwords=True)),
            metadata=metadata,
        )

        progress.progress((i + 1) / total, f"Processing page {i+1}")

    progress.empty()
    
    st.success("MCP Index updated successfully.")
    
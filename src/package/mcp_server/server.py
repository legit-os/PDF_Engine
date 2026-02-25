from pathlib import Path

from sqlalchemy import text
from package.mcp_server.db_maker import create_engine_with_fts
from package.mcp_server.retriever import retrieve_chunk_ids

from fastmcp import FastMCP

db_path = Path(__file__).parent.parent / "mcp_chunks.db"

engine = create_engine_with_fts(db_path=db_path)

server = FastMCP(name="PDF Engine Query tool",instructions="""
                 Use this to query from a pdf connected with the PDF Engine,
                 you can retreive similar texts, pdf pages as images and some information about the pdf metadata
                 to help user to talk with the pdf.
                 """)

import sqlite3


def get_chunks_by_ids(db_path: str, ids: list[str]):
    if not ids:
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    placeholders = ",".join(["?"] * len(ids))

    cursor.execute(f"""
        SELECT page_id, text, keywords, metadata
        FROM chunks
        WHERE page_id IN ({placeholders})
    """, ids)

    rows = cursor.fetchall()
    conn.close()

    row_map = {
        row[0]: {
            "page_id": row[0],
            "text": row[1],
            "keywords": row[2],
            "metadata": row[3],
        }
        for row in rows
    }

    ordered_results = [row_map[i] for i in ids if i in row_map]

    return [t["text"] for t in ordered_results]


@server.tool(description="""
             Use this tool to search for some query, this tool doesn't use embedding models
             so use keywords properly in you query.
             excludes : it will exclude the chunks that contain those strings
             jaro_similarity : if not None, expects the jaro similarity threshold, it will correct the given query and replace some words to match with words present in the pdf
             """)
def similarity_retriever_tool(
    query: str,
    jaro_similarity: float | None = None,
    top_k: int = 10,
):
    global engine
    global db_path
    chunk_ids = retrieve_chunk_ids(db_path,query,jaro_similarity,top_k)
    chunks = get_chunks_by_ids(db_path,ids=[i["id"] for i in chunk_ids])
    return {i:{"text":k,"score":v["score"]} for i,(k,v) in enumerate(zip(chunks,chunk_ids)) } # enjoyed writing this




@server.tool(description="Check the number of pages")
def get_page_count():
    global engine
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM chunks"))
        return result.scalar_one()





if __name__ == "__main__":
    server.run(transport="stdio")
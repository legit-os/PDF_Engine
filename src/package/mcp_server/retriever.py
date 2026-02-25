import sqlite3
import re
import jellyfish


def build_vocabulary(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_vocab
        USING fts5vocab(chunks_fts, 'row');
    """)

    cursor.execute("SELECT term FROM chunks_vocab;")
    vocab = {row[0] for row in cursor.fetchall()}

    conn.close()
    return vocab


def clean_query(query: str) -> str:
    query = query.lower()
    query = re.sub(r'["\-\+\:\(\)\*]', " ", query)
    query = re.sub(r"\s+", " ", query)
    return query.strip()


def correct_query_jaro(query: str, vocabulary: set[str], threshold: float = 0.88):
    corrected_tokens = []

    for token in query.lower().split():

        if token in vocabulary:
            corrected_tokens.append(token)
            continue

        best_match = token
        best_score = 0.0

        for word in vocabulary:
            if abs(len(word) - len(token)) > 2:
                continue

            score = jellyfish.jaro_winkler_similarity(token, word)

            if score > best_score:
                best_score = score
                best_match = word

        if best_score >= threshold:
            corrected_tokens.append(best_match)
        else:
            corrected_tokens.append(token)

    return " ".join(corrected_tokens)


def retrieve_chunk_ids(
    db_path: str,
    query: str,
    jaro_similarity: float | None = None,
    top_k: int = 10
):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = clean_query(query)

    if jaro_similarity is not None:
        vocabulary = build_vocabulary(db_path)
        query = correct_query_jaro(query, vocabulary, jaro_similarity)

    cursor.execute("""
        SELECT chunks.page_id,
               bm25(chunks_fts) AS score
        FROM chunks_fts
        JOIN chunks ON chunks_fts.rowid = chunks.rowid
        WHERE chunks_fts MATCH ?
        ORDER BY score
        LIMIT ?
    """, (query, top_k))

    return_values = [{"id": row[0], "score": row[1]} for row in cursor.fetchall()]

    conn.close()
    return return_values
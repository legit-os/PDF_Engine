# all these functions are writtn by gpt, I didn't new how to setup the fts and usse bm25 in that, also i am using
# sqlite because storing large pdfs and running similarities takes memory and compute both, also I had to add some 
# more filters like jaro that are not in llama and langchain.





from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base
import sqlite3

Base = declarative_base()

def create_engine_with_fts(db_path: str):
    engine = create_engine(f"sqlite:///{db_path}", future=True)

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("PRAGMA temp_store=MEMORY;")
        cursor.close()

    return engine

from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime
import json

class Chunk(Base):
    __tablename__ = "chunks"

    page_id = Column(String, primary_key=True)
    text = Column(Text, nullable=False)
    keywords = Column(Text)
    meta_json = Column("metadata",Text)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
from sqlalchemy import text

def initialize_database(engine):
    with engine.begin() as conn:
        # Create main table
        Base.metadata.create_all(conn)

        # Create FTS5 virtual table linked to chunks
        conn.execute(text("""
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
            USING fts5(
                text,
                content='chunks',
                content_rowid='rowid'
            );
        """))

        # Trigger: insert
        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, text)
                VALUES (new.rowid, new.text);
            END;
        """))

        # Trigger: delete
        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, text)
                VALUES('delete', old.rowid, old.text);
            END;
        """))

        # Trigger: update
        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, text)
                VALUES('delete', old.rowid, old.text);
                INSERT INTO chunks_fts(rowid, text)
                VALUES (new.rowid, new.text);
            END;
        """))
        
from sqlalchemy.orm import sessionmaker

def upsert_chunk(engine, page_id, text, keywords=None, metadata=None):
    Session = sessionmaker(bind=engine)
    session = Session()

    chunk = session.get(Chunk, page_id)

    if chunk:
        chunk.text = text
        chunk.keywords = json.dumps(keywords or [])
        chunk.meta_json = json.dumps(metadata or {})
    else:
        chunk = Chunk(
            page_id=page_id,
            text=text,
            keywords=json.dumps(keywords or []),
            meta_json=json.dumps(metadata or {})
        )
        session.add(chunk)

    session.commit()
    session.close()
    

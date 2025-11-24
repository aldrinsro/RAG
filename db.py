import os
import psycopg2
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    # Forcer l'encodage UTF-8 pour éviter les problèmes avec les caractères accentués
    import sys
    if sys.platform == 'win32':
        import locale
        locale.setlocale(locale.LC_ALL, 'C')
    
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5433"),
        dbname=os.getenv("PG_DB", "ragdb"),
        user=os.getenv("PG_USER", "raguser"),
        password=os.getenv("PG_PASSWORD", "ragpass"),
        options='-c client_encoding=UTF8'
    )
    register_vector(conn)
    return conn
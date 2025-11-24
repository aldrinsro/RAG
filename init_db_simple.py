"""
Script simplifié d'initialisation - sans dotenv pour éviter les problèmes d'encodage
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Credentials hardcodés
HOST = "localhost"
PORT = 5433
USER = "raguser"
PASSWORD = "ragpass"
DB = "ragdb"

print("Initialisation de la base de données...")
print(f"Connexion à PostgreSQL sur {HOST}:{PORT}")

try:
    # Connexion initiale à postgres
    conn = psycopg2.connect(
        f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname=postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    with conn.cursor() as cur:
        # Vérifier si la base existe
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Création de la base de données {DB}...")
            cur.execute(f"CREATE DATABASE {DB}")
        else:
            print(f"Base de données {DB} existe déjà")
    
    conn.close()
except Exception as e:
    print(f"Note: {e}")
    print("Continuons...")

# Connexion à la base ragdb
print(f"Configuration de la base {DB}...")
conn = psycopg2.connect(
    f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname={DB}"
)

with conn.cursor() as cur:
    # Extension pgvector
    print("Activation de l'extension pgvector...")
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    
    # Table documents
    print("Création de la table documents...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            source TEXT NOT NULL,
            chunk TEXT NOT NULL,
            modality TEXT NOT NULL,
            embedding vector(1536),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    
    # Index vectoriel
    print("Création de l'index vectoriel...")
    cur.execute("""
        CREATE INDEX IF NOT EXISTS documents_embedding_idx 
        ON documents USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)
    conn.commit()

conn.close()
print("Initialisation terminée avec succès!")

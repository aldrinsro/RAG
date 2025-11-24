"""
Script d'initialisation de la base de données PostgreSQL avec pgvector
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import locale

# Forcer l'encodage UTF-8 pour éviter les problèmes avec les caractères accentués
if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, 'C')

# Charger manuellement les variables d'environnement
PG_HOST = "localhost"
PG_PORT = 5433
PG_USER = "raguser"
PG_PASSWORD = "ragpass"
PG_DB = "ragdb"

def init_database():
    # Connexion à PostgreSQL (sans spécifier de base de données)
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
            dbname="postgres",
            options='-c client_encoding=UTF8'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        with conn.cursor() as cur:
            # Vérifier si la base existe
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{PG_DB}'")
            exists = cur.fetchone()
            
            if not exists:
                print(f"Création de la base de données {PG_DB}...")
                cur.execute(f"CREATE DATABASE {PG_DB}")
                print("✓ Base de données créée")
            else:
                print(f"✓ Base de données {PG_DB} existe déjà")
        
        conn.close()
    except Exception as e:
        print(f"Note: {e}")
        print("La base de données existe probablement déjà, continuons...")

    # Connexion à la base de données spécifique
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        dbname=PG_DB,
        options='-c client_encoding=UTF8'
    )
    
    with conn.cursor() as cur:
        # Activer l'extension pgvector
        print("Activation de l'extension pgvector...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.commit()
        print("✓ Extension pgvector activée")
        
        # Créer la table documents
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
        print("✓ Table documents créée")
        
        # Créer un index pour accélérer les recherches vectorielles
        print("Création de l'index vectoriel...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS documents_embedding_idx 
            ON documents USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        """)
        conn.commit()
        print("✓ Index vectoriel créé")
    
    conn.close()
    print("\n✅ Initialisation de la base de données terminée avec succès!")

if __name__ == "__main__":
    init_database()

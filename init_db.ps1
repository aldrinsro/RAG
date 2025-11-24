# Script PowerShell pour initialiser la base via Docker
Write-Host "Initialisation de la base de données via Docker..." -ForegroundColor Cyan

# Créer la base de données
Write-Host "Création de la base de données ragdb..." -ForegroundColor Green
docker exec pgvector_rag psql -U raguser -d postgres -c "CREATE DATABASE ragdb;" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Base de données existe déjà" -ForegroundColor Yellow
}

# Activer l'extension pgvector
Write-Host "Activation de l'extension pgvector..." -ForegroundColor Green
docker exec pgvector_rag psql -U raguser -d ragdb -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Créer la table documents
Write-Host "Création de la table documents..." -ForegroundColor Green
docker exec pgvector_rag psql -U raguser -d ragdb -c "CREATE TABLE IF NOT EXISTS documents (id SERIAL PRIMARY KEY, source TEXT NOT NULL, chunk TEXT NOT NULL, modality TEXT NOT NULL, embedding vector(1536), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"

# Créer l'index vectoriel
Write-Host "Création de l'index vectoriel..." -ForegroundColor Green
docker exec pgvector_rag psql -U raguser -d ragdb -c "CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);"

Write-Host "Initialisation terminée avec succès!" -ForegroundColor Green

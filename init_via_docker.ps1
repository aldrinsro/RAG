Write-Host "Initialisation de la base de donnees via Docker..." -ForegroundColor Cyan

Write-Host "Creation de la base de donnees ragdb..." -ForegroundColor Green
docker exec pgvector_rag psql -U raguser -d postgres -c "CREATE DATABASE ragdb;" 2>$null

Write-Host "Activation de l'extension pgvector..." -ForegroundColor Green
docker exec pgvector_rag psql -U raguser -d ragdb -c "CREATE EXTENSION IF NOT EXISTS vector;"

Write-Host "Creation de la table documents..." -ForegroundColor Green
docker exec pgvector_rag psql -U raguser -d ragdb -c "CREATE TABLE IF NOT EXISTS documents (id SERIAL PRIMARY KEY, source TEXT NOT NULL, chunk TEXT NOT NULL, modality TEXT NOT NULL, embedding vector(1536), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"

Write-Host "Creation de l'index vectoriel..." -ForegroundColor Green
docker exec pgvector_rag psql -U raguser -d ragdb -c "CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);"

Write-Host "Initialisation terminee avec succes!" -ForegroundColor Green

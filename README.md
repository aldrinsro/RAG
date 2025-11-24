# 📝 README - Projet RAG Multimodal

Un système RAG (Retrieval-Augmented Generation) multimodal utilisant OpenAI et PostgreSQL avec pgvector.

## 🎯 Fonctionnalités

- ✅ Ingestion de documents PDF et images
- ✅ Recherche vectorielle avec pgvector
- ✅ Génération de réponses contextuelles avec GPT-5
- ✅ Support multimodal (texte + images)
- ✅ Interface web avec Streamlit

## 🚀 Démarrage Rapide

```powershell
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Démarrer PostgreSQL
docker-compose up -d

# 3. Initialiser la base de données
python init_db.py

# 4. Ingérer vos documents (placez-les dans data/)
python ingest.py

# 5. Lancer l'application
streamlit run app.py
```

## 📚 Documentation

Consultez le [**Guide de Démarrage Complet**](GUIDE_DEMARRAGE.md) pour des instructions détaillées.

## 🛠️ Technologies

- **Python 3.8+**
- **OpenAI API** (embeddings + GPT)
- **PostgreSQL + pgvector**
- **Streamlit**
- **Docker**

## 📄 Licence

Projet personnel - Libre d'utilisation

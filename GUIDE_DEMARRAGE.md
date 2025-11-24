# 🚀 Guide de Démarrage - Projet RAG Multimodal

Ce guide vous accompagne pas à pas pour lancer votre système RAG (Retrieval-Augmented Generation) multimodal avec OpenAI et pgvector.

## 📋 Table des Matières
1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Initialisation de la Base de Données](#initialisation-de-la-base-de-données)
5. [Ingestion des Données](#ingestion-des-données)
6. [Lancement de l'Application](#lancement-de-lapplication)
7. [Utilisation](#utilisation)
8. [Résolution des Problèmes](#résolution-des-problèmes)

---

## 🔧 Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Python 3.8+** installé
- **Docker Desktop** installé et en cours d'exécution
- **Une clé API OpenAI** (disponible sur [platform.openai.com](https://platform.openai.com))
- **Git** (optionnel, pour le versioning)

---

## 📦 Installation

### Étape 1 : Installer les dépendances Python

Ouvrez PowerShell dans le dossier du projet et exécutez :

```powershell
# Créer un environnement virtuel (si ce n'est pas déjà fait)
python -m venv env

# Activer l'environnement virtuel
.\env\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

> **Note** : Si vous rencontrez une erreur de politique d'exécution, exécutez :
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## ⚙️ Configuration

### Étape 2 : Vérifier le fichier `.env`

Le fichier `.env` contient vos variables d'environnement. Vérifiez qu'il contient :

```env
OPENAI_API_KEY=votre_clé_api_openai
PG_HOST=localhost
PG_PORT=5432
PG_USER=raguser
PG_PASSWORD=ragpass
PG_DB=ragdb
```

> ⚠️ **IMPORTANT** : Remplacez `votre_clé_api_openai` par votre vraie clé API OpenAI si ce n'est pas déjà fait.

---

## 🗄️ Initialisation de la Base de Données

### Étape 3 : Démarrer PostgreSQL avec Docker

```powershell
# Démarrer le conteneur PostgreSQL avec pgvector
docker-compose up -d

# Vérifier que le conteneur fonctionne
docker ps
```

Vous devriez voir un conteneur nommé `pgvector_rag` en cours d'exécution.

### Étape 4 : Initialiser la base de données

```powershell
# Exécuter le script d'initialisation
python init_db.py
```

Ce script va :
- ✅ Créer la base de données `ragdb`
- ✅ Activer l'extension `pgvector`
- ✅ Créer la table `documents` avec support des vecteurs
- ✅ Créer un index vectoriel pour accélérer les recherches

---

## 📄 Ingestion des Données

### Étape 5 : Préparer vos documents

Placez vos fichiers dans le dossier `data/` :
- **PDFs** : `*.pdf`
- **Images** : `*.png`, `*.jpg`

Un fichier exemple `guide_rag.pdf` a déjà été créé pour vous.

### Étape 6 : Lancer l'ingestion

```powershell
# Ingérer les documents dans la base vectorielle
python ingest.py
```

Ce script va :
1. 📖 Extraire le texte des PDFs
2. ✂️ Découper le texte en chunks de 800 caractères
3. 🖼️ Générer des descriptions pour les images (via GPT-4o-mini)
4. 🧮 Créer des embeddings vectoriels (via text-embedding-3-small)
5. 💾 Stocker tout dans PostgreSQL avec pgvector

> **Note** : L'ingestion peut prendre quelques minutes selon le nombre de fichiers et votre connexion à l'API OpenAI.

---

## 🎯 Lancement de l'Application

### Étape 7 : Démarrer l'interface Streamlit

```powershell
# Lancer l'application web
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse :
```
http://localhost:8501
```

---

## 💡 Utilisation

### Interface Streamlit

1. **Posez une question** dans le champ de texte
2. **Cliquez sur "Rechercher & Répondre"**
3. **Consultez la réponse** générée par le modèle
4. **Explorez les sources** utilisées (top-5 chunks les plus pertinents)

### Exemple de questions

- "Qu'est-ce que le RAG ?"
- "Quels sont les avantages du RAG ?"
- "Comment fonctionne l'architecture RAG ?"

---

## 🔍 Architecture du Projet

```
RAG/
├── app.py                 # Interface Streamlit
├── rag_core.py           # Logique de recherche et génération
├── ingest.py             # Script d'ingestion des documents
├── openai_utils.py       # Utilitaires OpenAI (embeddings, captions)
├── db.py                 # Connexion PostgreSQL
├── init_db.py            # Initialisation de la base de données
├── docker-compose.yml    # Configuration PostgreSQL + pgvector
├── requirements.txt      # Dépendances Python
├── .env                  # Variables d'environnement
└── data/                 # Dossier pour vos documents
    └── guide_rag.pdf     # Exemple de document
```

---

## 🛠️ Résolution des Problèmes

### Problème : Docker ne démarre pas

**Solution** :
- Vérifiez que Docker Desktop est bien lancé
- Redémarrez Docker Desktop
- Vérifiez que le port 5432 n'est pas déjà utilisé

### Problème : Erreur de connexion à PostgreSQL

**Solution** :
```powershell
# Redémarrer le conteneur
docker-compose down
docker-compose up -d

# Attendre quelques secondes puis réessayer
python init_db.py
```

### Problème : Erreur API OpenAI (401 Unauthorized)

**Solution** :
- Vérifiez que votre clé API dans `.env` est correcte
- Vérifiez que votre compte OpenAI a du crédit disponible
- Testez votre clé sur [platform.openai.com](https://platform.openai.com)

### Problème : Aucun résultat lors de la recherche

**Solution** :
- Vérifiez que vous avez bien exécuté `python ingest.py`
- Vérifiez que des fichiers sont présents dans le dossier `data/`
- Consultez les logs pour voir si l'ingestion s'est bien passée

### Problème : L'application Streamlit ne se lance pas

**Solution** :
```powershell
# Vérifier que streamlit est installé
pip install streamlit --upgrade

# Relancer l'application
streamlit run app.py
```

---

## 📊 Commandes Utiles

### Gestion de Docker

```powershell
# Voir les logs du conteneur PostgreSQL
docker logs pgvector_rag

# Arrêter le conteneur
docker-compose down

# Redémarrer le conteneur
docker-compose restart

# Supprimer complètement le conteneur et les données
docker-compose down -v
```

### Gestion de la Base de Données

```powershell
# Se connecter à PostgreSQL
docker exec -it pgvector_rag psql -U raguser -d ragdb

# Compter le nombre de documents ingérés
# (dans psql) SELECT COUNT(*) FROM documents;

# Voir les modalités des documents
# (dans psql) SELECT modality, COUNT(*) FROM documents GROUP BY modality;

# Quitter psql
# \q
```

---

## 🎓 Concepts Clés

### Qu'est-ce qu'un RAG ?

Le **RAG (Retrieval-Augmented Generation)** combine :
1. **Recherche** : Trouver les documents pertinents dans une base vectorielle
2. **Génération** : Utiliser un LLM pour générer une réponse basée sur ces documents

### Pourquoi pgvector ?

**pgvector** est une extension PostgreSQL qui permet de :
- Stocker des vecteurs d'embeddings
- Effectuer des recherches par similarité cosinus ultra-rapides
- Bénéficier de la robustesse de PostgreSQL

### Modèles OpenAI utilisés

- **text-embedding-3-small** : Génération d'embeddings (1536 dimensions)
- **gpt-3.5-turbo** : Génération de réponses textuelles
- **gpt-4o-mini** : Génération de descriptions d'images (vision)

---

## 🚀 Prochaines Étapes

Maintenant que votre système RAG fonctionne, vous pouvez :

1. **Ajouter vos propres documents** dans le dossier `data/`
2. **Réexécuter l'ingestion** avec `python ingest.py`
3. **Personnaliser les prompts** dans `rag_core.py`
4. **Ajuster les paramètres** (taille des chunks, nombre de résultats, etc.)
5. **Améliorer l'interface** Streamlit selon vos besoins

---

##  Support

Si vous rencontrez des problèmes :
1. Consultez la section [Résolution des Problèmes](#résolution-des-problèmes)
2. Vérifiez les logs de l'application
3. Consultez la documentation officielle :
   - [OpenAI API](https://platform.openai.com/docs)
   - [pgvector](https://github.com/pgvector/pgvector)
   - [Streamlit](https://docs.streamlit.io)

---

**Bon développement ! 🎉**

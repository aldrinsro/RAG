import streamlit as st
from rag_core import answer
from ingest import chunck_text, ingest_pdf, save_chunk
from openai_utils import embed_text, caption_image
from db import get_conn
import os
import tempfile
from PIL import Image

st.set_page_config(page_title="RAG Multimodal Assistant", layout="wide")

# Sidebar pour l'upload de fichiers
with st.sidebar:
    st.header("📁 Gestion des Documents")
    
    # Upload de fichiers
    uploaded_files = st.file_uploader(
        "Importer des documents",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Importez des PDFs ou des images pour enrichir la base de connaissances"
    )
    
    if uploaded_files and st.button("🚀 Ingérer les fichiers", type="primary"):
        conn = get_conn()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_files = len(uploaded_files)
        
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Traitement de {uploaded_file.name}...")
            
            # Sauvegarder temporairement le fichier
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                if uploaded_file.type == "application/pdf":
                    # Traiter le PDF
                    full_text = ingest_pdf(tmp_path)
                    chunks = chunck_text(full_text)
                    
                    for chunk in chunks:
                        emb = embed_text(chunk)
                        save_chunk(conn, uploaded_file.name, chunk, "text", emb)
                    
                    st.success(f"✅ {uploaded_file.name} : {len(chunks)} chunks ingérés")
                
                elif uploaded_file.type.startswith("image/"):
                    # Traiter l'image
                    caption = caption_image(tmp_path)
                    emb = embed_text(caption)
                    save_chunk(conn, uploaded_file.name, caption, "image", emb)
                    
                    st.success(f"✅ {uploaded_file.name} : image ingérée")
            
            except Exception as e:
                st.error(f"❌ Erreur avec {uploaded_file.name}: {str(e)}")
            
            finally:
                # Supprimer le fichier temporaire
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            
            progress_bar.progress((idx + 1) / total_files)
        
        conn.close()
        status_text.text("✅ Ingestion terminée !")
        st.balloons()
    
    st.divider()
    st.caption("💡 Astuce : Vous pouvez aussi ajouter des fichiers dans le dossier `data/` et exécuter `python ingest.py`")

# Interface principale
st.title("🤖 RAG Multimodal Assistant")
st.markdown("Posez une question sur le corpus indexé (textes + images)")

# Zone de recherche
query = st.text_input("❓ Votre question :", placeholder="Ex: Qu'est-ce que le RAG ?")

col1, col2 = st.columns([1, 4])
with col1:
    k_results = st.selectbox("Nombre de sources", [3, 5, 10,20], index=1)

if st.button("🔍 Rechercher & Répondre", type="primary") and query:
    with st.spinner("Recherche en cours..."):
        try:
            resp, rows = answer(query, k=k_results)
            
            # Afficher la réponse
            st.subheader("💬 Réponse :")
            st.markdown(f"**{resp}**")
            
            # Afficher les sources
            st.subheader(f"📚 Sources utilisées (top-{k_results}) :")
            
            for idx, (src, chunk, modality, score) in enumerate(rows, 1):
                with st.expander(f"#{idx} - {src} | {modality.upper()} | Score: {score:.4f}"):
                    if modality == "image":
                        st.markdown("**Description de l'image :**")
                        st.write(chunk)
                    else:
                        st.markdown("**Extrait du texte :**")
                        st.text(chunk[:500] + "..." if len(chunk) > 500 else chunk)
        
        except Exception as e:
            st.error(f"❌ Erreur lors de la recherche : {str(e)}")

# Footer
st.divider()
st.caption("🔧 Powered by OpenAI + pgvector | RAG Multimodal System")

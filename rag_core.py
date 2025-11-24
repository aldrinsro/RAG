from db import get_conn 
from openai_utils import embed_text
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def retrieve(query: str, k=5):
    q_emb = embed_text(query)
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
                """
                SELECT source, chunk, modality,
                1 - (embedding <-> %s::vector) AS score
                FROM documents
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (q_emb, q_emb, k)
        )
        rows = cur.fetchall()
    conn.close()
    return rows

def answer(query: str, k=5):
    rows = retrieve(query, k=k)
    context = "\n\n".join([f"[{m}] {c}" for _, c, m, _ in rows])

    prompt = f""" 

Tu es un assistant RAG multimodal.
Utilise STRICTEMENT le contexte pour répondre 

Contexte : 
{context}

Question :
{query}


"""
    
    resp = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "Tu es un assistant RAG multimodal. Réponds uniquement en te basant sur le contexte fourni."},
            {"role": "user", "content": prompt}
        ]
    )
    return resp.choices[0].message.content, rows
import os, glob
from pypdf import PdfReader
import tqdm
from openai_utils import embed_text, caption_image
from db import get_conn


CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

def chunck_text(text: str):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+CHUNK_SIZE])
        i += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def ingest_pdf(path: str):
    reader = PdfReader(path)
    full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return full_text

def ingest_images(paths: list[str]):
    image_chunks = []
    for p in paths:
        cap = caption_image(p)
        image_chunks.append((p, cap))
    return image_chunks


def save_chunk(conn, source, chunk, modality, emb):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO documents (source, chunk, modality, embedding)
            VALUES (%s, %s, %s, %s)
            """,
            (source, chunk, modality, emb)
        )
        conn.commit()

def main(data_dir="data"):
    conn = get_conn()

    pdfs = glob.glob(os.path.join(data_dir, "*.pdf"))
    imgs = glob.glob(os.path.join(data_dir, "*.png")) + glob.glob(os.path.join(data_dir, "*.jpg"))

    # PDFs -> texte 
    for pdf in tqdm.tqdm(pdfs, desc="PDF ingestion"):
        full_text = ingest_pdf(pdf)
        chunks = chunck_text(full_text)
        for c in chunks:
            emb = embed_text(c)
            save_chunk(conn, pdf, c, "text", emb)

    # Images -> caption -> embedding
    image_data = ingest_images(imgs)
    for img_path, cap in tqdm.tqdm(image_data, desc="Image ingestion"):
        emb = embed_text(cap)
        save_chunk(conn, img_path, cap, "image", emb)

    conn.close()
    print("Ingestion Terminée.")

if __name__ == "__main__":
    main()
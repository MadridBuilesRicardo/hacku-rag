from celery import Celery
from bs4 import BeautifulSoup
import requests
import os
import re
from core.ingest import load_and_split_documents
from core.embed_store import create_chroma_retriever

app = Celery(
    "scraper_task",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

def limpiar_texto(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", text)

@app.task
def scrapear_y_guardar(cliente: str, urls: list):
    carpeta_docs = os.path.join("clientes", cliente.lower(), "docs")
    os.makedirs(carpeta_docs, exist_ok=True)

    for i, url in enumerate(urls):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            texto = limpiar_texto(response.text)

            path_archivo = os.path.join(carpeta_docs, f"scrap_{i+1}.txt")
            with open(path_archivo, "w", encoding="utf-8") as f:
                f.write(texto)
            print(f"✅ Guardado: {path_archivo}")

        except Exception as e:
            print(f"❌ Error en {url}: {e}")

    # Ingestar documentos una vez finalice el scraping
    try:
        from core.ingest import load_and_split_documents
        from core.embed_store import create_chroma_retriever
        
        documentos = load_and_split_documents(carpeta_docs, use_hash=True)
        persist_path = os.path.join("clientes", cliente.lower(), "chroma_db")
        retriever = create_chroma_retriever(documentos, persist_directory=persist_path, use_hash=True)
        print(f"🧠 Ingesta completa para {cliente}")
    except Exception as e:
        print(f"❌ Error al vectorizar los documentos: {e}")

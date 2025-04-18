import os
import requests
from bs4 import BeautifulSoup
from core.normalize_scraped_txt import clean_scraped_text
from core.embed_store import create_chroma_retriever
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import SentenceTransformersTextSplitter


def scrape_and_vectorize(url: str, output_path: str, persist_path: str):
    try:
        # 🌐 Paso 1: Scraping básico
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        raw_text = soup.get_text(separator=" ")

        # 🧼 Paso 2: Normalización
        normalized_text = clean_scraped_text(raw_text)

        # 💾 Paso 3: Guardar .txt limpio
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(normalized_text)
        print(f"✅ Guardado normalizado en: {output_path}")

        # 🧠 Paso 4: Vectorización con splitter optimizado
        loader = TextLoader(output_path, encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = output_path

        text_splitter = SentenceTransformersTextSplitter(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            chunk_size=800,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(docs)

        _ = create_chroma_retriever(
            chunks,
            persist_directory=persist_path,
            use_hash=True
        )

        print(f"🧠 Vector store actualizado en: {persist_path}")

    except Exception as e:
        print(f"❌ Error en proceso con {url}: {e}")


if __name__ == "__main__":
    cliente = "recetron"
    urls = [
        "https://vexia.com.co",
        # puedes agregar más URLs si deseas
    ]

    docs_folder = f"clientes/{cliente}/docs"
    persist_folder = f"clientes/{cliente}/chroma_db"
    os.makedirs(docs_folder, exist_ok=True)

    for i, url in enumerate(urls):
        output_file = os.path.join(docs_folder, f"scrap_{i + 1}.txt")
        scrape_and_vectorize(url, output_file, persist_folder)

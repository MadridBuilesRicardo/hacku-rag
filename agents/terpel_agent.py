import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.ingest import load_and_split_documents
from core.embed_store import create_chroma_retriever
from core.query_engine import build_qa_chain, answer_question

# Configurar la API Key
os.environ["OPENAI_API_KEY"] = "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"

def run_terpel_agent():
    # Paso 1: Ingestar y chunkear el documento
    documents = load_and_split_documents("docs/ejemplo.txt")

    # Paso 2: Crear el vector store y retriever
    retriever = create_chroma_retriever(documents, persist_directory="chroma_db")

    # Paso 3: Crear el RAG chain con el LLM
    qa_chain = build_qa_chain(retriever)

    # Paso 4: Ejecutar una consulta
    pregunta = "¿Qué productos ofrece Terpel?"
    respuesta, fuentes = answer_question(qa_chain, pregunta)

    print("\n📌 Respuesta:")
    print(respuesta)

    print("\n📚 Fuentes:")
    for doc in fuentes:
        print("-", doc.metadata.get("source", "sin nombre"))

if __name__ == "__main__":
    run_terpel_agent()

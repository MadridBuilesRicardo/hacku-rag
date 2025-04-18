import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

# 🧠 Desactivar advertencias de tokenizers que aparecen en Mac/Linux
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def create_chroma_retriever(documents, persist_directory):
    """
    Crea el vector store con OpenAIEmbeddings y devuelve un retriever configurado.
    Usa ChromaDB como almacenamiento y recuperación local persistente.
    """

    # 🧠 Embeddings con OpenAI
    embedding_function = OpenAIEmbeddings()

    # 💾 Vector store con persistencia
    vectordb = Chroma.from_documents(
        documents,
        embedding=embedding_function,
        persist_directory=persist_directory
    )

    # 🔍 Retriever con k=2 para mejor rendimiento y foco
    retriever = vectordb.as_retriever(search_kwargs={"k": 2})
    return retriever

import os
import hashlib
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain.schema.document import Document

def hash_file(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def clean_pdf_text(pages):
    """
    Limpia espacios innecesarios y saltos de línea de cada página del PDF.
    """
    cleaned = []
    for page in pages:
        cleaned_text = " ".join(page.page_content.split())
        cleaned.append(Document(page_content=cleaned_text, metadata=page.metadata))
    return cleaned

def load_and_split_documents(folder_path, use_hash=False):
    documents = []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".txt":
            loader = TextLoader(filepath, encoding="utf-8")
            docs = loader.load()
        elif ext == ".pdf":
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            docs = clean_pdf_text(docs)  # ✅ limpieza de PDF
        elif ext == ".docx":
            loader = Docx2txtLoader(filepath)
            docs = loader.load()
        else:
            continue

        if use_hash:
            file_hash = hash_file(filepath)
            for doc in docs:
                doc.metadata["source"] = f"{filename}#{file_hash}"
        else:
            for doc in docs:
                doc.metadata["source"] = filename

        documents.extend(docs)

    splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=50,
        tokens_per_chunk=300  # ✅ dentro del límite del modelo all-mpnet-base-v2
    )

    return splitter.split_documents(documents)

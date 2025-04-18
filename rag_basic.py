from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

# 1. Configura tu API Key de OpenAI
os.environ["OPENAI_API_KEY"] = "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"

# 2. Carga documento
loader = TextLoader("docs/ejemplo.txt", encoding='utf-8')
documents = loader.load()

# 3. Chunking del texto
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 4. Embeddings
embeddings = OpenAIEmbeddings()

# 5. Crear o cargar VectorStore
db = Chroma.from_documents(docs, embeddings, persist_directory="chroma_db")
db.persist()

# 6. Crear retriever
retriever = db.as_retriever()

# 7. Instanciar LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# 8. Crear el chain de RAG
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# 9. Pregunta de prueba
query = "¿Qué es Terpel?"
result = qa_chain({"query": query})

# 10. Mostrar respuesta
print("\n📌 Respuesta generada:")
print(result["result"])

print("\n📚 Fuente:")
for doc in result["source_documents"]:
    print("-", doc.metadata.get("source", "Sin nombre"))

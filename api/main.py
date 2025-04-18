import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.ingest import load_and_split_documents
from core.embed_store import create_chroma_retriever
from core.query_engine import build_qa_chain, answer_question

# 🔁 Cargar clientes dinámicamente desde carpetas
def cargar_clientes_dinamicamente(base_path="clientes"):
    clientes = {}
    for cliente in os.listdir(base_path):
        cliente_path = os.path.join(base_path, cliente)
        docs_path = os.path.join(cliente_path, "docs")

        if os.path.isdir(docs_path):
            archivos_validos = [
                f for f in os.listdir(docs_path)
                if f.endswith((".txt", ".pdf", ".docx"))
            ]
            if archivos_validos:
                clientes[cliente.lower()] = {
                    "docs_path": docs_path,
                    "persist_path": os.path.join(cliente_path, "chroma_db"),
                    "system_instruction_path": os.path.join(docs_path, "system_instruction.txt")
                }

    print(f"🔍 Clientes detectados dinámicamente: {list(clientes.keys())}")  # DEBUG
    return clientes

# 🚀 Inicializar FastAPI
app = FastAPI(title="API RAG Multiagente - hackÜ")

# 🌐 Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Ajustar para producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📥 Modelo de entrada
class QueryInput(BaseModel):
    cliente: str
    pregunta: str

# 📮 Endpoint principal
@app.post("/query")
def query_cliente(input: QueryInput):
    cliente = input.cliente.lower()
    clientes_actualizados = cargar_clientes_dinamicamente()

    if cliente not in clientes_actualizados:
        return {"error": f"Cliente '{cliente}' no está registrado."}

    config = clientes_actualizados[cliente]
    docs_path = config["docs_path"]
    persist_path = config["persist_path"]
    system_instruction_path = config.get("system_instruction_path")

    try:
        documentos = load_and_split_documents(docs_path, use_hash=True)
        retriever = create_chroma_retriever(documentos, persist_directory=persist_path)
        chain = build_qa_chain(
            retriever,
            system_instruction_path=system_instruction_path
        )

        print("✅ QA Chain ready. Prompt espera:", chain.combine_documents_chain.llm_chain.prompt.input_variables)

        result, sources = answer_question(chain, input.pregunta)

        return {
            "cliente": cliente,
            "respuesta": result,
            "fuentes": [doc.metadata.get("source", "sin fuente") for doc in sources]
        }

    except Exception as e:
        return {"error": str(e)}

# 🧠 RAG Multiagente - hackÜ

Este repositorio contiene la API REST de un sistema RAG (Retrieval-Augmented Generation) con agentes personalizados por cliente. Cada agente responde preguntas basándose exclusivamente en sus propios documentos. Está diseñado para integrarse fácilmente con frontends como WhatsApp, Slack, Web o App.

---

## 🚀 Cómo levantar el proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/hacku-team/hacku-rag.git
cd hacku-rag
2. Crea un entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows

3. Instala las dependencias
pip install -r requirements.txt

4. Configura tus claves de API
Crea un archivo .env en la raíz con el siguiente contenido:

OPENAI_API_KEY=tu-clave-openai
⚠️ Este archivo no debe ser versionado (ya está en el .gitignore).

5. Corre el servidor local
uvicorn api.main:app --reload --port 8001
Abre tu navegador en: http://localhost:8001/docs

📬 Endpoints principales
POST /query
Consulta estándar con recuperación de contexto por cliente.
{
  "cliente": "recetron",
  "pregunta": "¿Qué es la inteligencia artificial moderna?"
}
Respuesta esperada:
{
  "cliente": "recetron",
  "respuesta": "La inteligencia artificial moderna se basa en modelos de aprendizaje profundo...",
  "fuentes": ["docs/archivo1.pdf", "docs/scrap.txt"]
}

📁 Estructura del repositorio

hacku_rag/
├── api/                        # API REST con FastAPI
│   └── main.py                # Endpoints: /query, /query-stream
│
├── core/                       # Lógica del sistema
│   ├── ingest.py              # Ingesta + limpieza de documentos
│   ├── embed_store.py         # Indexación en ChromaDB
│   ├── query_engine.py        # Prompt + RetrievalQA + LLM
│   ├── normalize_scraped_txt.py  # Limpieza de textos scrappeados
│   └── scraper.py             # Scraper básico de URLs
│
├── tasks/                      # Tareas asincrónicas (Celery)
│   └── scraper_task.py
│
├── scripts/                    # Utilitarios de prueba
│   └── run_scraper.py
│
├── clientes/                   # Datos por cliente
│   ├── recetron/
│   │   ├── docs/              # Archivos .txt, .pdf, .docx
│   │   ├── chroma_db/         # Vector store local (Chroma)
│   │   └── system_instruction.txt # Instrucciones del agente
│   ├── bancolombia/
│   └── terpel/
│
├── .env                        # Claves de entorno (NO versionar)
├── requirements.txt            # Dependencias Python
└── README.md                   # Este archivo 📄

🧠 ¿Cómo funciona?
Se detecta dinámicamente el cliente desde el payload.
Se cargan sus documentos vectorizados desde /clientes/[cliente]/docs.
Se aplica una instrucción system_instruction.txt exclusiva por cliente.
Se genera la respuesta usando gpt-4o-mini de OpenAI vía LangChain.
Se devuelven los resultados junto a las fuentes utilizadas.

El sistema usa ChromaDB como vector store local, con limpieza automática de PDFs y segmentación optimizada vía SentenceTransformersTokenTextSplitter.

🛠 Tecnologías utilizadas
🧠 LangChain + langchain-community
🧬 OpenAI (modelo: gpt-4o-mini)
🧲 ChromaDB
⚡ FastAPI
🧪 Uvicorn
📄 PDF / DOCX / TXT
🧹 Limpieza con SentenceTransformers splitter

✅ Pruebas
Puedes probar el sistema de tres formas:
http://localhost:8001/docs vía Swagger
Postman o Insomnia (POST /query)
Desde cualquier interfaz frontend (WhatsApp, web, etc.)

🔐 Seguridad
Cada agente tiene su propio vector store aislado.
Solo accede a sus documentos.
Se permite personalizar comportamiento con instrucciones por cliente.
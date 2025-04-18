import os
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ⚡ Modelo ajustado
model_name = "gpt-4o-mini"

def build_qa_chain(retriever, system_instruction_path=None, streaming=False, callbacks=None):
    # 1. Instrucción personalizada
    if system_instruction_path and os.path.exists(system_instruction_path):
        with open(system_instruction_path, "r", encoding="utf-8") as f:
            system_instruction = f.read()
    else:
        system_instruction = "Responde basándote únicamente en los documentos disponibles. Sé útil, preciso y profesional."

    # 2. Prompt tradicional (no ChatPromptTemplate)
    prompt = PromptTemplate.from_template(f"""
{system_instruction}

Usa la siguiente información para responder de forma clara y completa:

{{context}}

Pregunta: {{question}}
""")

    # 3. Inicializar modelo
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=0,
        streaming=streaming,
        callbacks=callbacks or [],
    )

    # 4. Chain clásica
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    return chain

def answer_question(chain, pregunta):
    """
    Consulta tradicional.
    """
    response = chain({"query": pregunta})
    return response["result"], response["source_documents"]

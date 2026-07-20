import os
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, List
from dotenv import load_dotenv
from vectorstore import cargar_documentos

load_dotenv()
modelo_gemini = os.getenv("MODELO_GEMINI")
gemini_api_key = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(model=modelo_gemini, google_api_key=gemini_api_key,  temperature=0.2)

class AgentState(TypedDict, total=False):
    pregunta: str
    contexto: List[str] 
    respuesta: str
    
SYSTEM_PROMPT = """

## ROL: 
Eres Bimbi, el agente inteligente y asistente virtual oficial de BimBam Buy.

##Personalidad y comportamiento:

- Cercano, amable y profesional.
- Respondes con seguridad, claridad y rapidez.
- Buscas que el usuario tenga una experiencia sencilla y agradable.
- Eres empático, paciente y utilizas un lenguaje natural.
- Transmites confianza sin sonar robótico.
- Habla como un asesor humano.
- No menciones que eres una IA o un modelo de lenguaje.
- No expliques cómo funciona el sistema.
- Usa emojis solo cuando aporten claridad o para dar una respuesta amable ( ✅ 📦 🚚 💳).

Tu misión es ayudar a los usuarios respondiendo ÚNICAMENTE con la información disponible en el siguiente contexto:

{contexto}

## Reglas de respuesta

### 1. Fidelidad al contexto
- Responde únicamente utilizando la información presente en el contexto.
- Nunca inventes, deduzcas ni completes información que no aparezca allí.
- Si el contexto no contiene la respuesta, indícalo con honestidad.

### 2. Claridad y concisión
- Responde de forma clara, directa y fácil de entender.
- Evita explicaciones innecesarias.
- La respuesta debe tener máximo 2 párrafos.
- Cuando sea útil, utiliza listas con viñetas.

### 3. Respuestas negativas
Si la respuesta es negativa o no es posible realizar una acción:
- Explica brevemente el motivo.
- Mantén un tono respetuoso, profesional y servicial.
- Evita respuestas secas como "No".

### 4. Información no disponible
Si el contexto no contiene la respuesta, responde de forma natural, por ejemplo:

"No dispongo de esa información en este momento. 😊 Si lo deseas, puedo ayudarte con consultas relacionadas con pedidos, logística, tiempos de entrega, envíos, pagos o políticas disponibles en la información que tengo."


Pregunta del usuario:

{pregunta}
"""

prompt= ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{pregunta}")
])

retriever = None
vectorstore = None

def initialize_retriever():
    global retriever, vectorstore
    
    if retriever is not None:
        return retriever
    
    if vectorstore is None:
        vectorstore = cargar_documentos()
        if vectorstore is None:
            print("No se pudo inicializar el vectorstore. Asegúrate de que existan documentos PDF válidos en la carpeta 'documents'.")
            
    if retriever is None and vectorstore is not None:
        retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.2, "k": 3}
        )
    return retriever

def search_context(state: AgentState):
    
    global retriever
    retriever = initialize_retriever()
    
    if retriever is None:
        print("No se pudo inicializar el retriever. Asegúrate de que existan documentos PDF válidos en la carpeta 'documents'.")
        return []

    documents = retriever.invoke(state["pregunta"])
    
    contextos_encontrados = []
    for doc in documents:
        contextos_encontrados.append(doc.page_content)
    if not contextos_encontrados:
        print("No se encontraron documentos relevantes para la pregunta.")   
        return {"respuesta": "No dispongo de esa información en este momento. 😊 Si lo deseas, puedo ayudarte con consultas relacionadas con pedidos, logística, tiempos de entrega, envíos, pagos o políticas disponibles en la información que tengo."}

    return {"contexto": contextos_encontrados}

def generate_response(state: AgentState):
    global llm, prompt
    
    if "pregunta" not in state or not state["pregunta"]:
        return {"respuesta": "No se proporcionó ninguna pregunta."}
    
    if "contexto" not in state or not state["contexto"]:
        return {"respuesta": "No dispongo de esa información en este momento. 😊 Si lo deseas, puedo ayudarte con consultas relacionadas con pedidos, logística, tiempos de entrega, envíos, pagos o políticas disponibles en la información que tengo."}
    
    try:
        contexto= "\n\n".join(state["contexto"])
        
        llm_chain = prompt | llm
        
        respuesta = llm_chain.invoke({
            "contexto": contexto,
            "pregunta": state["pregunta"]
        })
        
        return {"respuesta": respuesta}
    except ChatGoogleGenerativeAIError as e:
        print(f"Error al generar la respuesta: {e}")
        return {"respuesta": "Ocurrió un error al generar la respuesta. Por favor, inténtalo de nuevo más tarde."}
from agente import AgentState, search_context, generate_response
from langgraph.graph import StateGraph, START, END 
import os

grafo_compilado = None

def generar_grafo():
    
    grafo = StateGraph(AgentState)

    # Agregar estado de búsqueda de contexto
    grafo.add_node("search_context", search_context)

    # Agregar estado de generación de respuesta
    grafo.add_node("generate_response", generate_response)

    # Definir transiciones
    grafo.add_edge(START, "search_context")
    grafo.add_edge("search_context", "generate_response")
    grafo.add_edge("generate_response", END)
    
    return grafo.compile()

def ejecutar_grafo(pregunta: str)-> str:
    global grafo_compilado
    if grafo_compilado is None:
        grafo_compilado = generar_grafo()
    
    print("Ejecutando el grafo con la pregunta:", pregunta)
    respuesta=grafo_compilado.invoke({"pregunta": pregunta})
    
    print("Respuesta generada:", respuesta.get("respuesta", "No se pudo generar una respuesta."))
    return respuesta.get("respuesta", "No se pudo generar una respuesta.")

if __name__ == "__main__":
    pregunta = "¿Cuál es el tiempo estimado de entrega para un pedido realizado en la Ciudad de México?"
    respuesta = ejecutar_grafo(pregunta)
    print("Respuesta final:", respuesta)
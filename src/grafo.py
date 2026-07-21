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

def generar_visualizacion(grafo):
    """Genera y guarda la imagen del grafo dentro de la carpeta assets."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_dir = os.path.join(base_dir, "assets")
        
        os.makedirs(assets_dir, exist_ok=True)
        
        ruta_guardado = os.path.join(assets_dir, "grafo_flujo.png")
        
        png_data = grafo.get_graph().draw_mermaid_png()
        with open(ruta_guardado, "wb") as f:
            f.write(png_data)
            
        print(f"Imagen del grafo generada correctamente en: {ruta_guardado}")
    except Exception as e:
        print(f"Error al generar la imagen: {e}")

def ejecutar_grafo(pregunta: str)-> str:
    global grafo_compilado
    if grafo_compilado is None:
        grafo_compilado = generar_grafo()
    
    print("Ejecutando el grafo con la pregunta:", pregunta)
    respuesta=grafo_compilado.invoke({"pregunta": pregunta})
    
    print("Respuesta generada:", respuesta.get("respuesta", "No se pudo generar una respuesta."))
    
    #generar_visualizacion(grafo_compilado)
    return respuesta.get("respuesta", "No se pudo generar una respuesta.")


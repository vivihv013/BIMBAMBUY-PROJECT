import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
RUTA_FAISS = BASE_DIR / "faiss_index"
MODELO_EMBEDDING = os.getenv("MODELO_EMBEDDING", "gemini-embedding-001")
gemini_api_key = os.getenv("GEMINI_API_KEY")

def leer_documentos():
    
    """Procesa los archivos PDF de la carpeta documents, dividiéndolos en fragmentos."""
    
    documents = []
    BASE_DIR = Path(__file__).resolve().parent
    carpeta_docs = Path(BASE_DIR, "documents")

    print("Ruta documents:", carpeta_docs)
    print("Existe:", carpeta_docs.exists())

    for archivo in carpeta_docs.glob("*.*"):
        extension = archivo.suffix.lower()
        try:
            if extension == ".pdf":
                loader = PyMuPDFLoader(str(archivo))
                documents.extend(loader.load())
                print(f"PDF procesado: {archivo.name}")
        except Exception as e:
            print(f"Error procesado {archivo.name}: {e}")
    if not documents:
        print("No se encontraron documentos válidos en la carpeta 'documents'.")
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=250)
    fragmento = text_splitter.split_documents(documents)
    print(f"fragmentos creados: {len(fragmento)}")
    return fragmento

def cargar_documentos():
    """
        Inicializa el modelo de embeddings.

        Si existe un índice FAISS almacenado localmente, lo carga; de lo contrario,
        genera uno nuevo a partir de los documentos.
    """

    try:

        embeddings = GoogleGenerativeAIEmbeddings(model=MODELO_EMBEDDING, google_api_key=gemini_api_key)
        
        if os.path.exists(RUTA_FAISS):
            print("Índice FAISS detectado. Recuperando los vectores desde el almacenamiento local...")
        
            vector_store = FAISS.load_local(RUTA_FAISS, embeddings, allow_dangerous_deserialization=True)
            return vector_store
        
        print("No detecto ningun indice FAISS. Creando nuevo indice a partir de los documentos en la carpeta 'documents'...")
        frag = leer_documentos()
        
        if not frag:
            print("No se generaron fragmentos de texto. Comprueba que existan documentos PDF válidos en la carpeta 'documents'.")
            return None

        vector_store = FAISS.from_documents(frag, embeddings)
        vector_store.save_local(RUTA_FAISS)
        print(f"Nuevo índice FAISS creado y guardado exitosamente en '{RUTA_FAISS}'.")
        
        return vector_store
    
    except Exception as e:
        print(f"Error al crear o cargar el índice FAISS: {e}")
        return None
    

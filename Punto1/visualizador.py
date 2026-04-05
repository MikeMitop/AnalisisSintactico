import networkx as nx
import matplotlib.pyplot as plt
from nodos import NodoOperacion, NodoValor

def construir_grafo(nodo, grafo, posiciones, x=0, y=0, capa=1):
    """Función recursiva para mapear el AST en un grafo de NetworkX con coordenadas."""
    if nodo is None:
        return

    # Usamos la dirección de memoria id() para que los nodos con el mismo valor no se sobreescriban
    nodo_id = str(id(nodo))

    if isinstance(nodo, NodoOperacion):
        grafo.add_node(nodo_id, label=nodo.operador)
        posiciones[nodo_id] = (x, y)
        
        # Procesar hijo izquierdo
        hijo_izq_id = str(id(nodo.izquierda))
        grafo.add_edge(nodo_id, hijo_izq_id)
        # Desplazamos a la izquierda y abajo
        construir_grafo(nodo.izquierda, grafo, posiciones, x - 1/(capa**0.8), y - 1, capa + 1)
        
        # Procesar hijo derecho
        hijo_der_id = str(id(nodo.derecha))
        grafo.add_edge(nodo_id, hijo_der_id)
        # Desplazamos a la derecha y abajo
        construir_grafo(nodo.derecha, grafo, posiciones, x + 1/(capa**0.8), y - 1, capa + 1)
        
    elif isinstance(nodo, NodoValor):
        grafo.add_node(nodo_id, label=nodo.valor)
        posiciones[nodo_id] = (x, y)

def dibujar_arbol_visual(nodo_raiz):
    """Crea y muestra la ventana gráfica con el AST."""
    grafo = nx.DiGraph()
    posiciones = {}
    
    construir_grafo(nodo_raiz, grafo, posiciones)
    
    # Extraer etiquetas para dibujarlas
    etiquetas = nx.get_node_attributes(grafo, 'label')
    
    plt.figure(figsize=(8, 6))
    plt.title("Árbol de Sintaxis Abstracto (AST)", fontsize=14)
    
    # Dibujar nodos, bordes y etiquetas
    nx.draw(grafo, pos=posiciones, with_labels=False, node_size=2000, 
            node_color="lightblue", edge_color="gray", arrows=False)
    nx.draw_networkx_labels(grafo, pos=posiciones, labels=etiquetas, 
                            font_size=12, font_family="sans-serif", font_weight="bold")
    
    plt.axis("off") # Ocultar ejes
    plt.show()      # Mostrar ventana
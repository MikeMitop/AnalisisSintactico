import matplotlib.pyplot as plt
import networkx as nx
from lark import Lark, Tree
import sys


# Asociatividad Izquierda
gramatica_izq = """
    ?start: expr
    expr: expr "-" NUMERO | NUMERO
    NUMERO: /\d+/
    %ignore " "
"""

# Asociatividad Derecha
gramatica_der = """
    ?start: expr
    expr: NUMERO "-" expr | NUMERO
    NUMERO: /\d+/
    %ignore " "
"""

# Precedencia Alta (*)
gramatica_prec_alta = """
    ?start: expr
    expr: expr "+" term | term
    term: term "*" NUMERO | NUMERO
    NUMERO: /\d+/
    %ignore " "
"""

# Precedencia Baja (*)
gramatica_prec_baja = """
    ?start: expr
    expr: expr "*" term | term
    term: term "+" NUMERO | NUMERO
    NUMERO: /\d+/
    %ignore " "
"""

DICCIONARIO_EXPLICATIVO = {
    'start': 'RAÍZ DEL CÁLCULO',
    'expr': 'OPERACIÓN',
    'term': 'TÉRMINO AGRUPADO',
    'NUMERO': 'VALOR NUMÉRICO',
    # Mapeo directo de signos para mayor claridad semántica
    '+': 'SUMA (+)',
    '-': 'RESTA (-)',
    '*': 'MULTIPLICACIÓN (*)',
    '/': 'DIVISIÓN (/)'
}

def procesar_y_dibujar_ventana_separada(gramatica, cadena, titulo, color, numero_ventana):
    """
    Genera el parser, crea el AST y abre una NUEVA ventana emergente 
    con etiquetas explicativas fáciles de entender.
    """
    try:
        parser = Lark(gramatica, parser='lalr')
        arbol = parser.parse(cadena)
    except Exception as e:
        print(f"Error analizando '{cadena}' para {titulo}: {e}")
        return

    plt.figure(numero_ventana, figsize=(10, 8))
    ax = plt.gca() # Obtener el eje actual de esta nueva figura
    
    grafo = nx.DiGraph()
    posiciones = {}
    
    # Función recursiva para construir el grafo visual con etiquetas conceptuales
    def recorrer(nodo, x=0, y=0, id_padre=None, ancho=2.0):
        nodo_id = str(id(nodo))
        
        if isinstance(nodo, Tree):
            # Es una Regla (No terminal): Buscamos su traducción conceptual
            nombre_tecnico = nodo.data
            etiqueta_conceptual = DICCIONARIO_EXPLICATIVO.get(nombre_tecnico, nombre_tecnico.upper())
            
            # Mejora especial: Si es una operación, intentar identificar cuál es mirando a los hijos
            if nombre_tecnico == 'expr' or nombre_tecnico == 'term':
                tiene_signo = False
                for hijo in nodo.children:
                    if not isinstance(hijo, Tree) and str(hijo) in DICCIONARIO_EXPLICATIVO:
                        signo_txt = str(hijo)
                        etiqueta_conceptual = f"OP. {DICCIONARIO_EXPLICATIVO[signo_txt]}"
                        tiene_signo = True
                        break
                if not tiene_signo:
                    etiqueta_conceptual = "PASO INTERMEDIO"

        else:
            # Es un Token (Terminal): Un número o un signo directo
            valor_texto = str(nodo)
            if valor_texto.isdigit():
                etiqueta_conceptual = f"DATO:\n{valor_texto}" # Mostramos el número claramente
            else:
                # Signos (+, -, *, /)
                etiqueta_conceptual = DICCIONARIO_EXPLICATIVO.get(valor_texto, valor_texto)

        grafo.add_node(nodo_id, label=etiqueta_conceptual)
        posiciones[nodo_id] = (x, y)
        if id_padre:
            grafo.add_edge(id_padre, nodo_id)
            
        if isinstance(nodo, Tree):
            # Cálculo de posiciones de hijos
            inicio_x = x - (ancho * (len(nodo.children) - 1)) / 2
            for i, hijo in enumerate(nodo.children):
                recorrer(hijo, inicio_x + i * ancho, y - 1, nodo_id, ancho / 2)

    recorrer(arbol)
    
    etiquetas = nx.get_node_attributes(grafo, 'label')
    nx.draw(grafo, pos=posiciones, ax=ax, with_labels=True, labels=etiquetas,
            node_size=4000, # Nodos más grandes para etiquetas más largas
            node_color=color, 
            font_size=10, # Fuente ligeramente más pequeña para que quepan las palabras
            font_weight="bold", 
            edge_color="#555555", # Gris oscuro para las flechas
            arrows=True, # Mostrar dirección del flujo
            node_shape='s') # Forma cuadrada para simular "bloques de concepto"
    
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    plt.axis('off') # Ocultar ejes coordenados

if __name__ == "__main__":
    print("Generando Gráficos")

    procesar_y_dibujar_ventana_separada(
        gramatica_izq, "8 - 4 - 2", 
        "TEST 1: Asociatividad por IZQUIERDA", 
        "#ffb3ba", numero_ventana=1
    )
                       
    procesar_y_dibujar_ventana_separada(
        gramatica_der, "8 - 4 - 2", 
        "TEST 2: Asociatividad por DERECHA", 
        "#baffc9", numero_ventana=2
    )
                       
    procesar_y_dibujar_ventana_separada(
        gramatica_prec_alta, "2 + 3 * 4", 
        "TEST 3: Precedencia ALTA del (*)", 
        "#bae1ff", numero_ventana=3
    )
                       
    procesar_y_dibujar_ventana_separada(
        gramatica_prec_baja, "2 + 3 * 4", 
        "TEST 4: Precedencia BAJA del (*)\n(Gramática forzada: la suma se hace antes)", 
        "#ffffba", numero_ventana=4
    )

    # Mostrar todas las ventanas generadas
    plt.show()
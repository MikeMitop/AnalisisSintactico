# Construccion de un Arbol de Sintaxis Abstracto (AST)

# Problema Principal:

- Implementar un programa en Python que dada una gramática y una cadena, genere un AST.

## Introduccion

Este proyecto implementa un programa en Python capaz de tomar una expresión matemática en formato de texto, realizar un análisis léxico y sintáctico basado en una gramática libre de contexto, y generar una representación visual de su Árbol de Sintaxis Abstracto (AST). El programa lee la entrada desde un archivo de texto, procesa la jerarquía de las operaciones y utiliza herramientas gráficas para dibujar el resultado en una ventana emergente.
## Objetivo General

Desarrollar un analizador sintáctico descendente  modular en Python que evalúe cadenas matemáticas y grafique su correspondiente Árbol de Sintaxis Abstracto.
### Objetivos Específicos

1. Construir un analizador léxico que separe una cadena de texto en tokens válidos.
 
2. Implementar las reglas de una gramática matemática respetando la jerarquía de operaciones (paréntesis, multiplicación/división, suma/resta).

3. Utilizar librerías gráficas para mapear y renderizar la estructura de datos no lineal (el árbol) en una interfaz visual
# Jerarquía de carpetas

**El proyecto está dividido en submódulos para garantizar un código limpio y escalable:**

``` 
/proyecto_ast
│
├── cadena.txt          # Archivo de texto que contiene la expresión a evaluar
├── main.py             # Script principal que orquesta la lectura y ejecución
├── nodos.py            # Definición de las estructuras de datos (Nodos del árbol)
├── lexer.py            # Analizador léxico (Tokenizador)
├── parser_ast.py       # Analizador sintáctico (Constructor del árbol)
└── visualizador.py     # Motor de renderizado gráfico con NetworkX y Matplotlib
``` 

# Desarrollo
### Código fuente

**A continuación se presenta el código de cada uno de los módulos que conforman el proyecto:**

```
nodos.py
```
Define la estructura base del árbol, conteniendo una clase general y clases derivadas para los valores numéricos y las operaciones.

```python
class NodoAST:
    """Clase base para todos los nodos del árbol."""
    pass

class NodoOperacion(NodoAST):
    """Nodo que representa operaciones matemáticas (+, -, *, /) y tiene dos hijos."""
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

class NodoValor(NodoAST):
    """Nodo hoja que representa un número."""
    def __init__(self, valor):
        self.valor = valor
```

```
lexer.py
```

**Convierte la cadena de texto de entrada en una lista de tokens reconocibles mediante expresiones regulares, ignorando espacios y detectando errores léxicos.**

```python
import re

def tokenizar(cadena):
    """Convierte la cadena de texto de entrada en una lista de tokens reconocibles."""
    especificacion = [
        ('NUMERO',    r'\d+'),       
        ('SUMA',      r'\+'),        
        ('RESTA',     r'-'),         
        ('MULT',      r'\*'),        
        ('DIV',       r'/'),         
        ('PAREN_IZQ', r'\('),        
        ('PAREN_DER', r'\)'),        
        ('ESPACIO',   r'\s+'),       
        ('ERROR',     r'.'),         
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in especificacion)
    tokens = []
    
    for coincidencia in re.finditer(tok_regex, cadena):
        tipo = coincidencia.lastgroup
        valor = coincidencia.group()
        
        if tipo == 'ESPACIO':
            continue
        elif tipo == 'ERROR':
            raise ValueError(f"Error léxico: '{valor}'")
        tokens.append((tipo, valor))
        
    return tokens
```
```
parser_ast.py
    
```

**Construye el Árbol de Sintaxis Abstracto consumiendo los tokens generados por el lexer e instanciando los objetos importados de nodos.py**

```python
from nodos import NodoOperacion, NodoValor

class Parser:
    """Construye el AST a partir de la lista de tokens."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def avanzar(self):
        self.pos += 1

    def parsear(self):
        if not self.tokens:
            raise ValueError("Error sintáctico: ")
        
        nodo_raiz = self.expresion()
        
        if self.actual() is not None:
            raise ValueError(f"Error sintáctico: {self.actual()[1]}")
        return nodo_raiz

    def expresion(self):
        nodo = self.termino()
        while self.actual() and self.actual()[0] in ('SUMA', 'RESTA'):
            op = self.actual()[1]
            self.avanzar()
            derecha = self.termino()
            nodo = NodoOperacion(nodo, op, derecha)
        return nodo

    def termino(self):
        nodo = self.factor()
        while self.actual() and self.actual()[0] in ('MULT', 'DIV'):
            op = self.actual()[1]
            self.avanzar()
            derecha = self.factor()
            nodo = NodoOperacion(nodo, op, derecha)
        return nodo

    def factor(self):
        token = self.actual()
        if token is None:
            raise ValueError("Error sintáctico: ")

        if token[0] == 'NUMERO':
            self.avanzar()
            return NodoValor(token[1])
        elif token[0] == 'PAREN_IZQ':
            self.avanzar()
            nodo = self.expresion()
            if self.actual() and self.actual()[0] == 'PAREN_DER':
                self.avanzar()
                return nodo
            else:
                raise ValueError("Error sintáctico: ParentesisEl flujo de trabajo del algoritmo se divide en tres grandes fases. Primero, la fase de Análisis Léxico (lexer.py), donde se procesa la cadena de texto plano usando expresiones regulares para agrupar los caracteres en "Tokens" con significado lógico (como NUMERO o SUMA). A continuación, la fase de Análisis Sintáctico (parser_ast.py), donde el programa consume dichos tokens de forma recursiva simulando las reglas de precedencia; las operaciones de mayor prioridad (como las multiplicaciones o lo contenido en paréntesis) se resuelven primero en la pila de llamadas, asegurando que queden en las partes más profundas del árbol. Finalmente, la fase de Visualización recorre este árbol de nodos en memoria utilizando recursividad, asignando coordenadas espaciales dinámicas (desplazándose en x e y según la capa de profundidad) para evitar la superposición de ramas y renderizándolo con NetworkX. NO cerrado")
        else:
            raise ValueError(f"Error sintáctico: '{token[1]}'")

```

```
visualizador.py
```

**Se encarga de recorrer la estructura de nodos recursivamente y mapearla a coordenadas bidimensionales utilizando las librerías networkx y matplotlib para abrir la ventana interactiva.**

```python
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
```

```
main.py
```
    
**Es el orquestador del proyecto. Lee el archivo cadena.txt validando su existencia, invoca a los demás módulos y maneja las posibles excepciones y errores de compilación.**

 ```python

    import os
from lexer import tokenizar
from parser_ast import Parser
from visualizador import dibujar_arbol_visual

def main():
    nombre_archivo = "cadena.txt"
    
    if not os.path.exists(nombre_archivo):
        print(f"No se encontró el archivo '{nombre_archivo}'.")
        return

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            # .strip() elimina saltos de línea y espacios en blanco al inicio y al final
            cadena = archivo.read().strip() 
            
        if not cadena:
            print("El archivo está vacío.")
            return
            
        print(f"Leyendo desde '{nombre_archivo}'...")
        print(f"Evaluando cadena: '{cadena}'...\n")

        tokens = tokenizar(cadena)
        
        parser = Parser(tokens)
        ast_raiz = parser.parsear()
        
        print("Sintaxis correcta.")
        
        dibujar_arbol_visual(ast_raiz)
        
    except ValueError as e:
        print(f"COMPILACIÓN FALLIDA:\n {e}")
    except Exception as e:
        print(f" ERROR AL LEER EL ARCHIVO:\n {e}")

if __name__ == "__main__":
    main()
    
```

# Salida Esperada
Al proporcionarle al programa una cadena válida compleja en el archivo cadena.txt, como por ejemplo ( ( 5 + 3 ) * 2 ) - ( 8 / 4 ),
la terminal imprimirá un mensaje indicando éxito en la lectura y sintaxis, y se abrirá una ventana de Matplotlib mostrando el árbol 
estructurado correctamente con nodos celestes y conexiones grises. Si se ingresa una cadena inválida, el programa capturará y mostrará el error 
(léxico o sintáctico) en la consola y detendrá el programa.


  ## Pasos de Ejecución

Instalar las dependencias necesarias ejecutando en la terminal:
```bash
pip install networkx matplotlib
```

Ir hacia la ubicacion del archivo

Compilar el main de la siguiente forma:
```bash
python main.py cadena.txt
```

# Análisis del Funcionamiento

El flujo de trabajo del algoritmo se divide en tres grandes fases. Primero, la fase de Análisis Léxico (lexer.py), 
donde se procesa la cadena de texto plano usando expresiones regulares para agrupar los caracteres en "Tokens" con significado lógico (como NUMERO o SUMA).
 A continuación, la fase de Análisis Sintáctico (parser_ast.py), donde el programa consume dichos tokens de forma recursiva simulando las reglas de precedencia; 
las operaciones de mayor prioridad (como las multiplicaciones o lo contenido en paréntesis) se resuelven primero en la pila de llamadas, asegurando que queden en las partes más profundas del árbol. 
Finalmente, la fase de Visualización recorre este árbol de nodos en memoria utilizando recursividad, asignando coordenadas espaciales dinámicas (desplazándose en x e y según la capa de profundidad) 
para evitar la superposición de ramas y renderizándolo con NetworkX.

# Conclusiones:


1. Modularidad: 
Separar el proyecto en submódulos (Lexer, Parser, Estructuras y Visualizador) reduce drásticamente la complejidad cognitiva.

2. Manejo de Precedencia: 
El uso del análisis descendente recursivo (Recursive Descent Parsing) ha demostrado ser altamente efectivo y directo para hacer respetar el orden de las operaciones matemáticas de forma nativa a través de funciones anidadas.

3. Ventaja Visual: 
Trasladar la estructura abstracta y no lineal de la memoria a un gráfico bidimensional interactivo permite una depuración más ágil y hace que la comprensión del procesamiento de la máquina sea sumamente accesible para el usuario final.


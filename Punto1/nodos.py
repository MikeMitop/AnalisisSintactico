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
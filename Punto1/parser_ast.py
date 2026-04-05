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
                raise ValueError("Error sintáctico: Parentesis NO cerrado")
        else:
            raise ValueError(f"Error sintáctico: '{token[1]}'")
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
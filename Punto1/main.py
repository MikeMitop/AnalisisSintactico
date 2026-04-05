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
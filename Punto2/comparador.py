import subprocess
import time
import random
import matplotlib.pyplot as plt


GramaticaCNF = {
    'variaciones_no_terminales': {
        ('A', 'B'): 'S', ('B', 'C'): 'S',
        ('B', 'A'): 'A', ('C', 'C'): 'B', ('A', 'B'): 'C',
    },
    'variaciones_terminales': { 'a': ['A', 'C'], 'b': ['B'] },
    'simbolo_inicial': 'S'
}

def ejecutar_cyk(cadena, gramatica):
    n = len(cadena)
    if n == 0: return False
    tabla = [[set() for _ in range(n)] for _ in range(n)]
    term = gramatica['variaciones_terminales']
    non_term = gramatica['variaciones_no_terminales']
    
    for i in range(n):
        if cadena[i] in term:
            for nt in term[cadena[i]]: tabla[i][i].add(nt)
            
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            for k in range(i, j):
                for b in tabla[i][k]:
                    for c in tabla[k+1][j]:
                        if (b, c) in non_term:
                            tabla[i][j].add(non_term[(b, c)])
                            
    return gramatica['simbolo_inicial'] in tabla[0][n-1]


def realizar_comparativa(n_max, pasos):
    longitudes = []
    tiempos_cyk = []
    tiempos_bison = []

    print("🚀 Iniciando Benchmark (CYK [Python] vs Flex/Bison [C Nativo])...")
    
    #  10 hasta n_max, saltando de N en N pasos
    for n in range(10, n_max + 1, pasos):
        cadena = ''.join(random.choice(['a', 'b']) for _ in range(n))
        
        # --- Medir CYK en Python ---
        inicio_cyk = time.perf_counter()
        ejecutar_cyk(cadena, GramaticaCNF)
        fin_cyk = time.perf_counter()
        t_cyk = fin_cyk - inicio_cyk
        
        # Llamamos al ejecutable C que creamos y leemos su salida (el tiempo impreso)
        resultado = subprocess.run(["./parser_bison", cadena], capture_output=True, text=True)
        try:
            t_bison = float(resultado.stdout.strip())
        except ValueError:
            t_bison = 0.0 #
            
        longitudes.append(n)
        tiempos_cyk.append(t_cyk)
        tiempos_bison.append(t_bison)
        
        print(f" N={n:03d} | CYK (Python): {t_cyk:.5f}s | Bison (C): {t_bison:.6f}s")

    plt.figure(figsize=(10, 6))
    plt.plot(longitudes, tiempos_cyk, 'o-', label='CYK en Python ($O(N^3)$)', color='blue', linewidth=2)
    plt.plot(longitudes, tiempos_bison, 's-', label='Flex/Bison en C ($O(N)$)', color='red', linewidth=2)
    
    plt.title('Comparación de Rendimiento: Análisis Sintáctico', fontsize=14)
    plt.xlabel('Longitud de la Cadena', fontsize=12)
    plt.ylabel('Tiempo de Ejecución (Segundos)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    plt.fill_between(longitudes, tiempos_cyk, tiempos_bison, color='gray', alpha=0.1)
    plt.show()

if __name__ == "__main__":
    # N=200 es suficiente para que CYK empiece a asfixiarse en Python.
    # Bison lo procesará literalmente en 0.00000X segundos.
    realizar_comparativa(n_max=200, pasos=20)
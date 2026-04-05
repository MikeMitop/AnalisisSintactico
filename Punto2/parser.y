%{
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int yylex(void);
void yyerror(const char *s);

/* Funciones de Flex para leer desde un string en lugar de la consola (stdin) */
typedef struct yy_buffer_state * YY_BUFFER_STATE;
extern YY_BUFFER_STATE yy_scan_string(const char * str);
extern void yy_delete_buffer(YY_BUFFER_STATE buffer);
%}

%token TOKEN_A TOKEN_B

%%
/* La misma gramática CNF adaptada para Bison */
s: a b | b c ;
a: b a | TOKEN_A ;
b: c c | TOKEN_B ;
c: a b | TOKEN_A ;
%%

void yyerror(const char *s) {
    /* Silenciamos los errores sintácticos. 
       Bison fallará rápido si la sintaxis es incorrecta, lo cual es parte de su eficiencia O(N) */
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("0.0\n");
        return 1;
    }

    /* 1. Preparamos Flex para leer el argumento enviado desde Python */
    YY_BUFFER_STATE buffer = yy_scan_string(argv[1]);

    /* 2. Iniciamos el cronómetro interno de C (Máxima precisión) */
    clock_t start = clock();
    
    yyparse(); // Ejecuta el análisis
    
    clock_t end = clock();
    /* 3. Detenemos el cronómetro */

    yy_delete_buffer(buffer);

    /* 4. Imprimimos SOLO el tiempo (Python leerá este número) */
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("%f\n", time_spent);
    
    return 0;
}
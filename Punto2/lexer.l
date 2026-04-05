%{
#include "parser.tab.h" // Importa los tokens generados por Bison
%}

/* Le decimos a Flex que no envuelva archivos múltiples */
%option noyywrap

%%
"a"     { return TOKEN_A; }
"b"     { return TOKEN_B; }
[ \t]   { /* Ignorar espacios */ }
.       { /* Ignorar cualquier otra cosa */ }
%%
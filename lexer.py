import sys
import ply.lex as lex 

reserved = {
    'programa': 'PROGRAMA',
    'principal': 'PRINCIPAL',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void': 'VOID',
    'funcion': 'FUNCION',
    'regresa': 'REGRESA',
    'lee': 'LEE',
    'imprime': 'IMPRIME',
    'si': 'SI',
    'entonces': 'ENTONCES',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'hasta': 'HASTA',
    'para': 'PARA'
}

tokens = [
    'MAYOR_QUE',
    'MENOR_QUE',
    'AND',
    'OR',
    'DIFERENTE_A',
    'IGUAL_A',
    'MAS',
    'MENOS',
    'DIVIDE',
    'MULTIPLICA',
    'LEFTPAR',
    'RIGHTPAR',
    'IGUAL',
    'COMA',
    'PUNTOYCOMA',
    'ID',
    'LEFTBRACK',
    'RIGHTBRACK',
    'LEFTBRACE',
    'RIGHTBRACE',
    'EXCLAMACION',
    'INTERROGACION',
    'SIGNO_DOLAR',
    'CST_INT',
    'CST_FLOAT',
    'CST_STRING',
    'CST_CHAR',
    'COMMENT_TEXT'
] + list(reserved.values())

# Tokens

t_MAYOR_QUE           = r'>'
t_MENOR_QUE           = r'<'
t_AND           = r'&'
t_OR            = r'\|'
t_DIFERENTE_A      = r'<>'
t_IGUAL_A      = r'=='
t_MAS         = r'\+'
t_MENOS         = r'-'
t_DIVIDE        = r'/'
t_MULTIPLICA      = r'\*'
t_LEFTPAR       = r'\('
t_RIGHTPAR      = r'\)'
t_IGUAL         = r'='
t_COMA          = r','
t_PUNTOYCOMA     = r';'
t_LEFTBRACK     = r'\['
t_RIGHTBRACK    = r'\]'
t_LEFTBRACE     = r'\{'
t_RIGHTBRACE    = r'\}'
t_EXCLAMACION   = r'!'
t_INTERROGACION      = r'\?'
t_SIGNO_DOLAR    = r'\$'
t_CST_INT       = r'[0-9]+'
t_CST_FLOAT     = r'[0-9]+\.[0-9]+'
t_CST_CHAR      = r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')'
t_CST_STRING    = r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
t_COMMENT_TEXT  = r'%%.*\n'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

#Ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s' in line %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
    exit(0)

lexer = lex.lex()

lex.lex()

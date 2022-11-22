import ply.lex as lex 

#Palabras Reservadas
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
    'para': 'PARA',
    'raizcuadrada': 'RAIZCUADRADA',
    'cuadratica':'CUADRATICA',
    'pow':'POW',
    'exponencial':'EXPONENCIAL',
    'redondear':'REDONDEAR',
    'arriba':'ARRIBA',
    'abajo':'ABAJO',
    'gamma':'GAMMA',
    'residuo':'RESIDUO',
    'radianes':'RADIANES',
    'grados':'GRADOS',
    'seno':'SENO',
    'coseno':'COSENO',
    'tangente':'TANGENTE',
    'logaritmo':'LOGARITMO',
}

tokens = [
    'MAYOR_QUE',
    'MENOR_QUE',
    'MENOR_IGUAL',
    'MAYOR_IGUAL',
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
    'PUNTO',
    'LEFTBRACK',
    'RIGHTBRACK',
    'LEFTBRACE',
    'RIGHTBRACE',
    'CST_INT',
    'CST_FLOAT',
    'CST_STRING',
    'CST_CHAR',
    'COMMENT_TEXT'
] + list(reserved.values())

# Tokens

t_MAYOR_QUE           = r'>'
t_MENOR_QUE           = r'<'
t_MAYOR_IGUAL           = r'>='
t_MENOR_IGUAL          = r'<='
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
t_PUNTO          = r'.'
t_LEFTBRACK     = r'\['
t_RIGHTBRACK    = r'\]'
t_LEFTBRACE     = r'\{'
t_RIGHTBRACE    = r'\}'
t_CST_INT       = r'[0-9]+'
t_CST_FLOAT     = r'[0-9]+\.[0-9]+'
t_CST_CHAR      = r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')'
t_CST_STRING    = r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
t_COMMENT_TEXT  = r'//.*\n'


t_ignore = " \t\r"

#ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Caracter ilegal '%s' en la linea %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
    exit(0)

lexer = lex.lex()

lex.lex()

# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.:  
# ------------------------------------------------ #
#

class TokensClass:
    ID = (1, 'ident')
    CTE = (2, 'const')
    CADEIA = (3, 'cad')
    PROGRAMA = (4, 'PROGRAMA')
    VARIAVEIS = (5, 'VARIAVEIS')
    INTEIRO = (6, 'INTEIRO')
    REAL = (7, 'REAL')
    LOGICO = (8, 'LOGICO')
    CARACTER = (9, 'CARACTER')
    SE = (10, 'SE')
    SENAO = (11, 'SENAO')
    ENQUANTO = (12, 'ENQUANTO')
    LEIA = (13, 'LEIA')
    ESCREVA = (14, 'ESCREVA')
    FALSO = (15, 'FALSO')
    VERDADEIRO = (16, 'VERDADEIRO')
    ATRIB = (17, ':=')
    OPREL = (18, ['=', '<', '>', '<=', '>=', '<>'])
    OPAD = (19, ['+', '-'])
    OPMUL = (20, ['*', '/'])
    OPNEG = (21, '!')
    PVIRG = (22, ';')
    DPONTOS = (23, ':')
    VIRG = (24, ',')
    ABREPAR = (25, '(')
    FECHAPAR = (26, ')')
    ABRECH = (27, '{')
    FECHACH = (28, '}')
    FIMARQ = (29, '$')
    ERROR = (30, 'erro')

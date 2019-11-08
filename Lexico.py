# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.: 0002864 
# ------------------------------------------------ #
#

import Token
import TokensClass

class Lexico:
    reservadas = {
        'PROGRAMA': TokensClass.TokensClass.PROGRAMA,
        'VARIAVEIS': TokensClass.TokensClass.VARIAVEIS,
        'INTEIRO': TokensClass.TokensClass.INTEIRO,
        'REAL': TokensClass.TokensClass.REAL,
        'LOGICO': TokensClass.TokensClass.LOGICO,
        'CARACTER': TokensClass.TokensClass.CARACTER,
        'SE': TokensClass.TokensClass.SE,
        'SENAO': TokensClass.TokensClass.SENAO,
        'ENQUANTO': TokensClass.TokensClass.ENQUANTO,
        'LEIA': TokensClass.TokensClass.LEIA,
        'ESCREVA': TokensClass.TokensClass.ESCREVA,
        'FALSO': TokensClass.TokensClass.FALSO,
        'VERDADEIRO': TokensClass.TokensClass.VERDADEIRO
    }
    
    def __init__(self):
        self.buffer = ''
    
    def getChar(self, arq, linha):
        carct = None

        if(not(arq is None)):
            # Pega um caracter ja no buffer
            if(len(self.buffer) > 0):
                carct = self.buffer[0]
                self.buffer = self.buffer[1:]
            else:
                # Quando o buffer nao tem mais informacoes, busca do arquivo fonte
                carct = arq.read(1)

                if(carct == '\n'):
                    linha += 1
            
        return (carct, linha)

    def ungetChar(self, carct):
        if(not (carct is None)):
            self.buffer += carct
    
    def getToken(self, arq, linha):
        lexema = ''
        carct = None
        estado = 1

        while(True):
            if(estado == 1): # Estado de identificacao do caracter
                (carct, linha) = self.getChar(arq, linha)

                if((carct is None) or (carct == '')):
                    return (Token.Token(TokensClass.TokensClass.FIMARQ, '$', linha), linha)
                elif(carct in [' ', '\t', '\n']):
                    pass
                elif(carct.isalpha()):
                    estado = 2
                elif((carct.isdigit()) or (carct == '.')):
                    estado = 3
                elif(carct == '"'):
                    estado = 4
                elif(carct in [':=', '=', '<', '>', '<=', '>=', '<>', '+', '-', '*', '/', '!', ';', ':', ',', '(', ')', '{', '}']):
                    estado = 5
                else:
                    return (Token.Token(TokensClass.TokensClass.ERROR, '<'+ carct +'>', linha), linha)
            elif(estado == 2): # Estado para tratar identificadores e palavras reservadas
                lexema += carct
                (carct, linha) = self.getChar(arq, linha)

                # Verifica se a palavra terminou
                if((carct is None) or (not(carct.isalnum()))):
                    self.ungetChar(carct)

                    if(lexema in self.reservadas):
                        return (Token.Token(self.reservadas[lexema], lexema, linha), linha)
                    else:
                        # ID validos devem possuir no max, 32 caracters
                        if(len(lexema) <= 32):
                            return (Token.Token(TokensClass.TokensClass.ID, lexema, linha), linha)
                        else:
                            return (Token.Token(TokensClass.TokensClass.ERROR, lexema, linha), linha)
            elif(estado == 3): # Estado para tratar constantes numericas inteiras e reais
                lexema += carct
                (carct, linha) = self.getChar(arq, linha)

                # Verifica se a constante numerica terminou
                if((carct is None) or (not(carct.isdigit()) and not(carct == '.'))):
                    self.ungetChar(carct)
                    return (Token.Token(TokensClass.TokensClass.CTE, lexema, linha), linha)
            elif(estado == 4): # Estado para tratar cadeia de caracter entre ""
                lexema += carct
                (carct, linha) = self.getChar(arq, linha)
                
                while(not(carct is None) and (carct != '\n') and (carct != '"')):
                    lexema += carct
                    (carct, linha) = self.getChar(arq,linha)
                
                if(carct == '"'):
                    lexema += carct
                    return (Token.Token(TokensClass.TokensClass.CADEIA, lexema, linha), linha)
                else:
                    lexema = ''
                    estado = 1
            elif(estado == 5): # Estado para tratar outros tokens primitivos
                lexema += carct
                
                if(carct == '='):
                    return (Token.Token(TokensClass.OPREL, lexema, linha), linha)
                elif(carct == '<'):
                    (carct, linha) = self.getChar(arq, linha)

                    # Verifica se eh o '<', '<=' ou '<>'
                    if(carct == '='):
                        lexema += carct
                        return (Token.Token(TokensClass.TokensClass.OPREL, lexema, linha), linha)
                    elif(carct == '>'):
                        lexema += carct
                        return (Token.Token(TokensClass.TokensClass.OPREL, lexema, linha), linha)
                    else:
                        self.ungetChar(carct)
                        return (Token.Token(TokensClass.TokensClass.OPREL, lexema, linha), linha)
                elif(carct == '>'):
                    (carct, linha) = self.getChar(arq, linha)

                    # Verifica se eh o '>' ou '>='
                    if(carct == '='):
                        lexema += carct
                        return (Token.Token(TokensClass.TokensClass.OPREL, lexema, linha), linha)
                    else:
                        self.ungetChar(carct)
                        return (Token.Token(TokensClass.TokensClass.OPREL, lexema, linha), linha)
                elif(carct == '+'):
                    return (Token.Token(TokensClass.TokensClass.OPAD, lexema, linha), linha)
                elif(carct == '-'):
                    return (Token.Token(TokensClass.TokensClass.OPAD, lexema, linha), linha)
                elif(carct == '*'):
                    return (Token.Token(TokensClass.TokensClass.OPMUL, lexema, linha), linha)
                elif(carct == '/'):
                    (carct, linha) = self.getChar(arq, linha)

                    # Verifica se eh o '/' ou '//' ou '/**/'
                    if(carct == '/'): # Para tratar comentarios de linha
                        while(not(carct is None) and (carct != '\n')):
                            (carct, linha) = self.getChar(arq,linha)
                        
                        lexema = ''
                        estado = 1
                    elif(carct == '*'): # Para tratar comentarios de bloco
                        (carct, linha) = self.getChar(arq,linha)

                        while(not(carct is None) and (carct != '*')):
                            (carct, linha) = self.getChar(arq,linha)

                            if(carct == ''):
                                    break

                        if(carct == '*'):
                            while(not(carct is None) and(carct != '/')):
                                (carct, linha) = self.getChar(arq,linha)

                                if(carct == ''):
                                    break
                        
                        lexema = ''
                        estado = 1
                    else:
                        self.ungetChar(carct)
                        return (Token.Token(TokensClass.TokensClass.OPMUL, lexema, linha), linha)
                elif(carct == '!'):
                    return (Token.Token(TokensClass.TokensClass.OPNEG, lexema, linha), linha)
                elif(carct == ';'):
                    return (Token.Token(TokensClass.TokensClass.PVIRG, lexema, linha), linha)
                elif(carct == ':'):
                    (carct, linha) = self.getChar(arq, linha)

                    # Verifica se eh o ':' ou ':='
                    if(carct == '='):
                        lexema += carct
                        return (Token.Token(TokensClass.TokensClass.ATRIB, lexema, linha), linha)
                    else:
                        self.ungetChar(carct)
                        return (Token.Token(TokensClass.TokensClass.DPONTOS, lexema, linha), linha)
                elif(carct == ','):
                    return (Token.Token(TokensClass.TokensClass.VIRG, lexema, linha), linha)
                elif(carct == '('):
                    return (Token.Token(TokensClass.TokensClass.ABREPAR, lexema, linha), linha)
                elif(carct == ')'):
                    return (Token.Token(TokensClass.TokensClass.FECHAPAR, lexema, linha), linha)
                elif(carct == '{'):
                    return (Token.Token(TokensClass.TokensClass.ABRECH, lexema, linha), linha)
                elif(carct == '}'):
                    return (Token.Token(TokensClass.TokensClass.FECHACH, lexema, linha), linha)

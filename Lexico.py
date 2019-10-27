# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.:  
# ------------------------------------------------ #
#

import Token
import Archive
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
        'VERDADEIRO': TokensClass.TokensClass.VERDADEIRO,
    }
    
    # Construtor
    def __init__(self, nomeArquivo):
        self.buffer = ''
        self.arquivo = Archive.Archive(nomeArquivo)
    
    def getChar(self, arq):
        carct = None

        if(not(arq is None)):
            # Pega um caracter ja no buffer
            if(len(self.buffer) > 0):
                carct = self.buffer[0]
                self.buffer = self.buffer[1:]
            else:
                # Quando o buffer nao tem mais informacoes, busca do arquivo fonte
                carct = arq.read(1)
            
        return carct

    def ungetChar(self, carct):
        if(not (carct is None)):
            self.buffer += carct
    
    def getToken(self, arq):
        lexema = ''
        carct = None
        estado = 1

        while(True):
            if(estado == 1): # Estado de identificacao do caracter
                carct = self.getChar(arq)

                if((carct is None) or (carct == '')):
                    return Token.Token(TokensClass.TokensClass.FIMARQ, '$')
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
                    return Token.Token(TokensClass.TokensClass.ERROR, '<'+ carct +'>')
            elif(estado == 2): # Estado para tratar identificadores e palavras reservadas
                lexema += carct
                carct = self.getChar(arq)

                # Verifica se a palavra terminou
                if((carct is None) or (not(carct.isalnum()))):
                    self.ungetChar(carct)

                    if(lexema in self.reservadas):
                        return Token.Token(self.reservadas[lexema], lexema)
                    else:
                        # ID validos devem possuir no max, 32 caracters
                        if(len(lexema) <= 32):
                            return Token.Token(TokensClass.TokensClass.ID, lexema)
                        else:
                            return Token.Token(TokensClass.TokensClass.ERROR, lexema)
            elif(estado == 3): # Estado para tratar constantes numericas inteiras e reais
                lexema += carct
                carct = self.getChar(arq)

                # Verifica se a constante numerica terminou
                if((carct is None) or (not(carct.isdigit()) and not(carct == '.'))):
                    self.ungetChar(carct)
                    return Token.Token(TokensClass.TokensClass.CTE, lexema)
            elif(estado == 4): # Estado para tratar cadeia de caracter entre ""
                lexema += carct
                carct = self.getChar(arq)

                if((carct is None) or (carct == ')')):
                    return Token.Token(TokensClass.TokensClass.CADEIA, lexema)
            elif(estado == 5): # Estado para tratar outros tokens primitivos
                lexema += carct
                
                if(carct == '='):
                    return Token.Token(TokensClass.OPREL, lexema)
                elif(carct == '<'):
                    carct = self.getChar(arq)

                    # Verifica se eh o '<', '<=' ou '<>'
                    if(carct == '='):
                        lexema += carct
                        return Token.Token(TokensClass.TokensClass.OPREL, lexema)
                    elif(carct == '>'):
                        lexema += carct
                        return Token.Token(TokensClass.TokensClass.OPREL, lexema)
                    else:
                        self.ungetChar(carct)
                        return Token.Token(TokensClass.TokensClass.OPREL, lexema)
                elif(carct == '>'):
                    carct = self.getChar(arq)

                    # Verifica se eh o '>' ou '>='
                    if(carct == '='):
                        lexema += carct
                        return Token.Token(TokensClass.TokensClass.OPREL, lexema)
                    else:
                        self.ungetChar(carct)
                        return Token.Token(TokensClass.TokensClass.OPREL, lexema)
                elif(carct == '+'):
                    return Token.Token(TokensClass.TokensClass.OPAD, lexema)
                elif(carct == '-'):
                    return Token.Token(TokensClass.TokensClass.OPAD, lexema)
                elif(carct == '*'):
                    return Token.Token(TokensClass.TokensClass.OPMUL, lexema)
                elif(carct == '/'):
                    carct = self.getChar(arq)

                    # Verifica se eh o '/' ou '//'
                    if(carct == '/'): # Para tratar comentarios
                        while(not(carct is None) and (carct != '\n')):
                            carct = self.getChar(arq)
                        
                        lexema = ''
                        estado = 1
                    else:
                        self.ungetChar(carct)
                        return Token.Token(TokensClass.TokensClass.OPMUL, lexema)
                elif(carct == '!'):
                    return Token.Token(TokensClass.TokensClass.OPNEG, lexema)
                elif(carct == ';'):
                    return Token.Token(TokensClass.TokensClass.PVIRG, lexema)
                elif(carct == ':'):
                    carct = self.getChar(arq)

                    # Verifica se eh o ':' ou ':='
                    if(carct == '='):
                        lexema += carct
                        return Token.Token(TokensClass.TokensClass.ATRIB, lexema)
                    else:
                        self.ungetChar(carct)
                        return Token.Token(TokensClass.TokensClass.DPONTOS, lexema)
                elif(carct == ','):
                    return Token.Token(TokensClass.TokensClass.VIRG, lexema)
                elif(carct == '('):
                    return Token.Token(TokensClass.TokensClass.ABREPAR, lexema)
                elif(carct == ')'):
                    return Token.Token(TokensClass.TokensClass.FECHAPAR, lexema)
                elif(carct == '{'):
                    return Token.Token(TokensClass.TokensClass.ABRECH, lexema)
                elif(carct == '}'):
                    return Token.Token(TokensClass.TokensClass.FECHACH, lexema)

    def analisaArquivo(self):
        listTokens = []
        arq = self.arquivo.abrirArquivo()

        while(True):
            # SE PRECISAR do tokens, criar uma lista que receba no lugar da variavel token e dar return da lista de tokens
            listTokens.append(self.getToken(arq))
            print("token= %s , lexema= (%s)" % (listTokens[len(listTokens)-1].msg, listTokens[len(listTokens)-1].lexema))
            
            if(listTokens[len(listTokens)-1].const == TokensClass.TokensClass.FIMARQ[0]):
                break
        
        arq = self.arquivo.fecharArquivo()
        return listTokens
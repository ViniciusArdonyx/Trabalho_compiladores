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
    
    def getToken(self):
        lexema = ''
        carct = None
        estado = 1
        processa = True

        while processa:
            if(estado == 1):
                carct = self.getChar()

                if(carct is None):
                    return Token.Token(TokensClass.TokensClass.FIMARQ, '$')
                elif(carct in [' ', '\t', '\n']):
                    pass
                elif(carct.isalpha()):
                    estado = 2
                elif(carct.isdigit()):
                    estado = 3
                elif(carct in [':=', '=', '<', '>', '<=', '>=', '<>', '+', '-', '*', '/', '!', ';', ':', ',', '(', ')', '{', '}']):
                    estado = 4
                elif(carct == '//'):
                    estado = 5
                else:
                    return Token.Token(TokensClass.TokensClass.ERROR, '<'+ carct +'>')
            elif(estado == 2):
                continue

    def analisaArquivo(self):
        arq = self.arquivo.abrirArquivo()

        while(True):
            # SE PRECISAR do tokens, criar uma lista que receba no lugar da variavel token e dar return da lista de tokens
            token = self.getToken(arq)
            #print('Token: ')

            # if token.const == TipoToken.FIMARQ[0]:
            #   break
        
        arq = self.arquivo.fecharArquivo()
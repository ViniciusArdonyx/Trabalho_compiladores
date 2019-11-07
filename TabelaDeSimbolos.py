# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.: 0002864 
# ------------------------------------------------ #
#

class TabelaDeSimbolos:

    def __init__(self, nomeArquivo):
        self.arquivoI = None
        self.nome = nomeArquivo

    def criaTabela(self, listaIdent, listaTipo, listaLinha, listaReservadas):
        self.arquivoI = open('./'+self.nome,'w')
        #self.arquivoI = open('./TabelaDeSimbolosIdentificadores.txt', 'w')

        self.arquivoI.write("########################## TABELA DE SIMBOLOS - IDENTIFICADORES ##########################")
        self.arquivoI.write("\n")
        for a in range(0, len(listaIdent)):
            self.arquivoI.write("Identificador: "+str(listaIdent[a]) + "\t\tTipo: " + str(listaTipo[a]) + "\t\tLinha: " +str(listaLinha[a]))
            self.arquivoI.write("\n")

        self.arquivoI.write("##########################################################################################")
        self.arquivoI.write("\n")
        self.arquivoI.write("\n")

        self.arquivoI.write("########################## TABELA DE SIMBOLOS - Reservadas ###############################")
        self.arquivoI.write("\n")
        for i in range(0, len(listaReservadas)):
            self.arquivoI.write("Palavra Reservada: " + str(listaReservadas[i]))
            self.arquivoI.write("\n")

        self.arquivoI.write("##########################################################################################")
        self.arquivoI.write("\n")



        self.arquivoI.close()

    # def criaTabelaReserv(self, listaIdent, listaTipo, listaLinha):
    #     self.arquivoR = open('./TabelaDeSimbolosIdentificadores.txt','w')
    #
    #     self.arquivoR.write("########################## TABELA DE SIMBOLOS - RESERVADAS 33333##########################")
    #     self.arquivoR.write("\n")
    #     for a in range(0, len(listaIdent)):
    #         self.arquivoR.write("Identificador: "+str(listaIdent[a]) + "\t\tTipo: " + str(listaTipo[a]) + "\t\tLinha: " +str(listaLinha[a]))
    #         self.arquivoR.write("\n")
    #
    #     self.arquivoR.write("##########################################################################################")
    #     self.arquivoR.close()
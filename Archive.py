# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.: 0002864 
# ------------------------------------------------ #
#

from os import path

class Archive:

    # Construtor
    def __init__(self, nomeArquivo, fileName):
        self.nomeArquivo = nomeArquivo
        # Arquivo de entrada:
        self.arquivo = None
        # Arquivo de saida, Tabela de simbolos:
        self.arquivoI = None
        self.nome = fileName
    
    def abrirArquivo(self):
        if(not self.arquivo is None):
            print('ERRO: Arquivo aberto.')
            quit()
        elif(path.exists(self.nomeArquivo)):
            self.arquivo = open(self.nomeArquivo, 'r', encoding='latin-1')
        else:
            print('ERRO: Arquivo inexistente.')
            quit()
        
        return self.arquivo
    
    def fecharArquivo(self):
        self.arquivo.close()
        return None

    def criaTabela(self, listaIdent, listaTipo, listaLinha, listaReservadas):
        # Cria arquivo se nao existir, ou abri se existir:
        self.arquivoI = open('./' + self.nome, 'w')
        # Escreve no arquivo:
        self.arquivoI.write("########################## TABELA DE SIMBOLOS - IDENTIFICADORES ##########################")
        self.arquivoI.write("\n")
        for a in range(0, len(listaIdent)):
            # Escreve no arquivo os identificadores, os tipos e as linhas referentes, atraves de cada lista enviada:
            self.arquivoI.write("Identificador: " + str(listaIdent[a]) + "\t\tTipo: " + str(listaTipo[a]) + "\t\tLinha: " + str(listaLinha[a]))
            self.arquivoI.write("\n")
        # Escreve no arquivo:
        self.arquivoI.write("##########################################################################################")
        self.arquivoI.write("\n")
        self.arquivoI.write("\n")
        # Escreve no arquivo:
        self.arquivoI.write("########################## TABELA DE SIMBOLOS - Reservadas ###############################")
        self.arquivoI.write("\n")
        for i in range(0, len(listaReservadas)):
            # Escreve no arquivo cada palavra reservada contada na lista referente:
            self.arquivoI.write("Palavra Reservada: " + str(listaReservadas[i]))
            self.arquivoI.write("\n")
        # Escreve no arquivo:
        self.arquivoI.write("##########################################################################################")
        self.arquivoI.write("\n")
        # Fecha arquivo:
        self.arquivoI.close()
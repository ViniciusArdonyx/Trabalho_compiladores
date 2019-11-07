# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.: 0002864
# ------------------------------------------------ #
#
# Nota:
## Contem a opcao de gerar um arquivo de saida, contendo a tabela de simbolos
## Como Executar(Ex):
##  python3 main.py codigo_fonte.txt
##          ou
##  python3 main.py codigo_fonte.txt –t nomearquivo.txt

import sys
import Archive
import Lexico
import Sintatico

# Realiza os passos de analises (lexica, sintatica, semantica)
def blocoPrincipal(codeFile, fileTable):
    # Para nao printar em um arquivo a tabela de simbolos:
    if fileTable == None:
        lexico = Lexico.Lexico()
        sintatico = Sintatico.Sintatico(lexico, codeFile)
        parser = sintatico.parser()
    # Para printar em um arquivo a tabela de simbolos:
    else:
        lexico = Lexico.Lexico()
        sintatico = Sintatico.Sintatico(lexico, codeFile)
        parser = sintatico.parser()
        tabela = Archive.Archive(None, fileTable)
        listReserv = []
        aux = []
        # Pega as palavras reservadas
        for r in lexico.reservadas:
            aux.append(r.split())
        # Retira da string completa, so o que precisa:
        for i in aux:
            a = len(str(i)) -2
            listReserv.append(str(i)[2:a])
        # Manda criar a tabela:
        tabela.criaTabela(sintatico.listIdent,sintatico.listTipo,sintatico.listLinha, listReserv)

if __name__ == "__main__":
    # Pega todos os parametros informados por linha de comando
    param = sys.argv

    # Mensagem de erro
    msgError = 'ERRO: Parametros informados invalidos.\nEntradas validas:\n\tpython3 main.py codigo_fonte.txt\tpython3 main.py codigo_fonte.txt –t nomearquivo.txt'
    # Se nao quiser printar a tabela de simbolos
    if(len(param) == 2):
        codeFile = param[1]
        blocoPrincipal(codeFile, None)
    # Se quiser printar a tabela de simbolos
    elif(len(param) == 4):
        if(param[2] == '-t'):
            codeFile = param[1]
            fileTable = str(param[3])
            blocoPrincipal(codeFile, fileTable)
        else: # Se nao for o parametro '-t', apresenta a mensagem de erro
            print(msgError)
            exit()
    else:
        print(msgError)

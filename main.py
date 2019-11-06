# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.:  
# ------------------------------------------------ #
#
# Nota:
## Contem a opcao de gerar um arquivo de saida, contendo a tabela de simbolos
## Como Executar(Ex):
##  python3 main.py codigo_fonte.txt
##          ou
##  python3 main.py codigo_fonte.txt –t nomearquivo.txt

import sys
import TabelaDeSimbolos
import Lexico
import Sintatico

# Realiza os passos de analises (lexica, sintatica, semantica)
def blocoPrincipal(codeFile, fileTable):
    if fileTable == None:
        lexico = Lexico.Lexico()
        sintatico = Sintatico.Sintatico(lexico, codeFile)
        parser = sintatico.parser()
    else:
        lexico = Lexico.Lexico()
        sintatico = Sintatico.Sintatico(lexico, codeFile)
        parser = sintatico.parser()
        tabela = TabelaDeSimbolos.TabelaDeSimbolos(fileTable)
        listReserv = []
        aux = []
        for r in lexico.reservadas:
            aux.append(r.split())
        for i in aux:
            a = len(str(i)) -2
            listReserv.append(str(i)[2:a])
        tabela.criaTabela(sintatico.listIdent,sintatico.listTipo,sintatico.listLinha, listReserv)

if __name__ == "__main__":
    # Pega todos os parametros informados por linha de comando
    param = sys.argv

    print(len(param))
    if len(param) == 4:
        codeFile = param[1]
        fileTable = str(param[3])
        blocoPrincipal(codeFile,fileTable)
    elif len(param <=2):
        codeFile = param[1]
        fileTable = None
        blocoPrincipal(codeFile, fileTable)
    else:
        msgError = 'ERRO: Parametros informados invalidos.\nEntradas validas:\n\tpython3 main.py codigo_fonte.txt\tpython3 main.py codigo_fonte.txt –t nomearquivo.txt'
        print(msgError)
    # codeFile = param[0]
    #
    # if(len(param) <= 1):
    #     blocoPrincipal(codeFile)
    # elif len(param > 2):
    #     if (len(param < 4)):
    #         msgError = 'ERRO: Parametros informados invalidos.\nEntradas validas:\n\tpython3 main.py codigo_fonte.txt\tpython3 main.py codigo_fonte.txt –t nomearquivo.txt'
    #
    # else:
    #     msgError = 'ERRO: Parametros informados invalidos.\nEntradas validas:\n\tpython3 main.py codigo_fonte.txt\tpython3 main.py codigo_fonte.txt –t nomearquivo.txt'
    #
    #     if(param[1] == '-t'):
    #         blocoPrincipal(codeFile)
    #         # Tem que gerar o arquivo da tabela de simbolos
    #         pass
    #     else:
    #         print(msgError)
    #         exit()
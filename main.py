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
import Lexico

# Realiza os passos de analises (lexica, sintatica, semantica)
def blocoPrincipal(codeFile):
    lexico = Lexico.Lexico(codeFile)
    listTokens = lexico.analisaArquivo()
    #print(listTokens)

if __name__ == "__main__":
    # Pega todos os parametros informados por linha de comando
    param = sys.argv[1:]
    codeFile = param[0]

    if(len(param) <= 1):
        blocoPrincipal(codeFile)
    else:
        msgError = 'ERRO: Parametros informados invalidos.\nEntradas validas:\n\tpython3 main.py codigo_fonte.txt\tpython3 main.py codigo_fonte.txt –t nomearquivo.txt'

        if(param[1] == '-t'):
            blocoPrincipal(codeFile)
            # Tem que gerar o arquivo da tabela de simbolos
            pass
        else:
            print(msgError)
            exit()
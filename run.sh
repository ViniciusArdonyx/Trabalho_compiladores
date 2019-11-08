#!/bin/bash
# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.: 0002864
# ------------------------------------------------ #
# Entradas validas:
##  python3 main.py codigo_fonte.txt
##          ou
##  python3 main.py codigo_fonte.txt –t nomearquivo.txt

# Para executar sem a criacao da tabela de simbolos
EXE="python3 main.py ./testes-trabalho/exemplo1.txt"

# Para executar com a criacao da tabela de simbolos
#EXE="python3 main.py ./testes-trabalho/exemplo1.txt -t tabela.txt"

# Para executar a bateria de testes
t=45
for i in $(seq 1 $t);
do
    #echo $i
    echo "Arquivo exemplo$i:"
    EXE="python3 main.py ./testes-trabalho/exemplo$i.txt"
    ${EXE}
    echo "\n"
done

#${EXE}
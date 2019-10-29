# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.:  
# ------------------------------------------------ #
#

#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path

class Archive:

    # Construtor
    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
    
    def abrirArquivo(self):
        if(not self.arquivo is None):
            print('ERRO: Arquivo aberto.')
        elif(path.exists(self.nomeArquivo)):
            self.arquivo = open(self.nomeArquivo, 'r', encoding='latin-1')
        else:
            print('ERRO: Arquivo inexistente.')
        
        return self.arquivo
    
    def fecharArquivo(self):
        self.arquivo.close()
        return None
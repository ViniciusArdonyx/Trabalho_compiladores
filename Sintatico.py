# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.:  
# ------------------------------------------------ #
#

#!/usr/bin/python
# -*- coding: utf-8 -*-

import Token
import Lexico
import Archive
import TokensClass

class Sintatico:

    # Construtor
    def __init__(self, lexico, nomeArquivo):
        self.linha = 1
        self.tokenAtual = None
        self.analisadorLexico = lexico
        self.tokenList = TokensClass.TokensClass()
        self.arquivo = Archive.Archive(nomeArquivo)

    def consume(self, token):
        # verifico se o token que estou lendo é igual ao token esperado:
        if token == self.tokenAtual.tipo:
            (self.tokenAtual, self.linha) = self.analisadorLexico.getToken(self.arquivo.arquivo, self.linha)
        else:
            print("[SINTATICO] Erro na linha: " + str(self.tokenAtual.linha) + "\nEra esperado: ('" + str(token[1]) +
                  "') mas veio: ('"+ str(self.tokenAtual.msg) + "').")
            quit()

    def parser(self):
        self.arquivo.arquivo = self.arquivo.abrirArquivo()

        (self.tokenAtual, self.linha) = self.analisadorLexico.getToken(self.arquivo.arquivo, self.linha)
        #print(self.tokenAtual)
        self.a()

        self.arquivo.arquivo = self.arquivo.fecharArquivo()

    def a(self):
        self.prog()
        self.consume(self.tokenList.FIMARQ)

    def prog(self):
        self.consume(self.tokenList.PROGRAMA)
        self.consume(self.tokenList.ID)
        self.consume(self.tokenList.PVIRG)
        self.decls()
        self.c_comp()

    def decls(self):
        if self.tokenAtual.tipo == self.tokenList.VARIAVEIS:
            self.consume(self.tokenList.VARIAVEIS)
            self.list_decls()
        else:
            pass # vazio

    def list_decls(self):
        self.decl_tipo()
        self.d()

    def decl_tipo(self):
        self.list_id()
        self.consume(self.tokenList.DPONTOS)
        self.tipo()
        self.consume(self.tokenList.PVIRG)

    def list_id(self):
        self.consume(self.tokenList.ID)
        self.e()

    def e(self):
        if self.tokenAtual.tipo == self.tokenList.VIRG:
            self.consume(self.tokenList.VIRG)
            self.list_id()
        else:
            pass

    def tipo(self):
        if self.tokenAtual.tipo == self.tokenList.INTEIRO:
            self.consume(self.tokenList.INTEIRO)
        elif self.tokenAtual.tipo == self.tokenList.REAL:
            self.consume(self.tokenList.REAL)
        elif self.tokenAtual.tipo == self.tokenList.LOGICO:
            self.consume(self.tokenList.LOGICO)
        else:
            self.consume(self.tokenList.CARACTER)

    def d(self):
        if self.tokenAtual.tipo == self.tokenList.ID:
            self.list_decls()
        else:
            pass

    def c_comp(self):
        self.consume(self.tokenList.ABRECH)
        self.lista_comandos()
        self.consume(self.tokenList.FECHACH)

    def lista_comandos(self):
        self.comandos()
        self.g()

    def comandos(self):
        if self.tokenAtual.tipo == self.tokenList.SE:
            self._if()
        elif self.tokenAtual.tipo == self.tokenList.ENQUANTO:
            self._while()
        elif self.tokenAtual.tipo == self.tokenList.LEIA:
            self._read()
        elif self.tokenAtual.tipo == self.tokenList.ESCREVA:
            self._write()
        else:
            self.atrib()

    def _if(self):
        self.consume(self.tokenList.SE)
        self.consume(self.tokenList.ABREPAR)
        self.expr()
        self.consume(self.tokenList.FECHAPAR)
        self.c_comp()
        self.h()

    def expr(self):
        self.simples()
        self.p()

    def simples(self):
        self.termo()
        self.r()

    def termo(self):
        self.fat()
        self.s()

    def fat(self):
        if self.tokenAtual.tipo == self.tokenList.ID:
            self.consume(self.tokenList.ID)
        elif self.tokenAtual.tipo == self.tokenList.CTE:
            self.consume(self.tokenList.CTE)
        elif self.tokenAtual.tipo == self.tokenList.ABREPAR:
            self.consume(self.tokenList.ABREPAR)
            self.expr()
            self.consume(self.tokenList.FECHAPAR)
        elif self.tokenAtual.tipo == self.tokenList.VERDADEIRO:
            self.consume(self.tokenList.VERDADEIRO)
        elif self.tokenAtual.tipo == self.tokenList.FALSO:
            self.consume(self.tokenList.FALSO)
        else:
            self.consume(self.tokenList.OPNEG)
            self.fat()

    def s(self):
        if self.tokenAtual.tipo == self.tokenList.OPMUL:
            self.consume(self.tokenList.OPMUL)
            self.termo()
        else:
            pass

    def r(self):
        if self.tokenAtual.tipo == self.tokenList.OPAD:
            self.consume(self.tokenList.OPAD)
            self.simples()
        else:
            pass

    def p(self):
        if self.tokenAtual.tipo == self.tokenList.OPREL:
            self.consume(self.tokenList.OPREL)
            self.simples()
        else:
            pass

    def h(self):
        if self.tokenAtual.tipo == self.tokenList.SENAO:
            self.consume(self.tokenList.SENAO)
            self.c_comp()
        else:
            pass

    def _while(self):
        self.consume(self.tokenList.ENQUANTO)
        self.consume(self.tokenList.ABREPAR)
        self.expr()
        self.consume(self.tokenList.FECHAPAR)
        self.c_comp()

    def _read(self):
        self.consume(self.tokenList.LEIA)
        self.consume(self.tokenList.ABREPAR)
        self.list_id()
        self.consume(self.tokenList.FECHAPAR)
        self.consume(self.tokenList.PVIRG)

    def _write(self):
        self.consume(self.tokenList.ESCREVA)
        self.consume(self.tokenList.ABREPAR)
        self.list_w()
        self.consume(self.tokenList.FECHAPAR)
        self.consume(self.tokenList.PVIRG)

    def list_w(self):
        self.elem_w()
        self.l()

    def elem_w(self):
        if self.tokenAtual.tipo == self.tokenList.CADEIA:
            self.consume(self.tokenList.CADEIA)
        else:
            self.expr()

    def l(self):
        if self.tokenAtual.tipo == self.tokenList.VIRG:
            self.consume(self.tokenList.VIRG)
            self.list_w()
        else:
            pass

    def atrib(self):
        self.consume(self.tokenList.ID)
        self.consume(self.tokenList.ATRIB)
        self.expr()
        self.consume(self.tokenList.PVIRG)

    def g(self):
        if self.tokenAtual.tipo == self.tokenList.SE or self.tokenAtual.tipo == self.tokenList.ENQUANTO or self.tokenAtual.tipo == self.tokenList.LEIA or self.tokenAtual.tipo == self.tokenList.ESCREVA or self.tokenAtual.tipo == self.tokenList.ID:
            self.lista_comandos()
        else:
            pass
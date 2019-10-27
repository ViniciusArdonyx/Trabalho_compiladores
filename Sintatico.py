# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.:  
# ------------------------------------------------ #
#

from pip._internal.utils.misc import consume

import Token
import TokensClass
import Lexico

class Sintatico:
    # teste 3
    def __init__(self):
        self.analisadorLexico = Lexico.Lexico
        self.tokenAtual = None
        self.tokenList = TokensClass.TokensClass

    def consume(self, token):
        # verifico se o token que estou lendo é igual ao token esperado:
        if token == self.tokenAtual:
            self.tokenAtual = self.analisadorLexico.getToken();
        else:
            print("SINTATICO] Erro na linha: " + "LINHA COLOCAR" + "\nEra esperado: " + str(token) +
                  " mas veio: "+ str(self.tokenAtual) + ".")

    def parser(self):
        self.tokenAtual = self.analisadorLexico.getToken()
        self.a()


    def a(self):
        self.prog();
        self.consume(self.tokenList.FIMARQ);

    def prog(self):
        self.consume(self.tokenList.PROGRAMA)
        self.consume(self.tokenList.ID)
        self.consume(self.tokenList.PVIRG)
        self.decls()
        self.c_comp()

    def decls(self):
        if self.tokenAtual == self.tokenList.VARIAVEIS:
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
        if self.tokenAtual == self.tokenList.VIRG:
            self.consume(self.tokenList.VIRG)
            self.list_id()
        else:
            pass

    def tipo(self):
        if self.tokenAtual == self.tokenList.INTEIRO:
            self.consume(self.tokenList.INTEIRO)
        elif self.tokenAtual == self.tokenList.REAL:
            self.consume(self.tokenList.REAL)
        elif self.tokenAtual == self.tokenList.LOGICO:
            self.consume(self.tokenList.LOGICO)
        else:
            self.consume(self.tokenList.CARACTER)

    def d(self):
        if self.tokenAtual == self.tokenList.ID:
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
        if self.tokenAtual == self.tokenList.SE:
            self._if()
        elif self.tokenAtual == self.tokenList.ENQUANTO:
            self._while()
        elif self.tokenAtual == self.tokenList.LEIA:
            self._read()
        elif self.tokenAtual == self.tokenList.ESCREVA:
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
        if self.tokenAtual == self.tokenList.ID:
            self.consume(self.tokenList.ID)
        elif self.tokenAtual == self.tokenList.CTE:
            self.consume(self.tokenList.CTE)
        elif self.tokenAtual == self.tokenList.ABREPAR:
            self.consume(self.tokenList.ABREPAR)
            self.expr()
            self.consume(self.tokenList.FECHAPAR)
        elif self.tokenAtual == self.tokenList.VERDADEIRO:
            self.consume(self.tokenList.VERDADEIRO)
        elif self.tokenAtual == self.tokenList.FALSO:
            self.consume(self.tokenList.FALSO)
        else:
            self.consume(self.tokenList.OPNEG)
            self.fat()

    def s(self):
        if self.tokenAtual == self.tokenList.OPMUL:
            self.consume(self.tokenList.OPMUL)
            self.termo()
        else:
            pass

    def r(self):
        if self.tokenAtual == self.tokenList.OPAD:
            self.consume(self.tokenList.OPAD)
            self.simples()
        else:
            pass

    def p(self):
        if self.tokenAtual == self.tokenList.OPREL:
            self.consume(self.tokenList.OPREL)
            self.simples()
        else:
            pass

    def h(self):
        if self.tokenAtual == self.tokenList.SENAO:
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
        if self.tokenAtual == self.tokenList.CADEIA:
            self.consume(self.tokenList.CADEIA)
        else:
            self.expr()

    def l(self):
        if self.tokenAtual == self.tokenList.VIRG:
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
        if self.tokenAtual == self.tokenList.SE or self.tokenAtual == self.tokenList.ENQUANTO or self.tokenAtual == self.tokenList.LEIA or self.tokenAtual == self.tokenList.ESCREVA or self.tokenAtual == self.tokenList.ID:
            self.lista_comandos()
        else:
            pass
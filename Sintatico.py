# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.: 0002864
# ------------------------------------------------ #
#

import Token
import Lexico
import Archive
import TokensClass

class Sintatico:
    """
    FRIST = {
        'a': 'PROGRAMA'
        'prog': 'PROGRAMA'
        'decls': 'VARIAVEIS'
        'list_decls': 'ident'
        'decl_tipo': 'ident'
        'list_id': 'ident'
        'e': ','
        'tipo': 'CARACTER INTEIRO LOGICO REAL'
        'd': 'ident'
        'c_comp': '{'
        'lista_comandos': 'ident ENQUANTO ESCREVA LEIA SE'
        'comandos': 'ident ENQUANTO ESCREVA LEIA SE'
        '_if': 'SE'
        'expr': 'ident ( const FALSO ! VERDADEIRO'
        'simples': 'ident ( const FALSO ! VERDADEIRO'
        'termo': 'ident ( const FALSO ! VERDADEIRO'
        'fat': 'ident ( const FALSO ! VERDADEIRO'
        's': '* /'
        'r': '+ -'
        'p': '= < > <= >= <>'
        'h': 'SENAO'
        '_while': 'ENQUANTO'
        '_read': 'LEIA'
        '_write': 'ESCREVA'
        'list_w': 'cad ident ( const FALSO ! VERDADEIRO'
        'elem_w': 'cad ident ( const FALSO ! VERDADEIRO'
        'l': ','
        'atrib': 'ident'
        'g': 'ident ENQUANTO ESCREVA LEIA SE'
    }"""

    FOLLOW = {
        'a': 'eof',
        'prog': 'eof',
        'decls': 'eof {',
        'list_decls': 'eof { ident',
        'decl_tipo': 'eof {',
        'list_id': 'eof : )',
        'e': 'eof : )',
        'tipo': 'eof',
        'd': 'eof {',
        'c_comp': 'eof ident ENQUANTO ESCREVA } LEIA SE SENAO',
        'lista_comandos': 'eof }',
        'comandos': 'eof ident ENQUANTO ESCREVA } LEIA SE',
        '_if': 'eof ident ENQUANTO ESCREVA } LEIA SE',
        'expr': 'eof ) ; ,',
        'simples': 'eof ) ; , = < > <= >= <>',
        'termo': 'eof ) ; , = < > <= >= <> + -',
        'fat': 'eof + - * /',
        's': 'eof ) ; , = < > <= >= <> + -',
        'r': 'eof ) ; , = < > <= >= <>',
        'p': 'eof ) ; ,',
        'h': 'eof ident ENQUANTO ESCREVA } LEIA SE',
        '_while': 'eof ident ENQUANTO ESCREVA } LEIA SE',
        '_read': 'eof ident ENQUANTO ESCREVA } LEIA SE',
        '_write': 'eof ident ENQUANTO ESCREVA } LEIA SE',
        'list_w': 'eof )',
        'elem_w': 'eof ) ,',
        'l': 'eof )',
        'atrib': 'eof ident ENQUANTO ESCREVA } LEIA SE',
        'g': 'eof }'
    }

    # Construtor
    def __init__(self, lexico, nomeArquivo):
        self.linha = 1
        self.tokenAtual = None
        self.analisadorLexico = lexico
        self.tokenList = TokensClass.TokensClass()
        self.arquivo = Archive.Archive(nomeArquivo, None)
        self.listIdent = []
        self.listTipo = []
        self.listLinha = []
        self.cont = 0
        self.tipoAnterior = None


    def consume(self, token, lfollow):
        if token == self.tokenAtual.tipo:
            if self.tokenAtual.tipo == self.tokenList.PROGRAMA:
                self.tipoAnterior = 'PROGRAMA'

            (self.tokenAtual, self.linha) = self.analisadorLexico.getToken(self.arquivo.arquivo, self.linha)

            if ((self.tokenAtual.tipo == self.tokenList.PVIRG and self.tipoAnterior == 'PROGRAMA') or
                (self.tokenAtual.tipo == self.tokenList.VARIAVEIS and self.tipoAnterior == 'PROGRAMA') or
                (self.tokenAtual.tipo == self.tokenList.ABRECH and self.tipoAnterior == 'PROGRAMA') or
                (self.tokenAtual.tipo == self.tokenList.INTEIRO and self.tipoAnterior == 'PROGRAMA') or
                (self.tokenAtual.tipo == self.tokenList.REAL and self.tipoAnterior == 'PROGRAMA') or
                (self.tokenAtual.tipo == self.tokenList.CARACTER and self.tipoAnterior == 'PROGRAMA') or
                (self.tokenAtual.tipo == self.tokenList.LOGICO and self.tipoAnterior == 'PROGRAMA')):
                self.listTipo.append('PROGRAMA')
                self.listIdent.append('None')
                self.listLinha.append(self.tokenAtual.linha)
                self.tipoAnterior = None

            if self.tokenAtual.tipo == self.tokenList.ID and self.tipoAnterior == 'PROGRAMA':
                self.listTipo.append('PROGRAMA')
                self.listIdent.append(self.tokenAtual.lexema)
                self.listLinha.append(self.tokenAtual.linha)
                self.tipoAnterior = None

            if self.tokenAtual.tipo == self.tokenList.ID:
                if (self.tokenAtual.lexema not in self.listIdent):
                    self.cont += 1
                    self.listIdent.append(self.tokenAtual.lexema)
                    self.listLinha.append(self.tokenAtual.linha)
            elif self.cont != 0 and self.tokenAtual.tipo == self.tokenList.PVIRG:
                while self.cont != 0:
                    self.listTipo.append('None')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            elif (self.tokenAtual.msg == 'INTEIRO'):
                while self.cont != 0:
                    self.listTipo.append('INTEIRO')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            elif (self.tokenAtual.msg == 'REAL'):
                while self.cont != 0:
                    self.listTipo.append('REAL')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            elif (self.tokenAtual.msg == 'LOGICO'):
                while self.cont != 0:
                    self.listTipo.append('LOGICO')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            elif (self.tokenAtual.msg == 'CARACTER'):
                while self.cont != 0:
                    self.listTipo.append('CARACTER')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            elif self.tokenAtual.tipo == self.tokenList.DPONTOS:
                pass;
            elif self.tokenAtual.tipo == self.tokenList.VIRG:
                pass
            else:
                while self.cont != 0:
                    self.listTipo.append('None')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0

        else:
            print("[SINTATICO] Erro na linha: " + str(self.tokenAtual.linha) + "\nEra esperado: ('" + str(token[1]) +
                "') mas veio: ('"+ str(self.tokenAtual.msg) + "').")
            
            # Panico
            while(not(self.tokenAtual.msg in lfollow)):
                (self.tokenAtual, self.linha) = self.analisadorLexico.getToken(self.arquivo.arquivo, self.linha)
            
            # Se o token foi o final de arquivo, termina a execucao para nao estourar a pilha
            if(self.tokenAtual.msg == 'eof'):
                quit()

    def parser(self):
        self.arquivo.arquivo = self.arquivo.abrirArquivo()

        (self.tokenAtual, self.linha) = self.analisadorLexico.getToken(self.arquivo.arquivo, self.linha)
        self.a()

        self.arquivo.arquivo = self.arquivo.fecharArquivo()

    def a(self):
        self.prog()
        self.consume(self.tokenList.FIMARQ, self.FOLLOW['a'].split())

    def prog(self):
        self.consume(self.tokenList.PROGRAMA, self.FOLLOW['prog'].split())
        self.consume(self.tokenList.ID, self.FOLLOW['prog'].split())
        self.consume(self.tokenList.PVIRG, self.FOLLOW['prog'].split())
        self.decls()
        self.c_comp()

    def decls(self):
        if self.tokenAtual.tipo == self.tokenList.VARIAVEIS:
            self.consume(self.tokenList.VARIAVEIS, self.FOLLOW['decls'].split())
            self.list_decls()
        else:
            pass # vazio

    def list_decls(self):
        self.decl_tipo()
        self.d()

    def decl_tipo(self):
        self.list_id()
        self.consume(self.tokenList.DPONTOS, self.FOLLOW['decl_tipo'].split())
        self.tipo()
        self.consume(self.tokenList.PVIRG, self.FOLLOW['decl_tipo'].split())

    def list_id(self):
        self.consume(self.tokenList.ID, self.FOLLOW['list_id'].split())
        self.e()

    def e(self):
        if self.tokenAtual.tipo == self.tokenList.VIRG:
            self.consume(self.tokenList.VIRG, self.FOLLOW['e'].split())
            self.list_id()
        else:
            pass

    def tipo(self):
        if self.tokenAtual.tipo == self.tokenList.INTEIRO:
            self.consume(self.tokenList.INTEIRO, self.FOLLOW['tipo'].split())
        elif self.tokenAtual.tipo == self.tokenList.REAL:
            self.consume(self.tokenList.REAL, self.FOLLOW['tipo'].split())
        elif self.tokenAtual.tipo == self.tokenList.LOGICO:
            self.consume(self.tokenList.LOGICO, self.FOLLOW['tipo'].split())
        else:
            self.consume(self.tokenList.CARACTER, self.FOLLOW['tipo'].split())

    def d(self):
        if self.tokenAtual.tipo == self.tokenList.ID:
            self.list_decls()
        else:
            pass

    def c_comp(self):
        self.consume(self.tokenList.ABRECH, self.FOLLOW['c_comp'].split())
        self.lista_comandos()
        self.consume(self.tokenList.FECHACH, self.FOLLOW['c_comp'].split())

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
        self.consume(self.tokenList.SE, self.FOLLOW['_if'].split())
        self.consume(self.tokenList.ABREPAR, self.FOLLOW['_if'].split())
        self.expr()
        self.consume(self.tokenList.FECHAPAR, self.FOLLOW['_if'].split())
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
            self.consume(self.tokenList.ID, self.FOLLOW['fat'].split())
        elif self.tokenAtual.tipo == self.tokenList.CTE:
            self.consume(self.tokenList.CTE, self.FOLLOW['fat'].split())
        elif self.tokenAtual.tipo == self.tokenList.ABREPAR:
            self.consume(self.tokenList.ABREPAR, self.FOLLOW['fat'].split())
            self.expr()
            self.consume(self.tokenList.FECHAPAR, self.FOLLOW['fat'].split())
        elif self.tokenAtual.tipo == self.tokenList.VERDADEIRO:
            self.consume(self.tokenList.VERDADEIRO, self.FOLLOW['fat'].split())
        elif self.tokenAtual.tipo == self.tokenList.FALSO:
            self.consume(self.tokenList.FALSO, self.FOLLOW['fat'].split())
        else:
            self.consume(self.tokenList.OPNEG, self.FOLLOW['fat'].split())
            self.fat()

    def s(self):
        if self.tokenAtual.tipo == self.tokenList.OPMUL:
            self.consume(self.tokenList.OPMUL, self.FOLLOW['s'].split())
            self.termo()
        else:
            pass

    def r(self):
        if self.tokenAtual.tipo == self.tokenList.OPAD:
            self.consume(self.tokenList.OPAD, self.FOLLOW['r'].split())
            self.simples()
        else:
            pass

    def p(self):
        if self.tokenAtual.tipo == self.tokenList.OPREL:
            self.consume(self.tokenList.OPREL, self.FOLLOW['p'].split())
            self.simples()
        else:
            pass

    def h(self):
        if self.tokenAtual.tipo == self.tokenList.SENAO:
            self.consume(self.tokenList.SENAO, self.FOLLOW['h'].split())
            self.c_comp()
        else:
            pass

    def _while(self):
        self.consume(self.tokenList.ENQUANTO, self.FOLLOW['_while'].split())
        self.consume(self.tokenList.ABREPAR, self.FOLLOW['_while'].split())
        self.expr()
        self.consume(self.tokenList.FECHAPAR, self.FOLLOW['_while'].split())
        self.c_comp()

    def _read(self):
        self.consume(self.tokenList.LEIA, self.FOLLOW['_read'].split())
        self.consume(self.tokenList.ABREPAR, self.FOLLOW['_read'].split())
        self.list_id()
        self.consume(self.tokenList.FECHAPAR, self.FOLLOW['_read'].split())
        self.consume(self.tokenList.PVIRG, self.FOLLOW['_read'].split())

    def _write(self):
        self.consume(self.tokenList.ESCREVA, self.FOLLOW['_write'].split())
        self.consume(self.tokenList.ABREPAR, self.FOLLOW['_write'].split())
        self.list_w()
        self.consume(self.tokenList.FECHAPAR, self.FOLLOW['_write'].split())
        self.consume(self.tokenList.PVIRG, self.FOLLOW['_write'].split())

    def list_w(self):
        self.elem_w()
        self.l()

    def elem_w(self):
        if self.tokenAtual.tipo == self.tokenList.CADEIA:
            self.consume(self.tokenList.CADEIA, self.FOLLOW['elem_w'].split())
        else:
            self.expr()

    def l(self):
        if self.tokenAtual.tipo == self.tokenList.VIRG:
            self.consume(self.tokenList.VIRG, self.FOLLOW['l'].split())
            self.list_w()
        else:
            pass

    def atrib(self):
        self.consume(self.tokenList.ID, self.FOLLOW['atrib'].split())
        self.consume(self.tokenList.ATRIB, self.FOLLOW['atrib'].split())
        self.expr()
        self.consume(self.tokenList.PVIRG, self.FOLLOW['atrib'].split())

    def g(self):
        if self.tokenAtual.tipo == self.tokenList.SE or self.tokenAtual.tipo == self.tokenList.ENQUANTO or self.tokenAtual.tipo == self.tokenList.LEIA or self.tokenAtual.tipo == self.tokenList.ESCREVA or self.tokenAtual.tipo == self.tokenList.ID:
            self.lista_comandos()
        else:
            pass
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
        'tipo': 'eof ;',
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
        '_read': 'eof ident ENQUANTO ESCREVA } LEIA SE )',
        '_write': 'eof ident ENQUANTO ESCREVA } LEIA SE )',
        'list_w': 'eof )',
        'elem_w': 'eof ) ,',
        'l': 'eof )',
        'atrib': 'eof ident ENQUANTO ESCREVA } LEIA SE',
        'g': 'eof }'
    }

    # Construtor do analisador sintatico
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

    # Função consume, utilizada para ferificação dos token para consumo:
    def consume(self, token, lfollow):
        # verifca se o token passado é igual ao token atual:
        if token == self.tokenAtual.tipo:
            # Pega os simbolos para montagem da tabela de simbolos:
            if self.tokenAtual.tipo == self.tokenList.PROGRAMA:
                self.tipoAnterior = 'PROGRAMA'

            (self.tokenAtual, self.linha) = self.analisadorLexico.getToken(self.arquivo.arquivo, self.linha)
            # Pega os simbolos para montagem da tabela de simbolos:
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
            # Pega os simbolos para montagem da tabela de simbolos:]
            # Pega o identificador que da nome ao progrmama:
            if self.tokenAtual.tipo == self.tokenList.ID and self.tipoAnterior == 'PROGRAMA':
                self.listTipo.append('PROGRAMA')
                self.listIdent.append(self.tokenAtual.lexema)
                self.listLinha.append(self.tokenAtual.linha)
                self.tipoAnterior = None
            # Pega os simbolos para montagem da tabela de simbolos:
            # Caso encontre algum identificador ( variavel) adiciona ele na tabela de ident, e usa um contatador para
            # saber quantas variaveis foram adicionadas:
            if self.tokenAtual.tipo == self.tokenList.ID:
                if (self.tokenAtual.lexema not in self.listIdent):
                    self.cont += 1
                    self.listIdent.append(self.tokenAtual.lexema)
                    self.listLinha.append(self.tokenAtual.linha)
            # Pega os simbolos para montagem da tabela de simbolos:
            # Caso nao encontre nenhuma palavra reservada e foram adicionados identificadores na tabela de ident
            # adiciona na tabela de tipos "None":
            elif self.cont != 0 and self.tokenAtual.tipo == self.tokenList.PVIRG:
                while self.cont != 0:
                    self.listTipo.append('None')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            # Pega os simbolos para montagem da tabela de simbolos:
            # Verifica o tipo do ident, e adiciona o numero de vezes que foi contabilizada cont:
            elif (self.tokenAtual.msg == 'INTEIRO'):
                while self.cont != 0:
                    self.listTipo.append('INTEIRO')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            # Pega os simbolos para montagem da tabela de simbolos:
            # Verifica o tipo do ident, e adiciona o numero de vezes que foi contabilizada cont:
            elif (self.tokenAtual.msg == 'REAL'):
                while self.cont != 0:
                    self.listTipo.append('REAL')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            # Pega os simbolos para montagem da tabela de simbolos:
            # Verifica o tipo do ident, e adiciona o numero de vezes que foi contabilizada cont:
            elif (self.tokenAtual.msg == 'LOGICO'):
                while self.cont != 0:
                    self.listTipo.append('LOGICO')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            # Pega os simbolos para montagem da tabela de simbolos:
            # Verifica o tipo do ident, e adiciona o numero de vezes que foi contabilizada cont:
            elif (self.tokenAtual.msg == 'CARACTER'):
                while self.cont != 0:
                    self.listTipo.append('CARACTER')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0
            # Pega os simbolos para montagem da tabela de simbolos:
            # Para evitar erros, ignorar caractere:
            elif self.tokenAtual.tipo == self.tokenList.DPONTOS:
                pass
            # Pega os simbolos para montagem da tabela de simbolos:
            # Para evitar erros, ignorar caractere:
            elif self.tokenAtual.tipo == self.tokenList.VIRG:
                pass
            # Pega os simbolos para montagem da tabela de simbolos:
            # Caso adicionou algum identificador (variavel)  e nao identificou tipo, adiciona "None":
            else:
                while self.cont != 0:
                    self.listTipo.append('None')
                    self.listLinha.append(self.tokenAtual.linha)
                    self.cont -= 1
                self.cont = 0

        else:
            print("[SINTATICO] Erro na linha: " + str(self.tokenAtual.linha) + "\nEra esperado: ('" + str(token[1]) +
                "') mas veio: ('"+ str(self.tokenAtual.msg) + "').")
            
            # Metodo do Panico, com uso da tabela de follow:
            while(not(self.tokenAtual.msg in lfollow)):
                (self.tokenAtual, self.linha) = self.analisadorLexico.getToken(self.arquivo.arquivo, self.linha)
            
            # Se o token foi o final de arquivo, termina a execucao para nao estourar a pilha
            if(self.tokenAtual.msg == 'eof'):
                quit()

    def parser(self):
        # Inicializa o arquivo:
        self.arquivo.arquivo = self.arquivo.abrirArquivo()
        # Pega o primeiro token:
        (self.tokenAtual, self.linha) = self.analisadorLexico.getToken(self.arquivo.arquivo, self.linha)
        # Inicia a produção:
        self.a()
        # Fechamento do arquivo:
        self.arquivo.arquivo = self.arquivo.fecharArquivo()

    # Regra de Produção: A -> PROG $
    def a(self):
        # Chama a funcao prog:
        self.prog()
        # Consome fim de arquivo, com envio de follows:
        self.consume(self.tokenList.FIMARQ, self.FOLLOW['a'].split())
    # PROG -> programa id pvirg DECLS C-COMP
    def prog(self):
        # Consome programa, com envio de follows:
        self.consume(self.tokenList.PROGRAMA, self.FOLLOW['prog'].split())
        # Consome identificador, com envio de follows:
        self.consume(self.tokenList.ID, self.FOLLOW['prog'].split())
        # Consome ponto e virgula, com envio de follows:
        self.consume(self.tokenList.PVIRG, self.FOLLOW['prog'].split())
        # Chama a funcao decls:
        self.decls()
        # Chama a funcao c_comp:
        self.c_comp()
    # DECLS -> vazio OU variaveis LIST-DECLS
    def decls(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.VARIAVEIS:
            # Consome variaveis, com envio de follows:
            self.consume(self.tokenList.VARIAVEIS, self.FOLLOW['decls'].split())
            # Chama a funcao list_decls
            self.list_decls()
        else:
            # Se vazio so passa:
            pass # vazio
    # LIST-DECLS -> DECL-TIPO D
    def list_decls(self):
        # Chama a funcao decl_tipo:
        self.decl_tipo()
        # Chama a funcao d:
        self.d()
    # DECL-TIPO -> LIST-ID dpontos TIPO pvirg
    def decl_tipo(self):
        # Chama a funcao list_id:
        self.list_id()
        # Consome dois pontos, com envio de follows:
        self.consume(self.tokenList.DPONTOS, self.FOLLOW['decl_tipo'].split())
        # Chama a funcao tipo:
        self.tipo()
        # Consome ponto e virgula, com envio de follows:
        self.consume(self.tokenList.PVIRG, self.FOLLOW['decl_tipo'].split())
    # LIST-ID -> id E
    def list_id(self):
        # Consome identificador, com envio de follows:
        self.consume(self.tokenList.ID, self.FOLLOW['list_id'].split())
        # Chama a funcao e:
        self.e()
    # E -> vazio OU virg LIST-ID
    def e(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.VIRG:
            # Consome virgula, com envio de follows:
            self.consume(self.tokenList.VIRG, self.FOLLOW['e'].split())
            # Chama a funcao list_id:
            self.list_id()
        else:
            # Se vazio so passa:
            pass
    # TIPO -> inteiro OU real OU logico OU caracter
    def tipo(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.INTEIRO:
            # Consome tipo INTEIRO, com envio de follows:
            self.consume(self.tokenList.INTEIRO, self.FOLLOW['tipo'].split())
        elif self.tokenAtual.tipo == self.tokenList.REAL:
            # Consome tipo REAL, com envio de follows:
            self.consume(self.tokenList.REAL, self.FOLLOW['tipo'].split())
        elif self.tokenAtual.tipo == self.tokenList.LOGICO:
            # Consome tipo LOGICO, com envio de follows:
            self.consume(self.tokenList.LOGICO, self.FOLLOW['tipo'].split())
        else:
            # Consome tipo CARACTER, com envio de follows:
            self.consume(self.tokenList.CARACTER, self.FOLLOW['tipo'].split())
    # D -> vazio OU LIST-DECLS
    def d(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.ID:
            # Chama a funcao list_decls:
            self.list_decls()
        else:
            # Se vazio so passa:
            pass
    # C-COMP -> abrech LISTA-COMANDOS fechach
    def c_comp(self):
        # Consome abre chave, com envio de follows:
        self.consume(self.tokenList.ABRECH, self.FOLLOW['c_comp'].split())
        # Chama a funcao lista_comandos:
        self.lista_comandos()
        # Consome fecha chave, com envio de follows:
        self.consume(self.tokenList.FECHACH, self.FOLLOW['c_comp'].split())
    # LISTA-COMANDOS -> COMANDOS G
    def lista_comandos(self):
        # Chama a funcao comandos:
        self.comandos()
        # Chama a funcao g:
        self.g()
    # COMANDOS -> IF OU WHILE OU READ OU WRITE OU ATRIB
    def comandos(self):
        # Verificacao para saber qual regra seguir, no caso qual funcao chamar:
        if self.tokenAtual.tipo == self.tokenList.SE:
            # Chame funcao _if:
            self._if()
        elif self.tokenAtual.tipo == self.tokenList.ENQUANTO:
            # Chame funcao _while:
            self._while()
        elif self.tokenAtual.tipo == self.tokenList.LEIA:
            # Chame funcao _read:
            self._read()
        elif self.tokenAtual.tipo == self.tokenList.ESCREVA:
            # Chame funcao _write:
            self._write()
        else:
            # Chame funcao atrib:
            self.atrib()
    # IF -> se abrepar EXPR fechapar C-COMP H
    def _if(self):
        # Consome SE, com envio de follows:
        self.consume(self.tokenList.SE, self.FOLLOW['_if'].split())
        # Consome abre parentese, com envio de follows:
        self.consume(self.tokenList.ABREPAR, self.FOLLOW['_if'].split())
        # Chame funcao expr:
        self.expr()
        # Consome fecha parentese, com envio de follows:
        self.consume(self.tokenList.FECHAPAR, self.FOLLOW['_if'].split())
        # Chame funcao c_comp:
        self.c_comp()
        # Chame funcao h:
        self.h()
    # EXPR -> SIMPLES P
    def expr(self):
        # Chame funcao simples:
        self.simples()
        # Chame funcao p:
        self.p()
    # SIMPLES -> TERMO R
    def simples(self):
        # Chame funcao termo:
        self.termo()
        # Chame funcao r:
        self.r()
    # TERMO -> FAT S
    def termo(self):
        # Chame funcao fat:
        self.fat()
        # Chame funcao s:
        self.s()
    # FAT -> id OU cte OU abrepar EXPR fechapar OU verdadeiro OU falso OU opneg FAT
    def fat(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.ID:
            # Consome identificador, com envio de follows:
            self.consume(self.tokenList.ID, self.FOLLOW['fat'].split())
        elif self.tokenAtual.tipo == self.tokenList.CTE:
            # Consome constante, com envio de follows:
            self.consume(self.tokenList.CTE, self.FOLLOW['fat'].split())
        elif self.tokenAtual.tipo == self.tokenList.ABREPAR:
            # Consome abre parentese, com envio de follows:
            self.consume(self.tokenList.ABREPAR, self.FOLLOW['fat'].split())
            # Chame funcao expr:
            self.expr()
            # Consome fecha parentese, com envio de follows:
            self.consume(self.tokenList.FECHAPAR, self.FOLLOW['fat'].split())
        elif self.tokenAtual.tipo == self.tokenList.VERDADEIRO:
            # Consome VERDADEIRO, com envio de follows:
            self.consume(self.tokenList.VERDADEIRO, self.FOLLOW['fat'].split())
        elif self.tokenAtual.tipo == self.tokenList.FALSO:
            # Consome FALSO, com envio de follows:
            self.consume(self.tokenList.FALSO, self.FOLLOW['fat'].split())
        else:
            # Consome operador de negaçao, com envio de follows:
            self.consume(self.tokenList.OPNEG, self.FOLLOW['fat'].split())
            # Chame funcao fat:
            self.fat()
    # S -> vazio OU opmul TERMO
    def s(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.OPMUL:
            # Consome operador de multiplicacao e divisao, com envio de follows:
            self.consume(self.tokenList.OPMUL, self.FOLLOW['s'].split())
            # Chame funcao termo:
            self.termo()
        else:
            # Se vazio so passa:
            pass
    # R -> vazio OU opad SIMPLES
    def r(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.OPAD:
            # Consome operador de adiçao e subtraçao, com envio de follows:
            self.consume(self.tokenList.OPAD, self.FOLLOW['r'].split())
            # Chame funcao simples:
            self.simples()
        else:
            # Se vazio so passa:
            pass
    # P -> vazio OU oprel SIMPLES
    def p(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.OPREL:
            # Consome operador de igualdade, diferença, etc e envia ou follows:
            self.consume(self.tokenList.OPREL, self.FOLLOW['p'].split())
            # Chame funcao simples:
            self.simples()
        else:
            # Se vazio so passa:
            pass
    # H -> vazio OU senao C-COMP
    def h(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.SENAO:
            # Consome SENAO, com envio de follows:
            self.consume(self.tokenList.SENAO, self.FOLLOW['h'].split())
            # Chame funcao c_comp:
            self.c_comp()
        else:
            # Se vazio so passa:
            pass
    # WHILE -> enquanto abrepar EXPR fechapar C-COMP
    def _while(self):
        # Consome ENQUANTO, com envio de follows:
        self.consume(self.tokenList.ENQUANTO, self.FOLLOW['_while'].split())
        # Consome abre parentese, com envio de follows:
        self.consume(self.tokenList.ABREPAR, self.FOLLOW['_while'].split())
        # Chame funcao expr:
        self.expr()
        # Consome fecha parentese, com envio de follows:
        self.consume(self.tokenList.FECHAPAR, self.FOLLOW['_while'].split())
        # Chame funcao c_comp:
        self.c_comp()
    # READ -> leia abrepar LIST-ID fechapar pvirg
    def _read(self):
        # Consome LEIA, com envio de follows:
        self.consume(self.tokenList.LEIA, self.FOLLOW['_read'].split())
        # Consome abre parentese, com envio de follows:
        self.consume(self.tokenList.ABREPAR, self.FOLLOW['_read'].split())
        # Chame funcao list_id:
        self.list_id()
        # Consome fecha parentese, com envio de follows:
        self.consume(self.tokenList.FECHAPAR, self.FOLLOW['_read'].split())
        # Consome ponto e virgula, com envio de follows:
        self.consume(self.tokenList.PVIRG, self.FOLLOW['_read'].split())
    # WRITE -> escreva abrepar LIST-W fechapar pvirg
    def _write(self):
        # Consome ESCREVA, com envio de follows:
        self.consume(self.tokenList.ESCREVA, self.FOLLOW['_write'].split())
        # Consome abre parentese, com envio de follows:
        self.consume(self.tokenList.ABREPAR, self.FOLLOW['_write'].split())
        # Chame funcao list_w:
        self.list_w()
        # Consome fecha parentese, com envio de follows:
        self.consume(self.tokenList.FECHAPAR, self.FOLLOW['_write'].split())
        # Consome ponto e virgula, com envio de follows:
        self.consume(self.tokenList.PVIRG, self.FOLLOW['_write'].split())
    # LIST-W -> ELEM-W L
    def list_w(self):
        # Chame funcao elem_w:
        self.elem_w()
        # Chame funcao L:
        self.l()
    # ELEM-W -> EXPR ou cadeia
    def elem_w(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.CADEIA:
            # Consome cadeia de caracteres, com envio de follows:
            self.consume(self.tokenList.CADEIA, self.FOLLOW['elem_w'].split())
        else:
            # Chame funcao expr:
            self.expr()
    # L -> vazio OU virg LIST-W
    def l(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.VIRG:
            # Consome virgula, com envio de follows:
            self.consume(self.tokenList.VIRG, self.FOLLOW['l'].split())
            # Chame funcao list_w:
            self.list_w()
        else:
            # Se vazio so passa:
            pass
    # ATRIB -> id atrib EXPR pvirg
    def atrib(self):
        # Consome identificador, com envio de follows:
        self.consume(self.tokenList.ID, self.FOLLOW['atrib'].split())
        # Consome atribuiçao, com envio de follows:
        self.consume(self.tokenList.ATRIB, self.FOLLOW['atrib'].split())
        # Chame funcao expr:
        self.expr()
        # Consome ponto e virgula, com envio de follows:
        self.consume(self.tokenList.PVIRG, self.FOLLOW['atrib'].split())
    # G -> vazio OU LISTA-COMANDOS
    def g(self):
        # Verificacao para saber qual regra seguir:
        if self.tokenAtual.tipo == self.tokenList.SE or self.tokenAtual.tipo == self.tokenList.ENQUANTO or self.tokenAtual.tipo == self.tokenList.LEIA or self.tokenAtual.tipo == self.tokenList.ESCREVA or self.tokenAtual.tipo == self.tokenList.ID:
            # Chame funcao lista_comandos:
            self.lista_comandos()
        else:
            # Se vazio so passa:
            pass
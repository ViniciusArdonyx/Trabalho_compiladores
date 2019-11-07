# Data: 2019/10/28
# ------------------------------------------------ #
# Autores: Vinícius Araujo - Mat.: 0011941
#          Vinícius Morais - Mat.: 0002864 
# ------------------------------------------------ #
#

class Token:

    # Construtor
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.const = tipo[0]
        self.msg = tipo[1]

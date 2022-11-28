from enum import Enum

from src.Analisadores.AnalisadorLexico import AnalisadorLexico
from src.Program.modules.AbstractProgram import AbstractProgram
from src.Utils.utilsProgram import print_steps

PATH_GR = "entradas/gramaticas/"
PATH_ER = "entradas/ER/"
PATH_CD = "entradas/codigo-fonte/"


# Analisador Léxico
#  - carregar definições regulares
#  - carregar texto fonte
#  - montar TS


# Analisador Léxico
# analisador = AnalisadorLexico()
# analisador.set_er("entradas/ER/exemplo1.er")
# analisador.set_tokens_iniciais("PS,EQ,END")
# analisador.build()
# # analisador.show_tabela_lexica()
# analisador.set_file("entradas/codigo-fonte/exemplo1.codigo")


# Lexico e sintatico esta em AllProgram


class Step(Enum):
    CarregarArquivoER = 1
    CarregarTextoFonte = 2
    MontarTS = 3
    Clear = 4


class LexicoProgram(AbstractProgram):
    def __init__(self):
        self.lexico = AnalisadorLexico()

        self.functions = {
            Step.CarregarArquivoER: self.carregar_arquivo_er,
            Step.CarregarTextoFonte: self.carregar_texto_fonte,
            Step.MontarTS: self.montar_ts,

            Step.Clear: self.clear

        }

        self.lexico_now = 0

    def run(self):
        while True:
            print("Você está na sessão de Analisador Léxico: \n")
            print_steps(Step)

            try:
                result = int(input(": "))
            except ValueError:
                print("Você deve digitar um número")
                continue

            try:
                function = self.functions[Step(result)]
                function()
            except ValueError:
                break

    def carregar_arquivo_er(self):
        if self.lexico is None:
            print("Ainda não foi carregado um Analisador Léxico. \n")
            return

        try:
            self.lexico.set_er("entradas/ER/exemplo1.er")
        except Exception as e:
            print("Houve algum erro ao carregar arquivo de ER : " + str(e))

    def carregar_texto_fonte(self):
        # analisador.set_tokens_iniciais("PS,EQ,END")
        # analisador.build()
        # # analisador.show_tabela_lexica()
        # analisador.set_file("entradas/codigo-fonte/exemplo1.codigo")
        if self.lexico is None:
            print("Ainda não foi carregado um Analisador Léxico. \n")
            return

        try:
            pass
        except Exception as e:
            print("Houve algum erro ao carregar um texto fonte : " + str(e))

    def montar_ts(self):
        if self.lexico is None:
            print("Ainda não foi carregado um Analisador Léxico. \n")
            return

        try:
            self.lexico.build()
            self.lexico.show_tabela_lexica()
        except Exception as e:
            print("Houve algum erro ao montar a TS: " + str(e))

    def clear(self):
        self.lexico = None
        self.lexico_now = 0

        print("Analisador Léxico fo reinicializado. \n")

from enum import Enum
from typing import Union

from src.Analisadores.AnalisadorLexico import AnalisadorLexico
from src.Exceptions.Lexicon.TokenNotValidException import TokenNotValidException
from src.Program.modules.AbstractProgram import AbstractProgram
from src.Utils.utilsProgram import print_steps

PATH_ER = "entradas/ER/"
PATH_CD = "entradas/codigo-fonte/"


# Analisador Léxico
#  - carregar definições regulares
#  - carregar texto fonte
#  - mostrar tabela léxica AFD unido
#  - mostrar TS
#  - mostrar lista de tokens


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
    DefinirTokensIniciais = 2
    MostrarTabelaLexicaAFDunido = 3
    CarregarTextoFonte = 4
    MostrarTS = 5
    MostrarListaTokens = 6
    Clear = 7


class LexicoProgram(AbstractProgram):
    def __init__(self):
        self.lexico: Union[AnalisadorLexico, None] = None

        self.functions = {
            Step.CarregarArquivoER: self.carregar_arquivo_er,
            Step.DefinirTokensIniciais: self.definir_tokens_iniciais,
            Step.MostrarTabelaLexicaAFDunido: self.mostrar_tabela_lexica,
            Step.CarregarTextoFonte: self.carregar_texto_fonte,
            Step.MostrarTS: self.mostrar_ts,
            Step.MostrarListaTokens: self.mostrar_lista_tokens,
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
        try:
            print(f"""
                Digite o local onde está armazenado o arquivo de ER.
                OBS: Se você não digitar um caminho que comece com "/",
                tentará pegar automaticamente da pasta do projeto localizada em
                {PATH_ER}.
                Digite 0 para sair dessa função.
            """)
            path = input(": ")

            if path == "0":
                return

            self.lexico = AnalisadorLexico()

            if path.startswith("/"):
                self.lexico.set_er(path)
            else:
                self.lexico.set_er(PATH_ER + path)
        except Exception as e:
            print("Houve algum erro ao carregar arquivo de ER : " + str(e))

    def definir_tokens_iniciais(self):
        if self.lexico is None:
            print("Ainda não foi carregado um Analisador Léxico. \n")
            return

        print("""
            Você deve dar uma lista de quais tokens já devem estar na 
            TS antes de fazer a lista de tokens.
            Formato solicitado: token1,token2,token3,...
        """)

        tokens = input(": ")

        try:
            self.lexico.set_tokens_iniciais(tokens)
            self.lexico.build()
        except Exception as e:
            print("Houve algum erro ao definir tokens iniciais: " + str(e))

    def mostrar_tabela_lexica(self):
        if self.lexico is None:
            print("Ainda não foi carregado um Analisador Léxico. \n")
            return

        self.lexico.show_tabela_lexica()

    def carregar_texto_fonte(self):
        if self.lexico is None:
            print("Ainda não foi carregado um Analisador Léxico. \n")
            return

        print(f"""
            Digite o local onde está armazenado o arquivo de código fonte.
            OBS: Se você não digitar um caminho que comece com "/",
            tentará pegar automaticamente da pasta do projeto localizada em
            {PATH_CD}.
            Digite 0 para sair dessa função.
        """)
        path = input(": ")

        if path == "0":
            return

        try:
            if path.startswith("/"):
                self.lexico.set_file(path)
            else:
                self.lexico.set_file(PATH_CD + path)

        except TokenNotValidException as e:
            print("Algum token não foi reconhecido pelo analisador léxico: " + str(e))
        except Exception as e:
            print("Houve algum erro ao carregar um texto fonte : " + str(e))

    def mostrar_ts(self):
        if self.lexico is None:
            print("Ainda não foi carregado um Analisador Léxico. \n")
            return

        print(self.lexico.ts)

    def mostrar_lista_tokens(self):
        if self.lexico is None:
            print("Ainda não foi carregado um Analisador Léxico. \n")
            return

        print(self.lexico.tokens)

    def clear(self):
        self.lexico = None
        self.lexico_now = 0

        print("Analisador Léxico fo reinicializado. \n")

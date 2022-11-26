from enum import Enum

from src.Program.modules.AbstractProgram import AbstractProgram
from src.Analisadores.AnalisadorLexico import AnalisadorLexico
from src.Analisadores.AnalisadorSintatico import AnalisadorSintatico

# Analisador Léxico e Sintático
#  - carregar definições regulares
#  - carregar gramática
#  - carregar texto fonte
#  - mostrar TS
#  - mostrar Tabela de Análise sintática LL(1)
#  - mostrar se texto fonte é aceito


# Analisador Léxico
# analisador.set_er("entradas/ER/exemplo1.er")
# analisador.set_tokens_iniciais("PS,EQ,END")
# analisador.build()
# # analisador.show_tabela_lexica()
# analisador.set_file("entradas/codigo-fonte/exemplo1.codigo")

# sintatioco
# sintatico = AnalisadorSintatico(analisador)
# sintatico.set_grammar("entradas/gramaticas/variavel.grammar")
# sintatico.build()
# print(sintatico.run_entrada("teste=3"))
# print(sintatico.run_file())


PATH_GR = "entradas/gramaticas/"
PATH_ER = "entradas/ER/"
PATH_CD = "entradas/codigo-fonte/"


class Step(Enum):
    IniciarAnalisadorLexicoSintatico = 1

    Clear = 8


class AllProgram(AbstractProgram):
    def __init__(self):
        self.analisador = None
        self.sintatico = None

        self.functions = {
            Step.IniciarAnalisadorLexicoSintatico: self.inicializar_analisador_Lexico_Sintatico,
           
            Step.Clear: self.clear
        }

    def run(self):
        while True:
            print("Você está na sessão de Analisador Léxico e Sintático: \n")
            [print(f"{x.value}: {x.name}") for x in Step]

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

    def inicializar_analisador_Lexico_Sintatico(self):
        print(f"""
            Digite o local onde está armazenado o arquivo de ER.
            OBS: Se você não digitar um caminho que comece com "/",
            tentará pegar automaticamente da pasta do projeto localizada em
            {PATH_ER}.
            Digite 0 para sair dessa função.
        """)
        path = input(": ")

        try:
            self.analisador = AnalisadorLexico()
            if path.startswith("/"):
                self.analisador.set_er(path)
            else:
                self.analisador.set_er(PATH_ER + path)
        except IOError:
            print("Houve algum problema ao carregar o arquivo ER. Tente novamente. \n")
            return

        try:
            self.analisador.set_tokens_iniciais("PS,EQ,END")
            self.analisador.build()
            self.analisador.show_tabela_lexica()
        except IOError:
            print("Houve algum problema na execução do Analisador Léxico e Sintático. Tente novamente. \n")
            return

        try:
            if path.startswith("/"):
                self.analisador.set_file(path)
            else:
                self.analisador.set_file(PATH_ER + path)
        except IOError:
            print("Houve algum problema ao carregar o arquivo do código. Tente novamente. \n")
            return

        try:
            self.sintatico = AnalisadorSintatico(self.analisador)
        except IOError:
            print("Houve algum problema na execução do Analisador Léxico e Sintático. Tente novamente. \n")
            return

        try:
            if path.startswith("/"):
                self.sintatico.set_grammar(path)
            else:
                self.sintatico.set_grammar(PATH_ER + path)
        except IOError:
            print("Houve algum problema ao carregar o arquivo de gramatica. Tente novamente. \n")
            return

        try:
            self.sintatico.build()
            print(self.sintatico.run_file())
        except IOError:
            print("Houve algum problema na execução do Analisador Léxico e Sintático. Tente novamente. \n")
            return
            
    def clear(self):
        self.analisador = None
        self.sintatico = None

        print("Analisador Léxico e Sintático foi reinicializado. \n")

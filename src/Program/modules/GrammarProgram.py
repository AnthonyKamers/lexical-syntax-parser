from enum import Enum

from src.Grammar.Grammar import Grammar
from src.Program.modules.AbstractProgram import AbstractProgram
from src.Utils.utilsProgram import print_steps

PATH_GR = "entradas/gramaticas/"


# Gramática
#  - carregar arquivo
#  - remover recursão à esquerda
#  - RemoverNaoDeterminismo
#  - Firsts e Follows
#  - ver se é LL(1)


# Gramática
# grammar = Grammar()
# grammar.parse_file("entradas/gramaticas/exemplo-rec-esquerda-indireta.grammar")
# print(grammar.has_left_recursion())
# grammar.remove_recursao_esquerda()
# grammar.remove_nao_determinismo()
# print(grammar.has_nullable(), grammar.has_left_recursion())


# Analisador Sintático
# grammar = Grammar()
# grammar.parse_file("entradas/gramaticas/exemplo-ll1-valido1.grammar")
# grammar.get_firsts()
# grammar.get_follows()
# print(grammar.is_ll1())


class Step(Enum):
    CarregarArquivo = 1
    RetornarSeTemRecursaoEsquerda = 2
    RemoverRecursaoEsquerda = 3
    RemoverNaoDeterminismo = 4
    Retornar_Nullable_HasLeftRecursion = 5
    FazerFirstsFollows = 6
    VerificarLL1 = 7
    Clear = 8


class GrammarProgram(AbstractProgram):
    def __init__(self):
        self.grammar = None

        self.functions = {
            Step.CarregarArquivo: self.carregar_arquivo,
            Step.RetornarSeTemRecursaoEsquerda: self.retornar_se_rec_esquerda,
            Step.RemoverRecursaoEsquerda: self.remover_rec_esquerda,
            Step.RemoverNaoDeterminismo: self.remover_nao_determinismo,
            Step.Retornar_Nullable_HasLeftRecursion: self.retornar_nullable_has_left_recursion,
            Step.FazerFirstsFollows: self.make_firsts_follows,
            Step.VerificarLL1: self.verify_is_ll1,
            Step.Clear: self.clear

        }

        self.grammar_now = 0

    def run(self):
        while True:
            print("Você está na sessão de Gramática: \n")
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

    def carregar_arquivo(self):
        print(f"""
            Digite o local onde está armazenado o arquivo de Gramática.
            OBS: Se você não digitar um caminho que comece com "/",
            tentará pegar automaticamente da pasta do projeto localizada em
            {PATH_GR}.
            Digite 0 para sair dessa função.
        """)
        path = input(": ")
        try:
            self.grammar = Grammar()

            if path.startswith("/"):
                self.grammar.parse_file(path)
            else:
                self.grammar.parse_file(PATH_GR + path)

            print("Arquivo carregado. \n")
        except IOError:
            print("Houve algum problema ao fazer parse do arquivo. Tente novamente. \n")
            self.carregar_arquivo()

    def retornar_se_rec_esquerda(self):
        if self.grammar is None:
            print("Ainda não foi carregado uma Gramática. \n")
            return

        try:
            print(self.grammar.has_left_recursion())
        except Exception as e:
            print("Houve algum erro ao xx a Gramática: " + str(e))

    def remover_rec_esquerda(self):
        if self.grammar is None:
            print("Ainda não foi carregado uma Gramática. \n")
            return

        try:
            self.grammar.remove_recursao_esquerda()
            print("Removido recursão da Gramática. \n")
        except Exception as e:
            print("Houve algum erro ao remover recursão da Gramática: " + str(e))

    def remover_nao_determinismo(self):
        if self.grammar is None:
            print("Ainda não foi carregado uma Gramática. \n")
            return

        try:
            self.grammar.remove_nao_determinismo()
            print("Removido não determinismo da Gramática com sucesso. \n")
        except Exception as e:
            print("Houve algum erro ao remover não determinismo da Gramática: " + str(e))

    def retornar_nullable_has_left_recursion(self):
        if self.grammar is None:
            print("Ainda não foi carregado uma Gramática. \n")
            return

        try:
            print(self.grammar.has_nullable(), self.grammar.has_left_recursion())
        except Exception as e:
            print("Houve algum erro ao retornar se ter nullable e recursão a esquerda da Gramática: " + str(e))

    def make_firsts_follows(self):
        if self.grammar is None:
            print("Ainda não foi carregado uma Gramática. \n")
            return

        try:
            self.grammar.get_firsts()
            self.grammar.get_follows()
            print("Feito firsts e follows da Gramática com sucesso. \n")
        except Exception as e:
            print("Houve algum erro ao fazer firsts e follows da Gramática: " + str(e))

    def verify_is_ll1(self):
        if self.grammar is None:
            print("Ainda não foi carregado uma Gramática. \n")
            return

        try:
            print(self.grammar.is_ll1())
        except Exception as e:
            print("Houve algum erro ao verificar se a Gramática é LL(1): " + str(e))

    def clear(self):
        self.grammar = None

        print("Gramática foi reinicializada. \n")

from enum import Enum
from typing import Union, List

from src.Analisadores.AnalisadorLexico import AnalisadorLexico
from src.Analisadores.AnalisadorSintatico import AnalisadorSintatico
from src.Exceptions.Syntactic.LoopNaoDeterminismoException import LoopNaoDeterminismoException
from src.Exceptions.Syntactic.NotLL1Exception import NotLL1Exception
from src.Program.modules.AbstractProgram import AbstractProgram
from src.Program.modules.LexicoProgram import LexicoProgram
from src.Utils.utils import pretty_print_matrix
from src.Utils.utilsProgram import print_steps

# Analisador Léxico e Sintático
#  - carregar definições regulares
#  - carregar gramática
#  - carregar texto fonte
#  - mostrar TS
#  - mostrar lista de tokens
#  - mostrar Tabela de Análise sintática LL(1)
#  - mostrar se texto fonte é aceito LL(1)


# Analisador Léxico
# analisador.set_er("entradas/ER/exemplo1.er")
# analisador.set_tokens_iniciais("PS,EQ,END")
# analisador.build()
# # analisador.show_tabela_lexica()
# analisador.set_file("entradas/codigo-fonte/exemplo1.codigo")

# Analisador Sintático
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
    CarregarGramaticaSintatico = 2
    RodarArquivo = 3
    MostrarTS = 4
    MostrarListaTokens = 5
    MostrarTabelaAnaliseSintatica = 6
    Clear = 7


class LexicoSintaticoProgram(AbstractProgram):
    def __init__(self):
        self.lexico: Union[AnalisadorLexico, None] = None
        self.sintatico: Union[AnalisadorSintatico, None] = None

        self.functions = {
            Step.IniciarAnalisadorLexicoSintatico: self.inicializar_analisador_lexico_sintatico,
            Step.CarregarGramaticaSintatico: self.carregar_gramatica,
            Step.RodarArquivo: self.rodar_arquivo,
            Step.MostrarTS: self.mostrar_ts,
            Step.MostrarListaTokens: self.mostrar_lista_tokens,
            Step.MostrarTabelaAnaliseSintatica: self.mostrar_tabela_analise_sintatica,
            Step.Clear: self.clear
        }

    def run(self):
        while True:
            print("Você está na sessão de Analisador Léxico e Sintático: \n")
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

    def inicializar_analisador_lexico_sintatico(self):
        lexico_program: LexicoProgram = LexicoProgram()

        lexico_program.carregar_arquivo_er()
        lexico_program.definir_tokens_iniciais()
        lexico_program.carregar_texto_fonte()

        # analisador léxico feito com sucesso
        self.lexico = lexico_program.lexico
        self.sintatico = AnalisadorSintatico(self.lexico)

    def carregar_gramatica(self):
        if self.sintatico is None:
            print("Ainda não foi carregado um analisador léxico/sintático. \n")
            return

        print(f"""
            Digite o local onde está armazenado o arquivo de gramática.
            OBS: Se você não digitar um caminho que comece com "/",
            tentará pegar automaticamente da pasta do projeto localizada em
            {PATH_GR}.
            Digite 0 para sair dessa função.
        """)
        path = input(": ")

        try:
            if path.startswith("/"):
                self.sintatico.set_grammar(path)
            else:
                self.sintatico.set_grammar(PATH_GR + path)

            self.sintatico.build()

        except LoopNaoDeterminismoException as e:
            print("Algum loop foi identificado: " + str(e))
        except NotLL1Exception as e:
            print("A gramática carregada não é compatível com o analisador sintático LL(1): " + str(e))
        except Exception as e:
            print("Houve algum erro ao carregar gramática: " + str(e))

    def rodar_arquivo(self):
        if self.sintatico is None:
            print("Ainda não foi carregado um analisador léxico/sintático. \n")
            return

        print("""
            Nesta etapa, o arquivo é rodado com as regras da gramática especificada
            e com os tokens da lista de tokens. Com o algoritmo de pilha para LL(1),
            é retornado se o código é aceito com os parâmetros especificados ou não.
            True caso aceite, False caso rejeite.
        """)

        try:
            print("Resultado: " + str(self.sintatico.run_file()))
        except Exception as e:
            print("Houve algum erro ao rodar arquivo: " + str(e))

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

    def mostrar_tabela_analise_sintatica(self):
        if self.sintatico is None:
            print("Ainda não foi carregado um analisador léxico/sintático. \n")
            return

        # PS,EQ,END

        try:
            matrix: List[List[str]] = [["T/N"]]

            for terminal in self.sintatico.grammar.get_terminais():
                matrix[0].append(terminal.simbolo)

            for nao_terminal in self.sintatico.grammar.get_nao_terminais():
                lista = [nao_terminal.simbolo]

                for terminal in self.sintatico.grammar.get_terminais():
                    producoes = self.sintatico.tabela_sintatica.table[nao_terminal][terminal]
                    if len(producoes) == 0:
                        lista.append(" ")
                    else:
                        producao = ""
                        for simbolo in producoes[0]:
                            producao += f"{simbolo.simbolo},"
                        lista.append(producao[:-1])

                matrix.append(lista)

            pretty_print_matrix(matrix)
        except Exception as e:
            print("Houve algum erro ao mostrar tabela análise sintática: " + str(e))

    def clear(self):
        self.lexico = None
        self.sintatico = None

        print("Analisador Léxico e Sintático foram reinicializados. \n")

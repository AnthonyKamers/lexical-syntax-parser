from enum import Enum

from src.Program.modules.LexicoSintaticoProgram import LexicoSintaticoProgram
from src.Program.modules.AFProgram import AFProgram
from src.Program.modules.ERProgram import ERProgram
from src.Program.modules.GrammarProgram import GrammarProgram
from src.Program.modules.LexicoProgram import LexicoProgram


class State(Enum):
    AF = 1
    ER = 2
    GRAMMAR = 3
    LEXICO = 4
    LexicoSintatico = 5


class Program:
    def __init__(self):
        self.functions = {
            State.AF: AFProgram,
            State.ER: ERProgram,
            State.GRAMMAR: GrammarProgram,
            State.LEXICO: LexicoProgram,
            State.LexicoSintatico: LexicoSintaticoProgram
        }

    def run(self):
        print("""
            Bem vindo ao software gerador de analisador léxico e sintático!!
            Para executar as operações do programa, basta digitar os comandos a
            seguir (ou qualquer outro inteiro para sair da aplicação):
        """)

        while True:
            print("Digite um comando: ")
            [print(f"{x.value}: {x.name}") for x in State]

            try:
                result = int(input(": "))
            except ValueError:
                print("Você deve digitar um número")
                continue

            try:
                classe = self.functions[State(result)]
                classe().run()
            except ValueError:
                break

from enum import Enum


class State(Enum):
    AF = 1
    ER = 2
    GRAMMAR = 3
    LEXICO = 4
    ALL = 5
    EXIT = 6


class Program:
    def __init__(self):
        self.functions = {
            State.AF: "",
            State.ER: "",
            State.GRAMMAR: "",
            State.LEXICO: "",
            State.ALL: "",
            State.EXIT: ""
        }

    def run(self):
        print("""
            Bem vindo ao software gerador de analisador léxico e sintático!!
            Para executar as operações do programa, basta digitar os comandos a seguir:
        """)

        states = [(x.name, x.value) for x in State]
        while True:
            print("Digite um comando: ")
            for state in states:
                print(state)
            break

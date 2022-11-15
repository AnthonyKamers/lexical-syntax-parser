from src.Exceptions.Syntactic.SyntacticException import SyntacticException


class LoopNaoDeterminismoException(SyntacticException):
    def __init__(self):
        super().__init__("Não foi possível transformar a gramática em não determinista (entrou em loop infinito)")

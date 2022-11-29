from src.Exceptions.Syntactic.SyntacticException import SyntacticException


class NotProductionTabela(SyntacticException):
    def __init__(self):
        super().__init__("A entrada que deveria conter na Tabela Sintática LL(1) está incorreta")

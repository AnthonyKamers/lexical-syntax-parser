from src.Exceptions.Syntactic.SyntacticException import SyntacticException


class NotLL1Exception(SyntacticException):
    def __init__(self):
        super().__init__("A gramática escolhida não é compatível com preditivo LL(1)")

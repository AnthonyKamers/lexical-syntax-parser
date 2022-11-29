from src.Exceptions.Syntactic.SyntacticException import SyntacticException


class SymbolGrammarException(SyntacticException):
    def __init__(self):
        super().__init__("Algum símbolo declarado na gramática não é uma definição regular válida")

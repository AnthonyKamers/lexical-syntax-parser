from src.Exceptions.Syntactic.SyntacticException import SyntacticException


class DifferentSyntaxExpected(SyntacticException):
    def __init__(self):
        super().__init__("A análise sintática detectou uma inconformidade na estrutura: não-terminal não esperado "
                         "neste momento.")

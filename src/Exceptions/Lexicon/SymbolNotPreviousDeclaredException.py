from src.Exceptions.Lexicon.LexiconException import LexiconException


class SymbolNotPreviousDeclaredException(LexiconException):
    def __init__(self):
        super().__init__("Identificador deve ser declarado previamente")

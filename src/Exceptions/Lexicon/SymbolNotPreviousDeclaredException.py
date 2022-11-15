from src.Exceptions.Lexicon.LexiconException import LexiconException


class SymbolNotPreviousDeclaredException(LexiconException):
    def __init__(self):
        super("Identificador deve ser declarado previamente")

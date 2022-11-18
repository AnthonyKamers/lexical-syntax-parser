from src.Exceptions.Lexicon.LexiconException import LexiconException


class TokenNotValidException(LexiconException):
    def __init__(self):
        super().__init__("Token identificado não é válido para as definições regulares passadas")

from src.Analisadores.AnalisadorLexico import AnalisadorLexico
from src.Analisadores.AnalisadorSintatico import AnalisadorSintatico

FALHA_LER_ARQUIVO = "Falha ao ler arquivo"


class AnalisadorMain:
    def __init__(self):
        self.lexico = AnalisadorLexico()
        self.sintatico = AnalisadorSintatico(self.lexico)

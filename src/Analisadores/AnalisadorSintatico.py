from src.Grammar.Grammar import Grammar
from src.PilhaSintatica.PilhaSintatica import PilhaSintatica
from src.TabelaSintatica.TabelaSintatica import TabelaSintatica


class AnalisadorSintatico:
    def __init__(self, file_name: str):
        self.grammar = Grammar()
        self.grammar.parse_file(file_name)
        self.tabela_sintatica = TabelaSintatica(self.grammar)
        self.pilha = PilhaSintatica(self)

    def execute(self):
        self.grammar.remove_recursao_esquerda()
        self.grammar.remove_nao_determinismo()
        self.grammar.get_firsts()
        self.grammar.get_follows()
        self.grammar.is_ll1()

        self.tabela_sintatica.get_table()

        print(self.pilha.testar_entrada("dadbd"))


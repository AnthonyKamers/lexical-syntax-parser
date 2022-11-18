from src.Grammar.Grammar import Grammar
from src.PilhaSintatica.PilhaSintatica import PilhaSintatica
from src.TabelaSintatica.TabelaSintatica import TabelaSintatica


class AnalisadorSintatico:
    """
    Faz os procedimentos necessários para fazer construir o analisador sintático
    """
    def __init__(self):
        self.grammar = Grammar()
        self.tabela_sintatica = TabelaSintatica(self.grammar)
        self.pilha = PilhaSintatica(self)
        self.has_grammar = False

    def set_grammar(self, file_name: str, is_analyze: bool):
        """
        Setta a gramática do analisador sintático
        :param file_name: Path do arquivo de entrada
        :param is_analyze: Se é um analisador simples/complexo
        """
        self.grammar.parse_file(file_name, is_analyze)

    def build(self):
        """
        Executa os procedimentos de construção das etapas do analisador sintático.
        Também faz várias checagens, para garantir que a gramática escolhida consegue ser
        transformada em um analisador sintático LL(1)
        """
        self.grammar.remove_recursao_esquerda()
        self.grammar.remove_nao_determinismo()
        self.grammar.get_firsts()
        self.grammar.get_follows()
        self.grammar.is_ll1()

        self.tabela_sintatica.get_table()

    def run_entrada(self, entrada: str) -> bool:
        """
        Roda para uma determinada entrada, se aceita ou a rejeita com a gramática inserida
        :param entrada: Entrada para rodar a gramática com o analisador LL(1)
        :return: Se aceita ou rejeita a entrada
        """
        return self.pilha.run_entrada(entrada)

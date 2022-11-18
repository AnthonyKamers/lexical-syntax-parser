from src.Analisadores.AnalisadorLexico import AnalisadorLexico
from src.Exceptions.Syntactic.SymbolGrammarException import SymbolGrammarException
from src.Grammar.Grammar import Grammar
from src.PilhaSintatica.PilhaSintatica import PilhaSintatica
from src.TabelaSintatica.TabelaSintatica import TabelaSintatica


class AnalisadorSintatico:
    """
    Faz os procedimentos necessários para fazer construir o analisador sintático
    """
    def __init__(self, lexico: AnalisadorLexico):
        self.lexico = lexico
        self.grammar = Grammar()
        self.tabela_sintatica = TabelaSintatica(self.grammar)
        self.pilha = PilhaSintatica(self)
        self.has_grammar = False

    def set_grammar(self, file_name: str):
        """
        Setta a gramática do analisador sintático
        :param file_name: Path do arquivo de entrada
        """
        self.grammar.parse_file(file_name)

        # checar se os símbolos terminais da gramática
        # são diferentes dos estabelecidos no arquivo de definições regulares
        terminais = self.grammar.get_terminais()
        definicoes_regulares = self.lexico.get_definicoes_regulares()

        for terminal in terminais:
            if terminal.simbolo == "&" or terminal.simbolo in definicoes_regulares:
                continue
            else:
                raise SymbolGrammarException

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

    def run_file(self) -> bool:
        """
        Roda a TS construída pelo analisador léxico, para garantir
        que a sintaxe está de acordo a gramática
        :return: Se o código fonte está de acordo
        """
        return self.pilha.run_file()

    def run_entrada(self, entrada: str) -> bool:
        """
        Roda para uma determinada entrada, se aceita ou a rejeita com a gramática inserida
        :param entrada: Entrada para rodar a gramática com o analisador LL(1)
        :return: Se aceita ou rejeita a entrada
        """
        return self.pilha.run_entrada(entrada)

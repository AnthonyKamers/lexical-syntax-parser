from src.Exceptions.Syntactic.NotLL1Exception import NotLL1Exception
from src.Grammar.Grammar import Grammar


# {
#     "S": {
#         "a": [[AB]],
#         "b": []
#     }
# }

class TabelaSintatica:
    """
    Implentação de uma tabela sintática utilizada no analisador LL(1)
    """

    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = {}

    def construct_table(self):
        for nao_terminal in self.grammar.get_nao_terminais():
            self.table[nao_terminal] = {}

            for terminal in self.grammar.get_terminais():
                self.table[nao_terminal][terminal] = []

    def check_is_ll1(self):
        for _, nao_terminal in self.table.items():
            for _, terminal in nao_terminal.items():
                if len(terminal) > 1:
                    raise NotLL1Exception

    def get_table(self):
        self.construct_table()

        epsilon = self.grammar.find_symbol("&")

        for nao_terminal in self.grammar.get_nao_terminais():
            for producao in nao_terminal.producoes:
                if epsilon not in producao:
                    if producao[0].is_terminal():
                        # if any(elem.is_terminal() for elem in producao):
                        first = set()
                        for simbolo in producao:
                            if simbolo.is_terminal():
                                first.add(simbolo)
                    else:
                        first = nao_terminal.firsts

                    for terminal in first:
                        self.table[nao_terminal][terminal].append(producao)
                else:
                    for terminal in nao_terminal.follows:
                        self.table[nao_terminal][terminal].append(producao)

        self.check_is_ll1()

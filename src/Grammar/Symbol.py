from typing import List


class Symbol:
    def __init__(self, simbolo: str, grammar: any):
        self.grammar = grammar
        self.simbolo = simbolo
        self.producoes: List[List[Symbol]] = []
        self.is_terminal = False

    def __repr__(self):
        return f"{'Terminal' if self.is_terminal else 'Não terminal'} - {self.simbolo}"

    def add_producoes(self, producoes: List[str]):
        for producao in producoes:
            lista = []
            for char in producao:
                symbol = self.grammar.find_symbol(char)
                lista.append(symbol)
            self.producoes.append(lista)

    def check_terminal(self):
        if len(self.producoes) == 0:
            self.is_terminal = True

    def is_nullable(self) -> bool:
        for producao in self.producoes:
            for symbol in producao:
                if symbol.simbolo == "&":
                    return True
        return False

    def is_recursive(self):
        return self.is_recursive_check(self)

    def is_recursive_check(self, symbol_check) -> bool:
        # checar produções diretas
        for producao in self.producoes:
            for symbol in producao:
                if symbol == symbol_check:
                    return True

        # checar produções indiretas
        for producao in self.producoes:
            for symbol in producao:
                if not symbol.is_terminal:
                    # se for não terminal, seguir
                    result = symbol.is_recursive_check(self)
                    if result:
                        return True
        return False

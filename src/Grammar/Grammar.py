from typing import List, Union

from src.Grammar.Symbol import Symbol


class Grammar:
    def __init__(self):
        self.simbolos: List[Symbol] = []
        self.simbolo_inicial: Union[Symbol, None] = None

    def parse_file(self, file_name: str):
        def get_terminal():
            for symbol in self.simbolos:
                symbol.check_terminal()

        with open(file_name) as file:
            for line in file:
                line = line.replace(" ", "").replace("\n", "")
                simbolo, producoes = line.split("->")
                producoes = producoes.split("|")

                new_symbol = self.find_symbol(simbolo)
                new_symbol.add_producoes(producoes)

        # análise de quais símbolos são terminais devem
        # ser feitos após varredura completa no arquivo,
        # pois não há um padrão para símbolo terminal ou não terminal
        get_terminal()
        self.simbolo_inicial = self.simbolos[0]

    def get_terminais(self) -> List[Symbol]:
        return self.get_specific_simbolos(True)

    def get_nao_terminais(self) -> List[Symbol]:
        return self.get_specific_simbolos(False)

    def get_specific_simbolos(self, type_terminal: bool) -> List[Symbol]:
        return [x for x in self.simbolos if x.is_terminal == type_terminal]

    def has_recursive(self) -> bool:
        return len([x for x in self.get_nao_terminais() if x.is_recursive()]) > 0

    def has_nullable(self) -> bool:
        return len([x for x in self.get_nao_terminais() if x.is_nullable()]) > 0

    def find_symbol(self, simbolo: str) -> Symbol:
        symbol: Symbol
        try:
            symbol = self.get_symbol(simbolo)
        except StopIteration:
            symbol = Symbol(simbolo, self)
            self.simbolos.append(symbol)
        return symbol

    def get_symbol(self, simbolo: str):
        return next(symbol for symbol in self.simbolos if symbol.simbolo == simbolo)

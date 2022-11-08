from typing import List, Union

from src.Grammar.Symbol import Symbol

import string
import random

# flags
MAX_EXECUTION_NAO_DETERMINISMO = 50


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
                # ignorar comentários (para facilitar debbug)
                if line.startswith("#"):
                    continue
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
        """
        Retorna se a gramática é recursiva de alguma maneira
        (não necessariamente à esquerda)
        :return: Se a gramática é recursiva
        """
        return len([x for x in self.get_nao_terminais() if x.is_recursive()]) > 0

    def has_left_recursion(self) -> bool:
        """
        Retorna se a gramática é recursiva à esquerda
        :return: Se a gramática é recursiva à esquerda
        """
        return len([x for x in self.get_nao_terminais() if x.is_left_recursive()]) > 0

    def has_nullable(self) -> bool:
        """
        Retorna se a gramática contém o símbolo nulo (&)
        :return: Se a gramática contém o símbolo nulo (&)
        """
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

    def has_symbol(self, simbolo: str):
        try:
            self.get_symbol(simbolo)
            return True
        except StopIteration:
            return False

    def generate_random_symbol(self) -> Symbol:
        while True:
            random_char = random.choice(string.ascii_uppercase)
            if not self.has_symbol(random_char):
                symbol = Symbol(random_char, self)
                self.simbolos.append(symbol)
                return symbol

    def remove_nao_determinismo(self):
        """
        Este método transforma a gramática em não determinística para
        uma deterministica (na forma fatorada).
        Este método deve ser executado após a transformação de recursão à
        esquerda, podendo levar a um "loop" infinito caso isso não seja feito.
        """
        i = 0
        while True:
            changed = False
            for symbol in self.get_nao_terminais():
                flag = symbol.remove_nao_determinismo_direto()
                flag1 = symbol.transforma_nao_determinismo_indireto()

                changed = changed or flag or flag1
            i += 1

            if not changed:
                break

            if i == MAX_EXECUTION_NAO_DETERMINISMO:
                raise "Não foi possível transformar a gramática em " \
                      "não determinista (entrou em loop infinito)."

    def remove_recursao_esquerda(self):
        """
        Este método transforma a gramática de recursiva à esquerda para
        não recursiva à esquerda
        """
        nao_terminais = self.get_nao_terminais()

        # fazer para todos os terminais
        for k1, terminal1 in enumerate(nao_terminais):
            # se for o símbolo inicial, remover recursão direta
            if k1 == 0:
                terminal1.remove_recursao_esquerda_direta()

            for k2, terminal2 in enumerate(nao_terminais):
                if terminal1 == terminal2 or k2 < k1:
                    # se for o mesmo terminal, não precisa fazer nada,
                    # pois a recursão direta é feita em outro momento
                    continue

                else:
                    # fazer recursão indireta de terminal1 em terminal2
                    changed = terminal2.remove_recursao_esquerda_indireta(terminal1)

                    # se houve alteração, fazer remoção de recursão direta em terminal2
                    if changed:
                        terminal2.remove_recursao_esquerda_direta()

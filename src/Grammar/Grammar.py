import copy
from typing import List, Union

from src.Grammar.Symbol import Symbol

import string
import random

from src.Utils.utils import remove_duplicates_lista, subtract_listas

# flags
MAX_EXECUTION_NAO_DETERMINISMO = 50  # quantidade máxima de "loops" em não determinismo


class Grammar:
    def __init__(self):
        self.simbolos: List[Symbol] = []
        self.simbolo_inicial: Union[Symbol, None] = None

    def parse_file(self, file_name: str):
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
        self.simbolo_inicial = self.simbolos[0]

    def get_terminais(self) -> List[Symbol]:
        return self.get_specific_simbolos(True)

    def get_nao_terminais(self) -> List[Symbol]:
        return self.get_specific_simbolos(False)

    def get_specific_simbolos(self, type_terminal: bool) -> List[Symbol]:
        return [x for x in self.simbolos if x.is_terminal() == type_terminal]

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
                raise Exception("Não foi possível transformar a gramática em não determinista (entrou em loop "
                                "infinito).")

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

    def get_firsts(self):
        """
        Preenche os Firsts, para fazer o analisador sintático LL(1)
        """
        epsilon = self.find_symbol("&")
        set_epsilon = {epsilon}

        # fazer firsts dos terminais
        for simbolo in self.get_terminais():
            simbolo.firsts.add(simbolo)

        # fazer firsts dos não terminais
        while True:
            firsts_copy = []

            # para cada terminal, adiciona ele próprio em seus firsts
            for simbolo in self.simbolos:
                firsts_copy.append(frozenset(simbolo.firsts))

            # para cada não terminal, checar firsts e &-produções
            for nao_terminal in self.get_nao_terminais():
                # para cada produção do não terminal, fazer checagens
                for producao in nao_terminal.producoes:
                    first_producao = producao[0]

                    if first_producao in set(self.get_terminais()) | set_epsilon:
                        # se a primeira produção é um terminal, adicionar no set do não terminal
                        nao_terminal.firsts.add(first_producao)
                    else:
                        # se não, fazer checagem se todos os símbolos da produção contém &
                        for simbolo in producao:
                            nao_terminal.firsts.update(simbolo.firsts - set_epsilon)
                            if epsilon not in simbolo.firsts:
                                break
                        else:
                            # se tiver, adiciona o próprio &
                            nao_terminal.firsts.add(epsilon)

            # checar parada com as cópias dos firsts
            has_change = False
            for k, simbolo in enumerate(self.simbolos):
                if firsts_copy[k] != simbolo.firsts:
                    has_change = True
                    break

            if not has_change:
                break

    def get_follows(self):
        """
        Preenche os Follows, para fazer o analisador sintático LL(1)
        """
        epsilon = self.find_symbol("&")
        set_epsilon = {epsilon}
        nao_terminais = self.get_nao_terminais()

        while True:
            follows_copy = []

            # para cada terminal, adiciona ele próprio em seus follows
            for simbolo in self.simbolos:
                follows_copy.append(frozenset(simbolo.follows))

            for nao_terminal in nao_terminais:
                if nao_terminal == self.simbolo_inicial:
                    # se for o símbolo inicial da gramática,
                    # adiciona o símbolo inicial de pilha
                    nao_terminal.follows.add(self.find_symbol("$"))
                    continue

                for producao in nao_terminal.producoes:
                    for k, simbolo in enumerate(producao):
                        if not simbolo.is_terminal():
                            try:
                                next_symbol = producao[k + 1]
                                simbolo.follows.update(next_symbol.firsts - set_epsilon)
                            except IndexError:
                                pass
                            for i in range(k+1, len(producao)-1):
                                if epsilon in producao[i].firsts:
                                    next_ = producao[i+1]
                                    simbolo.follows.update(next_.firsts - set_epsilon)
                    for i in range(len(producao) - 1, -1, -1):
                        symbol_now = producao[i]
                        if not symbol_now.is_terminal():
                            break
                        symbol_now.follows.update(nao_terminal.follows)
                        if epsilon not in symbol_now.firsts:
                            break

            # checar parada com as cópias dos follows
            has_change = False
            for k, simbolo in enumerate(self.simbolos):
                if follows_copy[k] != simbolo.follows:
                    has_change = True
                    break

            if not has_change:
                break

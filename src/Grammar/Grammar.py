import random
import string
from typing import List, Union

from src.Exceptions.Syntactic.LoopNaoDeterminismoException import LoopNaoDeterminismoException
from src.Exceptions.Syntactic.NotLL1Exception import NotLL1Exception
from src.Grammar.Symbol import Symbol

# flags
MAX_EXECUTION_NAO_DETERMINISMO = 50  # quantidade máxima de "loops" em não determinismo


class Grammar:
    """
    Implementação de uma gramática, a fim de fazer operações importantes para análise sintática
    """
    def __init__(self):
        self.simbolos: List[Symbol] = []
        self.simbolo_inicial: Union[Symbol, None] = None

    def parse_file(self, file_name: str):
        """
        Faz parse de um arquivo de gramática
        :param file_name: Path do arquivo de entrada
        """
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

    def has_symbol(self, simbolo: str) -> bool:
        """
        Checa se já existe um símbolo
        :param simbolo: Símbolo de busca
        :return: Se já existe ou não o símbolo na gramática
        """
        try:
            self.get_symbol(simbolo)
            return True
        except StopIteration:
            return False

    def generate_random_symbol(self) -> Symbol:
        """
        Retorna um símbolo não terminal ainda não presente na gramática (para implementar novos símbolos não terminais)
        :return: Novo símbolo não terminal da gramática
        """
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
                raise LoopNaoDeterminismoException

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

            # fazer cópia dos dos símbolos firsts
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
        def get_next(k_now):
            set_now = set()
            if k_now >= len(producao):
                return set_now

            symbol_now = producao[k_now]
            firsts_now = symbol_now.firsts
            set_now.update(firsts_now)

            if symbol_now.is_terminal():
                return set_now
            elif epsilon in firsts_now:
                return set_now.update(get_next(k_now + 1))

        def get_previous(k_now):
            if k_now == -1:
                return

            symbol_now = producao[k_now]
            if symbol_now.is_terminal():
                return

            symbol_now.follows.update(nao_terminal.follows)

            if epsilon in symbol_now.firsts:
                get_previous(k_now - 1)

        epsilon = self.find_symbol("&")
        set_epsilon = {epsilon}
        nao_terminais = self.get_nao_terminais()

        while True:
            follows_copy = []

            # fazer cópia dos follows dos símbolos
            for simbolo in self.simbolos:
                follows_copy.append(frozenset(simbolo.follows))

            # primeira regra: símbolo de final de pilha no símbolo inicial
            self.simbolo_inicial.follows.add(self.find_symbol("$"))

            # para cada não terminal, executar as regras 2 e 3
            for nao_terminal in nao_terminais:
                for producao in nao_terminal.producoes:
                    # segunda regra: ida
                    for k, simbolo in enumerate(producao):
                        if simbolo.is_terminal() or k == len(producao) - 1:
                            continue

                        next_symbol = producao[k+1]
                        firsts_next = next_symbol.firsts

                        simbolo.follows.update(firsts_next - set_epsilon)
                        if epsilon in firsts_next:
                            simbolo.follows.update(get_next(k+2))

                    # terceira regra: volta
                    for k in range(len(producao)-1, -1, -1):
                        simbolo = producao[k]
                        if simbolo.is_terminal():
                            break

                        simbolo.follows.update(nao_terminal.follows)
                        if epsilon in simbolo.firsts:
                            get_previous(k - 1)
                            break

            # checar parada com as cópias dos follows
            has_change = False
            for k, simbolo in enumerate(self.simbolos):
                if follows_copy[k] != simbolo.follows:
                    has_change = True
                    break

            if not has_change:
                break

    def is_ll1(self):
        """
        Para que uma gramática possa ser convertida em um analisador sintático LL(1),
        é necessário que não seja recursiva à esquerda, que esteja na forma fatorada
        (sem não determinismo) e que a interseção dos firsts dos símbolos que contém
        epsilon com seus respectivos follows seja nulo.
        :return: Se é aceito converter para LL(1)
        :raise NotLL1Exception Caso não seja compatível com analisador sintático LL(1)
        """
        symbols_first_null = [x for x in self.simbolos if self.find_symbol("&") in x.firsts]

        for simbolo in symbols_first_null:
            if len(simbolo.firsts.intersection(simbolo.follows)) != 0:
                raise NotLL1Exception
        return True

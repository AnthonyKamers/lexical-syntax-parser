from typing import List

from src.utils.utils import subtract_listas


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

    def is_left_recursive(self) -> bool:
        return self.is_left_recursive_check(self)

    def is_left_recursive_check(self, symbol_check) -> bool:
        # checar produções diretas
        if len(self.find_producoes_start(self)) > 0:
            return True

        # checar produções indiretas
        for producao in self.producoes:
            first = producao[0]
            if not first.is_terminal:
                result = first.is_left_recursive_check(symbol_check)
                if result:
                    return True
        return False

    def is_recursive(self) -> bool:
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
                    result = symbol.is_recursive_check(symbol_check)
                    if result:
                        return True
        return False

    def remove_nao_determinismo_direto(self) -> bool:
        changed = False
        for k1, prod1 in enumerate(self.producoes):
            for k2, prod2 in enumerate(self.producoes):
                if prod1 == prod2 or len(prod1) == 1 or len(prod2) == 1:
                    continue

                # tem determinismo direto
                if prod1[0] == prod2[0]:
                    first_prod = prod1[0]

                    # gerar novo símbolo aleatório
                    # new_symbol = self.grammar.generate_random_symbol()

                    # gerar novo símbolo com base nesse
                    new_symbol = self.grammar.find_symbol(self.simbolo + "'")

                    # trocar produção antiga por novo símbolo
                    resto_1 = prod1[1:]
                    resto_2 = prod2[1:]

                    new_symbol.producoes = [resto_1, resto_2]

                    self.producoes[k1] = [first_prod, new_symbol]
                    self.producoes.pop(k2)
                    changed = True

        return changed

    def transforma_nao_determinismo_indireto(self) -> bool:
        def check_terminais_nao_terminal(nao_terminal) -> List[any]:
            producoes_nao_terminal: List[any] = nao_terminal.producoes
            terminais_now = []

            for prod in producoes_nao_terminal:
                first_prod = prod[0]
                if first_prod.is_terminal:
                    terminais_now.append(first_prod)
                else:
                    terminais_now = terminais_now + check_terminais_nao_terminal(first_prod)
            return terminais_now

        def transform_nao_terminal_in_terminal(nao_terminal_now):
            producoes_start = self.find_producoes_start(nao_terminal_now)

            # para cada produção, substituir o primeiro elemento
            # com as produções deste símbolo
            for producao in producoes_start:
                self.producoes.remove(producao)

                resto = producao[1:]
                for producao_simbolo in nao_terminal_now.producoes:
                    new_producao = [x for x in producao_simbolo]
                    new_producao = new_producao + resto
                    self.producoes.append(new_producao)

        def check_other_terminais(terminal_now) -> bool:
            # é terminal, apenas ver se outros não terminais levam para ele
            flag, search_list = self.search_other_symbol(terminal_now, prod1, [])

            # encontrou resultado
            if flag:
                symbol_find = search_list[0]
                transform_nao_terminal_in_terminal(symbol_find)

                # retorna que houve mudança
                return True
            return False

        for k1, prod1 in enumerate(self.producoes):
            first_search = prod1[0]
            if first_search.is_terminal:
                flag_check = check_other_terminais(first_search)

                # retornar a cada mudança na lista, para não
                # quebrar a integridade da gramática
                if flag_check:
                    return True
            else:
                # não terminal, é necessário ver para quais terminais ele leva e
                # checar se há outros não terminais que também levam para tais terminais
                # OBS: não precisa se preocupar com recursão à esquerda,
                # porque foi removida anteriormente

                # checar quais são seus terminais
                flag_check = False
                terminais = check_terminais_nao_terminal(first_search)
                for terminal in terminais:
                    flag_check = flag_check or check_other_terminais(terminal)

                # se houve mudança, mudar as suas próprias produções
                if flag_check:
                    transform_nao_terminal_in_terminal(first_search)
                    return True
        return False

    def find_producoes_start(self, symbol):
        return [x for x in self.producoes if x[0] == symbol]

    def search_other_symbol(self, search, prod_start, search_list):
        producoes: List[any] = [x for x in self.producoes if x != prod_start]
        for prod in producoes:
            first_prod = prod[0]

            if first_prod.is_terminal and first_prod == search and len(search_list) > 0:
                return True, search_list
            else:
                search_list.append(first_prod)
                return first_prod.search_other_symbol(search, prod, search_list)
        return False, search_list

    def remove_recursao_esquerda_direta(self):
        if self.is_left_recursive():
            producoes_symbol = self.find_producoes_start(self)
            producoes_not_symbol = subtract_listas(self.producoes, producoes_symbol)
            new_symbol = self.grammar.generate_random_symbol()

            # adicionar símbolo novo nas produções
            # que não contém o símbolo à esquerda
            for producao in producoes_not_symbol:
                producao.append(new_symbol)

            # preencher o new_symbol e remover das produções deste símbolo
            for producao in producoes_symbol:
                self.producoes.remove(producao)
                producao_sem_primeiro = producao[1:]
                producao_sem_primeiro.append(new_symbol)
                new_symbol.producoes.append(producao_sem_primeiro)

            # adicionar &
            epsilon = self.grammar.find_symbol("&")
            epsilon.is_terminal = True
            new_symbol.producoes.append([epsilon])

    def remove_recursao_esquerda_indireta(self, symbol_remove) -> bool:
        producoes_start = self.find_producoes_start(symbol_remove)

        if len(producoes_start) == 0:
            return False

        for producao in producoes_start:
            self.producoes.remove(producao)
            resto = producao[1:]

            for producao_symbol in symbol_remove.producoes:
                producao_new = producao_symbol + resto
                self.producoes.append(producao_new)
        return True

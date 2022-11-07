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
                    new_symbol = self.grammar.generate_random_symbol()

                    # trocar produção antiga por novo símbolo
                    resto_1 = prod1[1:]
                    resto_2 = prod2[1:]

                    new_symbol.producoes = [resto_1, resto_2]

                    self.producoes[k1] = [first_prod, new_symbol]
                    self.producoes.pop(k2)
                    changed = True

        return changed

    def transforma_nao_determinismo_indireto(self) -> bool:
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
                terminais = self.check_terminais_nao_terminal(first_search)
                for terminal in terminais:
                    flag_check = flag_check or check_other_terminais(terminal)

                # se houve mudança, mudar suas próprias produções
                if flag_check:
                    transform_nao_terminal_in_terminal(first_search)
                    return True
        return False

    @staticmethod
    def check_terminais_nao_terminal(nao_terminal) -> List[any]:
        producoes_nao_terminal: List[any] = nao_terminal.producoes
        terminais = []

        for prod in producoes_nao_terminal:
            first_prod = prod[0]
            if first_prod.is_terminal:
                terminais.append(first_prod)
            else:
                terminais = terminais + first_prod.check_terminais_nao_terminal(first_prod)
        return terminais

    def find_producoes_start(self, symbol):
        return [x for x in self.producoes if x[0] == symbol]

    def search_other_symbol(self, search, prod_start, search_list):
        producoes: List[any] = [x for x in self.producoes if x != prod_start]
        for prod in producoes:
            first_prod = prod[0]

            if first_prod.is_terminal and first_prod == search:
                return True, search_list
            else:
                search_list.append(first_prod)
                return first_prod.search_other_symbol(search, prod, search_list)
        return False, search_list

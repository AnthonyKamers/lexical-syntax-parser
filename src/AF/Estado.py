from typing import Tuple, List


class Estado:
    def __init__(self, nome: str, af):
        self.nome: str = nome
        self.transicoes: List[Tuple[str, str]] = []
        self.af = af
        self.is_deterministico: bool = True

    def add_transicao(self, letra_alfabeto: str, estado: str):
        self.transicoes.append((letra_alfabeto, estado))

    def next_estado(self, letra_alfabeto: str):
        tuplas = [x for x in self.transicoes if x[0] == letra_alfabeto]
        estados_nomes = [b for a, b in tuplas]
        estados_list = tuple(map(lambda x: self.af.get_estado(x), estados_nomes))
        return estados_list

from __future__ import annotations
from typing import Tuple, List, Union


class Estado:
    # FIXME: Necessário trocar as estruturas de dados de lista para set
    def __init__(self, nome: str):
        self.nome: str = nome
        self.transicoes: List[Tuple[str, Estado, any]] = []

        # é necessário gravar quais estados
        # fazem parte de uma determinização
        self.estados: List[Estado] = []

    def add_transicao(self, letra_alfabeto: str, estado: Estado, af: Union[None, any] = None):
        if estado not in self.next_estado(letra_alfabeto):
            self.transicoes.append((letra_alfabeto, estado, af))

    def next_estado(self, letra_alfabeto: str) -> List[Estado]:
        tuplas = [x for x in self.transicoes if x[0] == letra_alfabeto]
        return [b for _, b, _ in tuplas]

    def remove_transicao(self, letra_alfabeto: str):
        self.transicoes = [tupla for tupla in self.transicoes if tupla[0] != letra_alfabeto]

    def change_estado_nome(self):
        self.nome = self.nome + "'"

    def add_estados(self, estados: List[Estado]):
        for estado in estados:
            self.add_estado(estado)

    def add_estado(self, estado: Estado):
        if estado not in self.estados:
            self.estados.append(estado)

    def has_letra_transicao(self, letra: str):
        tuplas = [x for x in self.transicoes if x[0] == letra]
        return len(tuplas) > 0

    def has_estado_transicao(self, estado: Estado) -> bool:
        tuplas = [x for x in self.transicoes if x[1] == estado]
        return len(tuplas) > 0

    def has_afd_transicao(self) -> bool:
        tuplas = [x for x in self.transicoes if x[2] is not None]
        return len(tuplas) > 0

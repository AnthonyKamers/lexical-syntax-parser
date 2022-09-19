from __future__ import annotations
from typing import Tuple, List


class Estado:
    def __init__(self, nome: str, af):
        self.nome: str = nome
        self.transicoes: List[Tuple[str, Estado]] = []
        self.af = af

    def add_transicao(self, letra_alfabeto: str, estado: Estado):
        self.transicoes.append((letra_alfabeto, estado))

    def next_estado(self, letra_alfabeto: str):
        tuplas = [x for x in self.transicoes if x[0] == letra_alfabeto]
        return [b for a, b in tuplas]

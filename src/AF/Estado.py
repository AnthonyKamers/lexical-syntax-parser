from __future__ import annotations
from typing import Tuple, List


class Estado:
    def __init__(self, nome: str):
        self.nome: str = nome
        self.transicoes: List[Tuple[str, Estado]] = []

    def add_transicao(self, letra_alfabeto: str, estado: Estado):
        self.transicoes.append((letra_alfabeto, estado))

    def next_estado(self, letra_alfabeto: str) -> List[Estado]:
        tuplas = [x for x in self.transicoes if x[0] == letra_alfabeto]
        return [b for a, b in tuplas]

    def change_estado_nome(self):
        self.nome = self.nome + "'"

from __future__ import annotations
from typing import Tuple, List


class Estado:
    def __init__(self, nome: str):
        self.nome: str = nome
        self.transicoes: List[Tuple[str, Estado]] = []

        # é necessário gravar quais estados
        # fazem parte de uma determinização
        self.estados: List[Estado] = []

    def add_transicao(self, letra_alfabeto: str, estado: Estado):
        if estado not in self.next_estado(letra_alfabeto):
            self.transicoes.append((letra_alfabeto, estado))

    def next_estado(self, letra_alfabeto: str) -> List[Estado]:
        tuplas = [x for x in self.transicoes if x[0] == letra_alfabeto]
        return [b for a, b in tuplas]

    def change_estado_nome(self):
        self.nome = self.nome + "'"

    def add_estado(self, estado: Estado):
        if estado not in self.estados:
            self.estados.append(estado)

    def has_estado_transicao(self, estado: Estado) -> bool:
        tuplas = [x for x in self.transicoes if x[1] == estado]
        return True if len(tuplas) > 0 else False

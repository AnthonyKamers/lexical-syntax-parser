from typing import List, Union

from src.AF.Estado import Estado


# Classe de Equivalência
class CE:
    def __init__(self, estados: Union[List[Estado], Estado] = []):
        self.estados: List[Estado] = estados if isinstance(estados, list) else [estados]
        self.transicao: Union[CE, None] = self
        self.is_f: bool = False

    def add_estado(self, estado: Estado):
        self.estados.append(estado)

    def remove_estado(self, estado: Estado):
        self.estados.remove(estado)

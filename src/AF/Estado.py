from __future__ import annotations
from typing import Tuple, List, Union


class Estado:
    """
    Representação de um estado de um AF
    """

    # FIXME: Necessário trocar as estruturas de dados de lista para set
    def __init__(self, nome: str):
        self.nome: str = nome
        self.transicoes: List[Tuple[str, Estado, any]] = []

        # é necessário gravar quais estados
        # fazem parte de uma determinização
        self.estados: List[Estado] = []

    def add_transicao(self, letra_alfabeto: str, estado: Estado, af: Union[None, any] = None):
        """
        Adiciona transição de uma letra para um estado
        :param letra_alfabeto: Letra pela qual faz transição
        :param estado: Estado para o qual transita por letra_alfabeto
        :param af: Em caso de autômatos que derivam de outros, é necessário este atributo para manter histórico
        """
        if estado not in self.next_estado(letra_alfabeto):
            self.transicoes.append((letra_alfabeto, estado, af))

    def next_estado(self, letra_alfabeto: str) -> List[Estado]:
        """
        Pega quais as transições por letra_alfabeto
        :param letra_alfabeto: Letra para qual deseja transitar
        :return: Lista de estados para o qual pode transitar
        """
        tuplas = [x for x in self.transicoes if x[0] == letra_alfabeto]
        return [b for _, b, _ in tuplas]

    def remove_transicao(self, letra_alfabeto: str):
        """
        Remove transição por alguma letra do alfabeto
        :param letra_alfabeto: Transição que deseja ser removida
        """
        self.transicoes = [tupla for tupla in self.transicoes if tupla[0] != letra_alfabeto]

    def change_estado_nome(self):
        """
        Muda o nome do estado genericamente, para conseguir distinguir em um debug
        """
        self.nome = self.nome + "'"

    def add_estados(self, estados: List[Estado]):
        """
        Adiciona uma lista de estados para o qual é derivado (no algoritmo de determinização)
        :param estados: Estados para os quais pode derivar (em uma determinização)
        """
        for estado in estados:
            self.add_estado(estado)

    def add_estado(self, estado: Estado):
        """
        Adiciona apenas um estado no algoritmo de determinização
        :param estado: Estado que deseja recordar no algoritmo de determinização
        :return:
        """
        if estado not in self.estados:
            self.estados.append(estado)

    def has_letra_transicao(self, letra: str) -> bool:
        """
        Retorna se o estado possui transição por determinada letra do alfabeto
        :param letra: Letra de transição
        :return: Se possui transição por letra
        """
        tuplas = [x for x in self.transicoes if x[0] == letra]
        return len(tuplas) > 0

    def has_estado_transicao(self, estado: Estado) -> bool:
        """
        Checar se estado transita para estado
        :param estado: Estado de checagem
        :return: Se estado atual possui transição para estado
        """
        tuplas = [x for x in self.transicoes if x[1] == estado]
        return len(tuplas) > 0

    def has_afd_transicao(self) -> bool:
        """
        Checa se é derivado de algum outro AF
        :return: Se possui alguma derivação de outro AF (para manter histórico de ER)
        """
        tuplas = [x for x in self.transicoes if x[2] is not None]
        return len(tuplas) > 0

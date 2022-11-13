from typing import List


def pretty_print_matrix(matrix: List[List[str]]) -> None:
    """
    Printa uma tabela 2x2 de maneira agradável
    contribuição por:
        https://stackoverflow.com/questions/13214809/pretty-print-2d-list
    :param matrix: Tabela 2x2
    """
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


def remove_duplicates_lista(lista: List[any]) -> List[any]:
    """
    Remove duplicadas de uma lista (mesmo procedimento de um Set())
    :param lista: Lista que deseja remover duplicatas
    :return: Lista sem duplicatas
    """
    return list(dict.fromkeys(lista))


def subtract_listas(lista1: List[any], lista2: List[any]) -> List[any]:
    """
    Método genérico para fazer a subtração de duas listas (o que tem em lista1 que não tem em lista2)
    :param lista1: Lista primária da subtração
    :param lista2: Lista secundária da subtração
    :return: A diferença entre lista1 e lista2
    """
    return [x for x in lista1 if x not in lista2]

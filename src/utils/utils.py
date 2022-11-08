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
    return list(dict.fromkeys(lista))


def subtract_listas(lista1: List[any], lista2: List[any]) -> List[any]:
    return [x for x in lista1 if x not in lista2]

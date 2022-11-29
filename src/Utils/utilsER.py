from typing import List

from src.ER.Node import Node


def get_lowercase_letters() -> List[str]:
    """
    Retorna lista com operação OR entre alfabeto em minúsculo (para Regex)
    :return: Entradas do alfabeto separadas por operando OR
    """
    return add_or_operation(list(map(chr, range(ord('a'), ord('z') + 1))))


def get_uppercase_letters() -> List[str]:
    """
    Retorna lista com operação OR entre alfabeto em maiúsculo (para Regex)
    :return: Entradas do alfabeto separadas por operando OR
    """
    return add_or_operation(list(map(chr, range(ord('A'), ord('Z') + 1))))


def get_all_letters() -> List[str]:
    """
    Retorna lista com operação OR entre alfabeto em minúsculo e maiúsculo (para Regex)
    :return: Entradas do alfabeto separadas por operando OR
    """
    return get_lowercase_letters() + ["|"] + get_uppercase_letters()


def get_numbers() -> List[str]:
    """
    Retorna lista com operação OR entre números naturais (para Regex)
    :return: Entradas de números separados por operando OR
    """
    return add_or_operation(list(map(str, range(0, 10))))


def add_or_operation(lista: List[str]) -> List[str]:
    """
    Função genérica para adicionar operando OR entre duas entradas de uma lista
    :param lista: Lista que deseja adicionar o operando OR
    :return: Lista de elementos separados por operando OR
    """
    for i in range(1, len(lista) * 2, 2):
        lista.insert(i, "|")
    return lista[:-1]


COUNT = [10]


def print_tree(root: Node, space: int):
    """
    Printta uma árvore lateralmente: inorder.
    Retirado de: https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
    :param root: Nodo sendo visto no momento
    :param space: Quantidade de itens a deslocar à direita no terminal
    """
    # Base case
    if root is None:
        return

    # Increase distance between levels
    space += COUNT[0]

    # Process right child first
    print_tree(root.right, space)

    # Print current node after space
    # count
    print()
    for i in range(COUNT[0], space):
        print(end=" ")
    print(root.el)

    # Process left child
    print_tree(root.left, space)

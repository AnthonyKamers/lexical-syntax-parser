from typing import List


def get_lowercase_letters(make_epsilon: bool = True):
    lista = ["a"]
    if make_epsilon:
        lista.append("|")
        lista.append("&")
    return [lista, "|", *add_or_operation(list(map(chr, range(ord('b'), ord('z') + 1))))] if make_epsilon else \
        [*lista, "|", *add_or_operation(list(map(chr, range(ord('b'), ord('z') + 1))))]


def get_uppercase_letters(make_epsilon: bool = True):
    lista = ["A"]
    if make_epsilon:
        lista.append("|")
        lista.append("&")
    return [lista, "|", *add_or_operation(list(map(chr, range(ord('B'), ord('Z') + 1))))] if make_epsilon else \
        [*lista, "|", *add_or_operation(list(map(chr, range(ord('B'), ord('Z') + 1))))]


def get_all_letters():
    return get_lowercase_letters(True) + ["|"] + get_uppercase_letters(False)


def get_numbers():
    return [["0", "|", "&"], "|", *add_or_operation(list(map(str, range(1, 10))))]


def add_or_operation(lista: List[str]) -> List[str]:
    for i in range(1, len(lista) * 2, 2):
        lista.insert(i, "|")
    return lista[:-1]

# entre_parentesis = content[content.find("(") + 1:content.find(")")]

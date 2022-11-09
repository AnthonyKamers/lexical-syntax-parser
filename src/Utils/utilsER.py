from typing import List


def get_lowercase_letters() -> List[str]:
    return add_or_operation(list(map(chr, range(ord('a'), ord('z') + 1))))


def get_uppercase_letters() -> List[str]:
    return add_or_operation(list(map(chr, range(ord('A'), ord('Z') + 1))))


def get_all_letters() -> List[str]:
    return get_lowercase_letters() + ["|"] + get_uppercase_letters()


def get_numbers() -> List[str]:
    return add_or_operation(list(map(str, range(0, 10))))


def add_or_operation(lista: List[str]) -> List[str]:
    for i in range(1, len(lista) * 2, 2):
        lista.insert(i, "|")
    return lista[:-1]

# entre_parentesis = content[content.find("(") + 1:content.find(")")]

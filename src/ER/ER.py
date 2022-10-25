from typing import Union, Tuple
from enum import Enum

from src.utils.utilsER import *

caracteres_especiais = ["(", "|", "*", "?", "+", ")"]
order_preference = ["#", "*", ".", "|"]


class Operation(Enum):
    CLOSE = 4,
    FECHO = 3,
    CONCAT = 2
    OR = 1
    ELEMENT = 0


class Node:
    def __init__(self, el, operation: Operation):
        self.el = el
        self.op = operation
        self.left = None
        self.right = None


class ER:
    def __init__(self):
        self.er = {}
        self.er_tree = {}

    def __repr__(self):
        return "ER()"

    def parse_file(self, file_name: str):
        def get_parenthesis(cont: str, index_: int) -> Tuple[List[Union[str, List[str]]], int, str]:
            lista = []
            palavra_now: str = ""
            substring: str = cont[index_:len(cont)]
            for index, character in enumerate(substring):
                if character not in caracteres_especiais:
                    palavra_now += character
                else:
                    # TODO: if character == "(" não sendo tratado aqui

                    if character == "|":
                        if palavra_now != "":
                            lista.append(palavra_now)
                        lista.append(character)
                        palavra_now = ""
                    elif character == "*":
                        lista.append(character)
                    elif character == "?":
                        pass
                    elif character == "+":
                        pass
                    elif character == ")":
                        lista.append(palavra_now)
                        return lista, index + 1, substring

        def parse_content(cont: str, index_: int) -> List[Union[str, List[str]]]:
            palavra_now = ""
            lista: List[Union[str, List[str]]] = []
            substring: str = cont[index_:len(cont)]

            for index, character in enumerate(substring):
                if character not in caracteres_especiais:
                    palavra_now += character
                else:
                    if character == "(":
                        if palavra_now != "":
                            lista.append(palavra_now)
                        lista_nova, index_novo, substring_novo = get_parenthesis(substring, index + 1)
                        lista.append(lista_nova)
                        lista = lista + parse_content(substring_novo, index_novo)
                        break
                    elif character == "|":
                        lista.append(palavra_now)
                        lista.append(character)
                        palavra_now = ""
                    elif character == "*":
                        lista.append(character)
                    elif character == "?":
                        pass
                    elif character == "+":
                        pass
            return lista

        with open(file_name) as file:
            for line in file:
                line = line.replace(" ", "").replace("\n", "")
                key: str
                content: str
                key, content = line.split(":")

                if "[0-9]" in content:
                    self.er[key] = get_numbers()
                elif "[a-zA-Z]" in content:
                    self.er[key] = get_all_letters()
                elif "[a-z]" in content:
                    self.er[key] = get_lowercase_letters()
                elif "[A-Z]" in content:
                    self.er[key] = get_uppercase_letters()
                else:
                    # another type of ER, parse it
                    self.er[key] = parse_content(content, 0)

    def construct_syntactic_tree(self):
        def make_node_concat(lista: list) -> Node:
            if isinstance(lista, str):
                # é operador
                if lista == "*":
                    return Node(lista, Operation.FECHO)

            if len(lista) == 1:
                return Node(lista[0], Operation.ELEMENT)

            # é uma lista, faz recursão
            for op_ in order_preference:
                try:
                    index = lista.index(op_)
                    subset_left = lista[0:index]
                    subset_right = lista[index + 1:len(lista)]

                    if op_ == "*":
                        operation = Operation.FECHO
                    elif op_ == "|":
                        operation = Operation.OR
                    else:
                        operation = Operation.CONCAT

                    node = Node(op_, operation)
                    node.left = make_node_concat(subset_left)
                    node.right = make_node_concat(subset_right)

                    break
                except ValueError:
                    pass

            return node

        for key, value in self.er.items():
            operations = []

            # construir prioridades
            for el_now in value:
                if el_now == "*":
                    operations.append(Operation.FECHO)
                elif el_now == "|":
                    operations.append(Operation.OR)
                elif isinstance(el_now, list):
                    operations.append(Operation.CONCAT)
                else:
                    operations.append(Operation.ELEMENT)

            # inicia de qualquer maneira o nodo (somente para iniciar)
            node_now: Node = Node("", Operation.CLOSE)
            first_run = True
            while len(value) != 0:
                first = value.pop(0)
                first_op = operations.pop(0)

                # iniciar node_aux com qualquer valor
                node_aux: Node = Node("", Operation.CLOSE)

                # ver qual operação estou fazendo no momento
                if first_op == Operation.CONCAT:
                    node_aux1 = make_node_concat(first)

                    if not first_run:
                        node_aux = Node(".", Operation.CONCAT)
                        node_aux.left = node_now
                        node_aux.right = node_aux1
                        node_now = node_aux
                    else:
                        node_aux = node_aux1
                elif first_op == Operation.FECHO:
                    node_aux = Node(first, first_op)

                    last_right = node_now.right
                    node_aux.right = last_right
                    node_now.right = node_aux
                elif first_op == Operation.OR:
                    node_aux = Node(first, first_op)
                    node_aux.left = node_now
                    node_now = node_aux
                elif first_op == Operation.ELEMENT:
                    node_aux = Node(first, first_op)
                    node_now.right = node_aux

                # fazer checagens de parada e de primeira instância
                if first_run:
                    node_now = node_aux
                    first_run = False

            father_final = Node(".", Operation.CONCAT)
            father_final.left = node_now
            father_final.right = Node("#", Operation.CLOSE)

            # adiciona no dicionário a árvore construída
            self.er_tree[key] = father_final

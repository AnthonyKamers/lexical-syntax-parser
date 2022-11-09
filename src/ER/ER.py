import copy
from typing import Union, Tuple
from enum import Enum

from src.AF.AF import AF
from src.AF.Estado import Estado
from src.Utils.utilsER import *

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
        self.left: Union[None, Node] = None
        self.right: Union[None, Node] = None
        self.father: Union[None, Node] = None
        self.first_pos = set()
        self.last_pos = set()
        self.follow_pos = set()

    def __repr__(self):
        return self.el

    def is_nullable(self) -> bool:
        if self.op == Operation.CONCAT:
            return self.left.is_nullable() and self.right.is_nullable()
        elif self.op == Operation.OR:
            return self.left.is_nullable() or self.right.is_nullable()
        elif self.op == Operation.FECHO:
            return True
        elif self.op == Operation.CLOSE:
            return False
        elif self.op == Operation.ELEMENT:
            return self.el == "&"

    def get_first_pos(self):
        if self.op == Operation.CONCAT:
            if self.left.is_nullable():
                return self.left.get_first_pos().union(self.right.get_first_pos())
            else:
                return self.left.get_first_pos()
        elif self.op == Operation.OR:
            return self.left.get_first_pos().union(self.right.get_first_pos())
        elif self.op == Operation.FECHO:
            return self.right.get_first_pos()
        elif self.op in (Operation.CLOSE, Operation.ELEMENT):
            return self.first_pos

    def get_last_pos(self):
        if self.op == Operation.CONCAT:
            if self.right.is_nullable():
                return self.right.get_last_pos().union(self.left.get_last_pos())
            else:
                return self.right.get_last_pos()
        elif self.op == Operation.OR:
            return self.right.get_last_pos().union(self.left.get_last_pos())
        elif self.op == Operation.FECHO:
            return self.right.get_last_pos()
        elif self.op in (Operation.CLOSE, Operation.ELEMENT):
            return self.last_pos


class ER:
    def __init__(self):
        self.er = {}
        self.er_tree = {}
        self.afds = {}

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
                        lista.append(character)
                    elif character == "+":
                        lista.append(character)
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
                        if palavra_now != "":
                            lista.append(palavra_now)
                        lista.append(character)
                        palavra_now = ""
                    elif character == "*":
                        lista.append(character)
                    elif character == "?":
                        if palavra_now != "":
                            lista.append(palavra_now)
                        lista.append(character)
                        palavra_now = ""
                    elif character == "+":
                        if palavra_now != "":
                            lista.append(palavra_now)
                        lista.append(character)
                        palavra_now = ""
            return lista

        def treat_exceptions(parsed):
            # busca por ?
            for k, el in enumerate(parsed):
                if el == "?":
                    before = parsed[k-1]

                    # substituir no índice k-1
                    parsed[k-1] = [before, "|", "&"]

                    # remover índice k
                    parsed.pop(k)

            # busca por +
            for k, el in enumerate(parsed):
                if el == "+":
                    before = parsed[k-1]

                    # substituir no índice k
                    parsed[k] = before

                    # adicionar fecho no próximo elemento
                    parsed.insert(k+1, "*")

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
                    er_parsed = parse_content(content, 0)
                    treat_exceptions(er_parsed)
                    self.er[key] = er_parsed

    def make_afd_er(self):
        self.construct_syntactic_tree()
        self.make_followpos()

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

                    return node
                except ValueError:
                    pass

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
            first_operator: Union[None, Operation] = None
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

                        # atualizar nodo pai
                        node_now.father = node_aux
                        node_aux1.father = node_aux

                        # atualizar node_now
                        node_now = node_aux
                    else:
                        node_aux = node_aux1
                elif first_op == Operation.FECHO:
                    node_aux = Node(first, first_op)

                    last_right = node_now.right
                    node_aux.right = last_right
                    node_now.right = node_aux

                    # atualizar nodo pai
                    last_right.father = node_aux
                    node_aux.father = node_now
                elif first_op == Operation.OR:
                    node_aux = Node(first, first_op)

                    if node_now.op == Operation.OR:
                        # atualizar para o lado esquerdo
                        node_aux.left = node_now.right
                        node_aux.left.father = node_aux

                        # atualizar node_now
                        node_aux.father = node_now
                        node_now.right = node_aux
                        node_now = node_aux
                    else:
                        node_aux.left = node_now

                        # atualizar nodo pai
                        node_now.father = node_aux

                        # atualizar node_now
                        node_now = node_aux
                elif first_op == Operation.ELEMENT:
                    node_aux = Node(first, first_op)
                    node_now.right = node_aux

                    # atualizar nodo pai
                    node_aux.father = node_now

                # fazer checagens de parada e de primeira instância
                if first_run:
                    node_now = node_aux
                    first_run = False

                # ver qual foi o primeiro operador
                if first_operator is None and first_op in (Operation.OR, Operation.CONCAT):
                    first_operator = first_op

            # ver quem é o nodo pai, pelo primeiro operador
            # se for OR, tem que fazer recursão com o enésimo pai
            if first_operator == Operation.OR:
                while node_now.father is not None:
                    node_now = node_now.father

            # fazer nodo de finalização
            node_close = Node("#", Operation.CLOSE)

            # fazer nodo pai final
            father_final = Node(".", Operation.CONCAT)
            father_final.left = node_now
            father_final.right = node_close

            # atualizar nodo pai
            node_close.father = father_final
            node_now.father = father_final

            # adiciona no dicionário a árvore construída
            self.er_tree[key] = father_final

    def make_followpos(self):
        def mark_elements(node: Node):
            if node is None:
                return

            # check its first and last pos
            if (node.op == Operation.ELEMENT and node.el != "&") or \
                    node.op == Operation.CLOSE:
                node.first_pos.add(node)
                node.last_pos.add(node)

            mark_elements(node.right)
            mark_elements(node.left)

        def mark_follow_pos(node: Node):
            if node is None:
                return

            if node.op == Operation.CONCAT:
                c2_first_pos = node.right.get_first_pos()
                for i in node.left.get_last_pos():
                    i.follow_pos = i.follow_pos.union(c2_first_pos)

            elif node.op == Operation.FECHO:
                for i in node.get_last_pos():
                    i.follow_pos = i.follow_pos.union(node.get_first_pos())

            mark_follow_pos(node.right)
            mark_follow_pos(node.left)

        def find_identical_el(list_node: List[Node]):
            obj = {}
            for i in list_node:
                try:
                    obj[i.el].append(i)
                except KeyError:
                    obj[i.el] = [i]
            return obj

        def make_afd_estado(transition_nodes, af, estado_now):
            for transition, nodes in transition_nodes.items():
                has_afd: bool = transition in list(self.afds.keys())
                afd_link: Union[None, AF] = None if not has_afd else self.afds[transition]

                # se possui um AF, colocar no AF correspondente, para poder fazer a busca posteriomente
                if has_afd:
                    af.afds.add(afd_link)

                # ver se é preciso colocar transição no alfabeto do AFD
                if transition not in af.alfabeto and transition != "#":
                    if not has_afd:
                        if len(transition) > 1:
                            raise "Erro: Identificador deve ser declarado primeiramente"

                        # é apenas uma letra
                        af.alfabeto.append(transition)
                    else:
                        # é um AF, logo seu alfabeto vêm dele
                        for el in afd_link.alfabeto:
                            af.alfabeto.append(el)

                # pegar follow_pos dos nodes
                follow_pos = set()
                for node in nodes:
                    follow_pos = follow_pos.union(node.follow_pos)

                list_follow_pos = list(follow_pos)
                obj = find_identical_el(list_follow_pos)

                # follow_pos é zerado, não precisa fazer nada
                if len(list_follow_pos) == 0:
                    continue

                # fazer cópia dos estados anteriores, para ver
                # se o novo já existia antes, para ver se é necessário
                # fazer recusão ou não
                estados_before = copy.copy(af.estados)

                # criar estado novo ou pegar já criado
                estado_new: Estado = af.find_estado(",".join([x.el for x in list_follow_pos]))

                # colocar transição do estado antigo para este
                if has_afd:
                    # adicionar transição de todos os elementos de seu alfabeto para estado_new
                    for letra in afd_link.alfabeto:
                        estado_now.add_transicao(letra, estado_new, afd_link)
                else:
                    estado_now.add_transicao(transition, estado_new, afd_link)

                # ver se é o estado final
                if any(elem.op == Operation.CLOSE for elem in list_follow_pos) and \
                        estado_new not in af.estados_finais:
                    af.estados_finais.append(estado_new)

                # ver se é necessário fazer recursão (caso este estado
                # não tenha sido percorrido ainda
                if estado_new not in estados_before:
                    make_afd_estado(obj, af, estado_new)

        def make_afd(node: Node) -> AF:
            af_new = AF()

            # pegar nodos de maneira a identificar
            # quais são as mesmas letras de transição
            first_pos: List[Node] = list(node.get_first_pos())
            obj = find_identical_el(first_pos)

            # fazer estado inicial
            estado: Estado = af_new.find_estado(",".join([x.el for x in first_pos]))
            af_new.estado_inicial = estado

            # ver se é o estado final
            if any(elem.op == Operation.CLOSE for elem in first_pos):
                af_new.estados_finais.append(estado)

            # percorrer transições e fazer cada transição recursivamente
            make_afd_estado(obj, af_new, estado)

            # colocar último atributo
            af_new.qtd_estados = len(af_new.estados)

            # retornar o AFD construído do ER, pela
            # árvore de transformação
            return af_new

        for key, root in self.er_tree.items():
            mark_elements(root)
            mark_follow_pos(root)
            afd: AF = make_afd(root)
            self.afds[key] = afd

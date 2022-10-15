from typing import Union, Tuple

from src.utils.utilsER import *

caracteres_especiais = ["(", "|", "*", "?", "+", ")"]


class ER:
    def __init__(self):
        self.er = {}

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
                        return lista, index+1, substring

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
                        lista_nova, index_novo, substring_novo = get_parenthesis(substring, index+1)
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

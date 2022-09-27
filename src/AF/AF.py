from __future__ import annotations

import copy
from typing import List, Union
from src.AF.Estado import Estado
from src.utils.utils import pretty_print_matrix, remove_duplicates_lista


class AF:
    def __init__(self):
        self.qtd_estados: int = 0
        self.estados: List[Estado] = []
        self.estados_finais: List[Estado] = []
        self.estado_inicial: Union[Estado, None] = None
        self.alfabeto: List[str] = []
        self.is_deterministico: bool = True
        self.estado_now: Union[Estado, None] = None

        self.functions_file = {
            1: self.set_qtd_estados,
            2: self.set_estado_inicial,
            3: self.set_estados_finais,
            4: self.set_alfabeto,
            "default": self.set_transicao
        }

    def __repr__(self):
        return "AF()"

    def __str__(self):
        return f"""
            qtd estados: {self.qtd_estados},
            estado inicial: {self.estado_inicial.nome}
            estados finais: {' - '.join([x.nome for x in self.estados_finais])}
            estados: {' - '.join([x.nome for x in self.estados])}
            alfabeto: {self.alfabeto}
            deterministico: {self.is_deterministico}
        """

    def show_tabela_transicao(self) -> None:
        """
        Mostra a tabela de transição do autômato
        δ           | l1 alfabeto | ln alfabeto
        estado1     | transição   | transição
        estado2     | transição   | transiçõa
        """
        matrix: List[List[str]] = [["δ"]]
        matrix[0] = matrix[0] + self.alfabeto

        for estado in self.estados:
            estado_nome: str = ""
            if estado in self.estados_finais:
                estado_nome += "*"
            if estado == self.estado_inicial:
                estado_nome += "->"
            estado_nome += estado.nome

            line: List[str] = [estado_nome]
            for letra in self.alfabeto:
                next_estados = estado.next_estado(letra)
                line.append(",".join([x.nome for x in next_estados]))
            matrix.append(line)

        pretty_print_matrix(matrix)

    def set_qtd_estados(self, qtd_estados: str):
        self.qtd_estados = int(qtd_estados)

    def set_estado_inicial(self, estado_inicial: str):
        self.estado_inicial = self.find_estado(estado_inicial)

    def set_estados_finais(self, estados_finais: str):
        for nome in estados_finais.split(','):
            estado: Estado = self.find_estado(nome)
            self.estados_finais.append(estado)

    def set_alfabeto(self, alfabeto: str):
        if "&" in alfabeto:
            self.is_deterministico = False
        self.alfabeto = alfabeto.split(',')

    def set_transicao(self, transicao: str):
        estado_nome, letra_alfabeto, proximo_estado_nome = transicao.split(',')

        estado: Estado = self.find_estado(estado_nome)

        if "-" in proximo_estado_nome:
            self.is_deterministico = False

            split = proximo_estado_nome.split('-')
            for estado_transicao in split:
                proximo_estado = self.find_estado(estado_transicao)
                estado.add_transicao(letra_alfabeto, proximo_estado)
        else:
            estado.add_transicao(letra_alfabeto, self.find_estado(proximo_estado_nome))

    def parse_file(self, file_name: str):
        with open(file_name) as file:
            for index, line in enumerate(file, 1):
                line = line.replace("\n", "")
                self.functions_file[index if index < 5 else "default"](line)
        self.estado_now = self.estado_inicial

    def find_estado(self, nome: str) -> Estado:
        estado: Estado
        try:
            estado = self.get_estado(nome)
            return estado
        except StopIteration:
            estado = Estado(nome)
            self.estados.append(estado)
            return estado

    def get_estado(self, nome: str) -> Estado:
        return next(estado for estado in self.estados if estado.nome == nome)

    def change_estados_nomes(self):
        for estado in self.estados:
            estado.change_estado_nome()

    def run_entrada(self, entrada: str) -> str:
        """
        Roda uma entrada para AFD, retornando
        se aceita ou rejeita a entrada
        :param entrada: entrada do AF
        :return: ACEITA caso aceite, REJEITA caso rejeite
        """
        for letra in entrada:
            retorno = self.run_letra(letra)
            if not retorno:
                return "REJEITA"

        return "ACEITOU" \
            if self.estado_now in self.estados_finais \
            else "REJEITA"

    def run_letra(self, letra: str) -> bool:
        estados = self.estado_now.next_estado(letra)
        if len(estados) > 0:
            self.estado_now = estados[0]
            return True
        else:
            return False

    def determinizar(self) -> AF:
        """
        Caso o autômato seja não determinístico,
        esse método o determiniza
        """
        if not self.is_deterministico:
            # determinização por epsilon
            if "&" in self.alfabeto:
                self.alfabeto.remove("&")

                af_new: AF = AF()
                af_new.alfabeto = self.alfabeto

                estados_epsilon: List[List[Estado]] = self.get_epsilon_fecho()

                # adiciona estados de epsilon
                for estados in estados_epsilon:
                    estado_novo: Estado = af_new.find_estado(",".join([x.nome for x in estados]))
                    estado_novo.estados = estados

                    if estados[0] == self.estado_inicial:
                        af_new.estado_inicial = estado_novo

                    if any(elem in estados for elem in self.estados_finais):
                        af_new.estados_finais.append(estado_novo)

                # analisa os estados novos recursivamente
                estados_analisados: List[Estado] = []
                fila_estados: List[Estado] = copy.copy(af_new.estados)
                while len(fila_estados) != 0:
                    estado_analisado_now: Estado = fila_estados.pop(0)
                    estados_analisados.append(estado_analisado_now)

                    for letra in self.alfabeto:
                        estado_transicao: List[Estado] = []
                        for estado in estado_analisado_now.estados:
                            estado_now: List[Estado] = estado.next_estado(letra)
                            estado_transicao = estado_transicao + estado_now

                        estado_transicao = remove_duplicates_lista(estado_transicao)
                        next_estado: List[Estado] = []
                        for estado in estado_transicao:
                            try:
                                estado_fecho: List[Estado] = next(x for x in estados_epsilon if x[0] == estado)
                                next_estado = next_estado + estado_fecho
                            except StopIteration:
                                pass

                        next_estado = remove_duplicates_lista(next_estado)
                        next_estado_estado: Estado = af_new.find_estado(",".join([x.nome for x in next_estado]))
                        next_estado_estado.estados = next_estado

                        if next_estado_estado not in estados_analisados and next_estado_estado not in fila_estados:
                            fila_estados.append(next_estado_estado)

                        if any(elem in next_estado for elem in self.estados_finais) \
                                and next_estado not in af_new.estados_finais:
                            af_new.estados_finais.append(next_estado_estado)
                        estado_analisado_now.add_transicao(letra, next_estado_estado)
                af_new.remove_useless_estados()
                return af_new

    def get_epsilon_fecho(self) -> List[List[Estado]]:
        estados: List[List[Estado]] = []
        for estado in self.estados:
            epsilon_fecho: List[Estado] = []
            fila_estados: List[Estado] = [estado]
            while len(fila_estados) != 0:
                estado_now: Estado = fila_estados.pop(0)
                epsilon_fecho.append(estado_now)

                transicoes_epsilon: List[Estado] = estado_now.next_estado("&")
                fila_estados = fila_estados + transicoes_epsilon

            estados.append(epsilon_fecho)

        return estados

    def remove_useless_estados(self):
        estados_novos: List[Estado] = copy.copy(self.estados)
        estados_removidos: List[Estado] = []
        len_estados: int = len(estados_novos)
        len_now: int = 0

        while len_estados != len_now:
            len_estados = len(estados_novos)

            for estado in estados_novos:
                has_transicao: bool = False
                for estado2 in estados_novos:
                    if (estado != estado2 and estado2.has_estado_transicao(estado)) or estado == self.estado_inicial:
                        has_transicao = True
                        break
                if not has_transicao:
                    estados_removidos.append(estado)
                    estados_novos.remove(estado)
                    break

            len_now = len(estados_novos)

        self.estados = estados_novos
        self.estados_finais = remove_duplicates_lista([x for x in self.estados_finais if x in self.estados])

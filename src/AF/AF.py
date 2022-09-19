from typing import List, Union
from src.AF.Estado import Estado


class AF:
    def __init__(self):
        self.qtd_estados: int = 0
        self.estados: List[Estado] = []
        self.estados_finais: List[Estado] = []
        self.estado_inicial: Estado
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
            estados finais: { ','.join([x.nome for x in self.estados_finais]) }
            estados: { ','.join([x.nome for x in self.estados]) }
            alfabeto: {self.alfabeto}
            deterministico: {self.is_deterministico}
        """

    def set_qtd_estados(self, qtd_estados: str):
        self.qtd_estados = int(qtd_estados)

    def set_estado_inicial(self, estado_inicial: str):
        self.estado_inicial = Estado(estado_inicial, self)
        self.estados.append(self.estado_inicial)

    def set_estados_finais(self, estados_finais: str):
        for nome in estados_finais.split(','):
            estado: Estado = Estado(nome, self)
            self.estados_finais.append(estado)
            self.estados.append(estado)

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
            estado = Estado(nome, self)
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

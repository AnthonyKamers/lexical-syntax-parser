from typing import List, Union
from src.AF.Estado import Estado


class AF:
    def __init__(self):
        self.qtd_estados: int = 0
        self.estados: List[Estado] = []
        self.estados_finais: List[str] = []
        self.estado_inicial: str = ""
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
        estado inicial: {self.estado_inicial}
        estados finais: {self.estados_finais}
        alfabeto: {self.alfabeto}
        deterministico: {self.is_deterministico}
        """

    def set_qtd_estados(self, qtd_estados: str):
        self.qtd_estados = int(qtd_estados)

    def set_estado_inicial(self, estado_inicial: str):
        self.estado_inicial = estado_inicial

    def set_estados_finais(self, estados_finais: str):
        self.estados_finais = estados_finais.split(',')

    def set_alfabeto(self, alfabeto: str):
        if "&" in alfabeto:
            self.is_deterministico = False
        self.alfabeto = alfabeto.split(',')

    def set_transicao(self, transicao: str):
        estado_nome, letra_alfabeto, proximo_estado = transicao.split(',')
        estado: Estado = Estado(estado_nome, self)

        if "-" in proximo_estado:
            self.is_deterministico = False

            split = proximo_estado.split('-')
            for estado_transicao in split:
                estado.add_transicao(letra_alfabeto, estado_transicao)
        else:
            estado.add_transicao(letra_alfabeto, proximo_estado)

        self.estados.append(estado)

    def parse_file(self, file_name: str):
        with open(file_name) as file:
            for index, line in enumerate(file, 1):
                line = line.replace("\n", "")
                self.functions_file[index if index < 5 else "default"](line)

        self.estado_now = self.get_estado_inicial()

    def get_estado(self, nome: str) -> Estado:
        return next(estado for estado in self.estados if estado.nome == nome)

    def get_estado_inicial(self) -> Estado:
        return self.get_estado(self.estado_inicial)

    def run_entrada(self, entrada: str) -> str:
        """
        Roda uma entrada para AFD, retornando
        se aceita ou rejeita a entrada
        :param entrada: entrada do AF
        :return: ACEITA caso aceite, REJEITA caso rejeite
        """
        for letra in entrada:
            self.run_letra(letra)

        return "ACEITOU" \
            if self.estado_now.nome in self.estados_finais \
            else "REJEITA"

    def run_letra(self, letra: str):
        teste = self.estado_now.next_estado(letra)[0]
        print(teste)

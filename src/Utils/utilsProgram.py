from typing import List

from src.AF.AF import AF
from src.AF.Estado import Estado


def print_steps(steps):
    [print(f"{x.value}: {x.name}") for x in steps]


def salvar_af(af: AF):
    def parse_estado_nome(estado_now: Estado) -> str:
        if "," in estado_now.nome:
            return estado_now.nome.replace(",", "-")
        return estado_now.nome

    def parse_estados_nome(estados_now: List[Estado]) -> str:
        nomes = ""
        for estado_now in estados_now:
            nomes += parse_estado_nome(estado_now)
            nomes += ","
        return nomes[:-1]

    # main code
    if af is None:
        print("Ainda não foi carregado um AF principal. \n")
        return

    print("""
        Você deve digitar o caminho para o qual deseja salvar o arquivo.
        OBS: digite com o nome do arquivo .af no final, por exemplo:
        /home/jerusa/teste_incrivel.af
    """)
    path = input(": ")

    try:
        f = open(path, 'w')
        f.write(str(len(af.estados)) + "\n")
        f.write(parse_estado_nome(af.estado_inicial) + "\n")
        f.write(parse_estados_nome(af.estados_finais) + "\n")
        f.write(",".join(af.alfabeto) + "\n")

        for estado in af.estados:
            for transicao in estado.transicoes:
                letra, estado_new, _ = transicao
                f.write(f"{parse_estado_nome(estado)},{letra},{parse_estado_nome(estado_new)}\n")

        f.close()

        print("Arquivo foi gerado com sucesso! \n")
    except Exception as e:
        print("Houve algum erro ao salvar o arquivo de AF: " + str(e))

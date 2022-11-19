from enum import Enum
from typing import List

from src.AF.AF import AF
from src.AF.Estado import Estado
from src.Program.modules.AbstractProgram import AbstractProgram
from src.Utils.utilsAF import uniao_automatos

PATH_AF = "entradas/AF/"


class Step(Enum):
    CarregarArquivo = 1
    Determinizar = 2
    Minimizar = 3
    UniaoAutomatos = 4
    TabelaTransicao = 5
    InformacoesGeraisAF = 6
    SalvarAF = 7
    Clear = 8


class AFProgram(AbstractProgram):
    def __init__(self):
        self.af = None
        self.af1 = None

        self.functions = {
            Step.CarregarArquivo: self.carregar_arquivo,
            Step.Determinizar: self.determinizar,
            Step.Minimizar: self.minimizar,
            Step.UniaoAutomatos: self.uniao_automatos,
            Step.TabelaTransicao: self.tabela_transicao,
            Step.InformacoesGeraisAF: self.informacoes_gerais,
            Step.SalvarAF: self.salvar_af,
            Step.Clear: self.clear
        }

        self.af_now = 0

    def run(self):
        while True:
            print("Você está na sessão de AF: \n")
            [print(f"{x.value}: {x.name}") for x in Step]

            try:
                result = int(input(": "))
            except ValueError:
                print("Você deve digitar um número")
                continue

            try:
                function = self.functions[Step(result)]
                function()
            except ValueError:
                break

    def carregar_arquivo(self):
        print(f"""
            Digite o local onde está armazenado o arquivo de AF.
            OBS: Se você não digitar um caminho que comece com "/",
            tentará pegar automaticamente da pasta do projeto localizada em
            {PATH_AF}.
            Digite 0 para sair dessa função.
        """)
        path = input(": ")

        try:
            af: AF = AF()

            if path.startswith("/"):
                af.parse_file(path)
            else:
                af.parse_file(PATH_AF + path)

            if self.af_now == 0:
                self.af = af
            else:
                self.af1 = af
                self.af_now = 0

            print("Arquivo carregado. \n")
        except IOError:
            print("Houve algum problema ao fazer parse do arquivo. Tente novamente. \n")
            self.carregar_arquivo()

    def determinizar(self):
        if self.af is None:
            print("Ainda não foi carregado um AF. \n")
            return

        if self.af.is_deterministico:
            print("O AF já é determinístico. \n")
            return

        try:
            self.af.determinizar()
            print("AF Determinizado com sucesso. \n")
            return
        except Exception as e:
            print("Houve algum erro ao determinizar o AF: " + str(e))

    def minimizar(self):
        if self.af is None:
            print("Ainda não foi carregado um AF. \n")
            return

        try:
            self.af = self.af.minimizar()
            print("AF minimizado com sucesso. \n")
        except Exception as e:
            print("Houve algum erro ao minimizar o AF: " + str(e))

    def uniao_automatos(self):
        if self.af is None:
            print("Ainda não foi carregado um AF principal. \n")
            return

        print("Um AF principal já está definido; Você deve carregar agora outro arquivo para fazer a união: ")

        self.af_now = 1
        self.carregar_arquivo()
        self.af_now = 0

        if self.af1 is None:
            print("Houve algum erro ao carregar segundo AF. \n")
            return

        try:
            self.af = uniao_automatos(self.af, self.af1)
        except Exception as e:
            print("Houve algum erro ao fazer a união dos autômatos; ambos vão"
                  " ser reinicilizados; tente novamente: " + str(e))
            self.af = None
            self.af1 = None
            self.af_now = 0

    def tabela_transicao(self):
        if self.af is None:
            print("Ainda não foi carregado um AF principal. \n")
            return

        try:
            self.af.show_tabela_transicao()
        except Exception as e:
            print("Houve algum erro ao mostrar a tabela de transição: " + str(e))

    def informacoes_gerais(self):
        if self.af is None:
            print("Ainda não foi carregado um AF principal. \n")
            return

        try:
            print(self.af)
        except Exception as e:
            print("Houve algum erro ao mostrar informações do AF: " + str(e))

    def salvar_af(self):
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
        if self.af is None:
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
            f.write(str(len(self.af.estados)) + "\n")
            f.write(parse_estado_nome(self.af.estado_inicial) + "\n")
            f.write(parse_estados_nome(self.af.estados_finais) + "\n")
            f.write(",".join(self.af.alfabeto) + "\n")

            for estado in self.af.estados:
                for transicao in estado.transicoes:
                    letra, estado_new, _ = transicao
                    f.write(f"{parse_estado_nome(estado)},{letra},{parse_estado_nome(estado_new)}\n")

            f.close()

            print("Arquivo foi gerado com sucesso! \n")
        except Exception as e:
            print("Houve algum erro ao salvar o arquivo de AF: " + str(e))

    def clear(self):
        self.af = None
        self.af1 = None

        print("Autômatos foram reinicializados. \n")

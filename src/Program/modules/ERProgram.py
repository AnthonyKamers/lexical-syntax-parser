from enum import Enum

from src.ER.ER import ER
from src.Program.modules.AbstractProgram import AbstractProgram
from src.Utils.utilsER import print_tree
from src.Utils.utilsAF import uniao_automatos

PATH_ER = "entradas/ER/"

# ER
#  - carregar arquivo
#  - fazer AFD de cada expressão regular
#  - mostrar árvore gerada para cada ER
#  - fazer a união de todos os autômatos gerados


class Step(Enum):
    CarregarArquivo = 1
    FazerArvoreER = 2
    MostrarArvore = 3
    FazerAFD_ER = 4
    Uniao_AFD = 5
    MostrarAFD_Unido = 6
    Clear = 8


class ERProgram(AbstractProgram):
    def __init__(self):
        self.er = None

        self.functions = {
            Step.CarregarArquivo: self.carregar_arquivo,
            Step.FazerArvoreER: self.make_tree_er,
            Step.MostrarArvore: self.show_tree,
            Step.FazerAFD_ER: self.make_afd_er,
            Step.Uniao_AFD: self.uniao_afd,
            Step.MostrarAFD_Unido: self.show_afd_unido,
            Step.Clear: self.clear

        }
        
        self.er_now = 0
        self.afnd_geral = None
        self.afd_geral = None



    def run(self):
        while True:
            print("Você está na sessão de ER: \n")
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
            Digite o local onde está armazenado o arquivo de ER.
            OBS: Se você não digitar um caminho que comece com "/",
            tentará pegar automaticamente da pasta do projeto localizada em
            {PATH_ER}.
            Digite 0 para sair dessa função.
        """)
        path = input(": ")

        try:
            self.er = ER()
            if path.startswith("/"):
                self.er.parse_file(path)
            else:
                self.er.parse_file(PATH_ER + path)

            print("Arquivo carregado. \n")
        except IOError:
            print("Houve algum problema ao fazer parse do arquivo. Tente novamente. \n")
            self.carregar_arquivo()

    def make_tree_er(self):
        if self.er is None:
            print("Ainda não foi carregado um ER principal. \n")
            return

        if self.er.er_tree:
            print("O ER já possui uma árvore. \n")
            return

        try:
            self.er.make_afd_er()
            print("Feito AFD da ER com sucesso. \n")
            return
        except Exception as e:
            print("Houve algum erro ao fazer o AFD da ER: " + str(e))

    def show_tree(self):
        if self.er is None:
            print("Ainda não foi carregado um ER principal. \n")
            return

        try:
            print_tree(self.er.er_tree['id'], 0)
            return
        except Exception as e:
            print("Houve algum erro ao retornar a ER: " + str(e))


    def make_afd_er(self):
        if self.er is None:
            print("Ainda não foi carregado um ER principal. \n")
            return

        try:
            self.er.make_afd_er()
            return
        except Exception as e:
            print("Houve algum erro ao fazer o AFD da ER: " + str(e))



    def uniao_afd(self):
        if self.er is None:
            print("Ainda não foi carregado um ER principal. \n")
            return

        try:
            self.afnd_geral: 'Union'[None, AF] = None   # tem erro
            afds = list(self.er.afds.values())
            
            for i in range(len(afds)):
                if i == 0:
                    continue
                if self.afnd_geral is None:
                    self.afnd_geral = uniao_automatos(afds[i-1], afds[i])
                else:
                    self.afnd_geral = uniao_automatos(self.afnd_geral, afds[i])
            self.afd_geral = self.afnd_geral.determinizar()
            return
        except Exception as e:
            print("Houve algum erro ao retornar a ER: " + str(e))

        

    def show_afd_unido(self):
        if self.er is None:
            print("Ainda não foi carregado um ER principal. \n")
            return

        try:
            print(self.afd_geral)
            self.afd_geral.show_tabela_transicao()
            print(self.afd_geral.run_entrada("asda1"))
            return
        except Exception as e:
            print("Houve algum erro ao retornar a ER: " + str(e))


    def clear(self):
        self.er = None
        #self.er1 = None

        print("Expressões Regulares foram reinicializadas. \n")

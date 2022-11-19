from enum import Enum

from src.ER.ER import ER
from src.Program.modules.AbstractProgram import AbstractProgram

PATH_ER = "entradas/ER/"


class Step(Enum):
    CarregarArquivo = 1
    FazerArvoreER = 2
    MostrarArvore = 3
    FazerAFD_ER = 4
    Uniao_AFD = 5
    MostrarAFD_Unido = 6


class ERProgram(AbstractProgram):
    def __init__(self):
        self.er = ER()

        self.functions = {
            Step.CarregarArquivo: self.carregar_arquivo,
            Step.FazerArvoreER: self.make_tree_er,
            Step.MostrarArvore: self.show_tree,
            Step.FazerAFD_ER: self.make_afd_er,
            Step.Uniao_AFD: self.uniao_afd,
            Step.MostrarAFD_Unido: self.show_afd_unido
        }

    def run(self):
        pass

    def carregar_arquivo(self):
        pass

    def make_tree_er(self):
        pass

    def show_tree(self):
        pass

    def make_afd_er(self):
        pass

    def uniao_afd(self):
        pass

    def show_afd_unido(self):
        pass

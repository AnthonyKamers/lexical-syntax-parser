from typing import Union

from src.AF.AF import AF
from src.AF.Estado import Estado
from src.ER.ER import ER
from src.Grammar.Grammar import Grammar
from src.Utils.utilsAF import uniao_automatos
from src.Utils.utilsER import *

if __name__ == '__main__':
    # exemplo fazendo união de autômatos
    # af1: AF = AF()
    # af1.parse_file("entradas/AF/exemplo1.af")
    # af2: AF = AF()
    # af2.parse_file("entradas/AF/exemplo1.af")
    # af_new: AF = uniao_automatos(af1, af2)
    # print(af_new)
    # af_new.show_tabela_transicao()

    # exemplo determinizando autômato com &-transição
    # af: AF = AF()
    # af.parse_file("entradas/AF/exemplo2.af")
    # af_new: AF = af.determinizar()
    # af_new.show_tabela_transicao()

    # exemplo determinizando autômato sem &-transição
    # af: AF = AF()
    # af.parse_file("entradas/AF/exemplo4.af")
    # af_new: AF = af.determinizar()
    # print(af_new)
    # af_new.show_tabela_transicao()

    # exemplo minimização de autômato
    # af: AF = AF()
    # af.parse_file("entradas/AF/exemplo5.af")
    # af_new: AF = af.minimizar()
    # af_new.show_tabela_transicao()
    # print(af_new)

    # ER
    # er: ER = ER()
    # er.parse_file("entradas/ER/exemplo4.er")
    # er.make_afd_er()
    #
    # print(list(er.afds.keys()))
    #
    # # fazer união de AFDs
    # afnd_geral: Union[None, AF] = None
    # afds = list(er.afds.values())
    #
    # for i in range(len(afds)):
    #     if i == 0:
    #         continue
    #     if afnd_geral is None:
    #         afnd_geral = uniao_automatos(afds[i-1], afds[i])
    #     else:
    #         afnd_geral = uniao_automatos(afnd_geral, afds[i])
    #
    # # determinizar união dos autômatos
    # afd_geral = afnd_geral.determinizar()

    # printtar para testar
    # print(afd_geral)
    # afd_geral.show_tabela_transicao()

    # Gramática
    # grammar = Grammar()
    # grammar.parse_file("entradas/gramaticas/exemplo-rec-esquerda-indireta.grammar")
    # print(grammar.has_left_recursion())
    # grammar.remove_recursao_esquerda()
    # grammar.remove_nao_determinismo()
    # print(grammar.has_nullable(), grammar.has_left_recursion())

    # Analisador Sintático
    grammar = Grammar()
    grammar.parse_file("entradas/gramaticas/exemplo-first-follow1.grammar")
    grammar.get_firsts()
    grammar.get_follows()
    print("")

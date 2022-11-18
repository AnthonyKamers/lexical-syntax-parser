from typing import Union

from src.AF.AF import AF
from src.ER.ER import ER
from src.Exceptions.Lexicon.TokenNotValidException import TokenNotValidException
from src.Utils.utilsAF import uniao_automatos


class AnalisadorLexico:
    """
    Faz os procedimentos de checagem léxica,
    assim como leitura de um arquivo-fonte e geração de tabela sintática
    """
    def __init__(self):
        self.er = ER()
        self.afd_geral: Union[None, AF] = None
        self.has_er = False
        self.tokens_iniciais = []

        self.special_words = []
        self.ts = []
        self.tokens = []

    def set_er(self, file_name: str):
        self.er.parse_file(file_name)
        self.has_er = True

    def set_tokens_iniciais(self, tokens: str):
        for token in tokens.split(","):
            self.tokens_iniciais.append(token)

    def build(self):
        def build_afd():
            self.er.make_afd_er()

            afds = list(self.er.afds.values())
            afnd_geral: Union[None, AF] = None

            # fazer união por &-transição
            for i in range(len(afds)):
                if i == 0:
                    continue
                if afnd_geral is None:
                    afnd_geral = uniao_automatos(afds[i - 1], afds[i])
                else:
                    afnd_geral = uniao_automatos(afnd_geral, afds[i])

            # determinizar união dos autômatos
            self.afd_geral = afnd_geral.determinizar()

        def build_ts():
            for token_inicial in self.tokens_iniciais:
                words = self.er.get_plain_words(token_inicial)
                for word in words:
                    self.special_words.append(word)
                    self.ts.append((word, token_inicial))

        # main code
        if self.has_er:
            # fazer AFD de todos os ER
            build_afd()

            # iniciar tabela de símbolos
            build_ts()
        else:
            print("O analisador léxico ainda não tem definições regulares definidas!")

    def show_tabela_lexica(self):
        if self.afd_geral is not None:
            print(self.afd_geral)
            self.afd_geral.show_tabela_transicao()
        else:
            print("O analisador léxico ainda não gerou a tabela léxica para as definições regulares")

    def find_token_ts(self, token: str):
        find = [(x, k) for k, x in enumerate(self.ts) if x[0] == token]
        return find[0] if len(find) > 0 else False

    def get_afds(self):
        return [(key, value) for key, value in self.er.afds.items() if key not in self.tokens_iniciais]

    def set_file(self, file_name: str):
        def get_token():
            token = self.find_token_ts(parte)
            if token is not False:
                # token já existente na TS
                self.tokens.append(token)
            else:
                # criar token
                is_valid = self.afd_geral.run_entrada(parte)
                if is_valid:
                    # token válido, checar qual sua classe
                    for key, afd in self.get_afds():
                        # se o AFD aceitou a entrada, então é desta classe
                        if afd.run_entrada(parte):
                            # adicionar primeiramente na TS
                            self.ts.append((parte, key))

                            # adicionar na lista de tokens
                            self.tokens.append(self.find_token_ts(parte))
                            return

                    raise TokenNotValidException
                else:
                    # token inválido
                    raise TokenNotValidException

        with open(file_name) as file:
            for line in file:
                line = line.replace("\n", "")
                # ignorar linhas com comentários
                if line[0] == "#":
                    continue

                partes = line.split(" ")
                for parte in partes:
                    get_token()

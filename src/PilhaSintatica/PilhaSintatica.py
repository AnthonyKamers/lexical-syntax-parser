import copy

from src.Exceptions.Syntactic.DifferentSyntaxExpected import DifferentSyntaxExpected


class PilhaSintatica:
    """
    Implementação da pilha sintática, que faz uso da tabela sintática gerada pelo
    analisador sintático LL(1)
    """
    def __init__(self, analisador_sintatico: any):
        self.analisador_sintatico = analisador_sintatico
        self.pilha = []

    def run_entrada(self, entrada: str):
        """
        Roda para a entrada especificada o algoritmo de autômato de pilha,
        fazendo com que retorna que a aceite ou rejeite
        :param entrada: palavra que deseja testar a gramática
        :return: Se aceita a entrada
        """
        def desempilhar_nao_terminais():
            """
            Roda laço de desempilhamento com base em um terminal
            """
            while True:
                if len(self.pilha) == 0:
                    break

                simbolo_pilha = self.pilha.pop()

                # condições de terminal
                if simbolo_pilha.is_terminal():
                    if simbolo_pilha.simbolo == char:
                        # desempilhar e parar o laço
                        break
                    elif simbolo_pilha == epsilon:
                        # somente desempilhar
                        continue
                    elif simbolo_pilha.simbolo != char:
                        # símbolo terminal diferente do esperado agora
                        raise DifferentSyntaxExpected

                # rodar as produções ao contrário na pilha
                producao = copy.copy(tabela_sintatica[simbolo_pilha][grammar.find_symbol(char)][0])
                producao.reverse()
                for simbolo in producao:
                    self.pilha.append(simbolo)

        self.pilha = [self.analisador_sintatico.grammar.simbolo_inicial]
        tabela_sintatica = self.analisador_sintatico.tabela_sintatica.table
        grammar = self.analisador_sintatico.grammar
        epsilon = grammar.find_symbol("&")

        for char in entrada:
            desempilhar_nao_terminais()

        # terminar de desempilhar o resto
        char = "$"
        desempilhar_nao_terminais()

        # checagem final
        return len(self.pilha) == 0

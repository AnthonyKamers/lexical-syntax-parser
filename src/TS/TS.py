from string import whitespace

class TS():
    def __init__(self):
        self.symbols_table = dict()
        self.tokens = []



# Lista de simbolos a-z 0-9 

    # Criar tabela de (dict) de simbolos apartir das palavras reservadas [Digit:9].  
    def create_TS(self, palavras: list):
        for i in palavras:
            self.symbols_table[i[0]] = {i[1]}


    #ver se o lexema ja ta na lista
    def verificar_lexema(self, lexema):
        if lexema in self.symbols_table:
            return True, self.symbols_table.get(lexema)
        #else:

    def calc_lexema_index(self, text, i):
        while i < len(text) and text[i] in whitespace:  # vai até o inicio da palavra, ja sala o i+1 para verificar o tamanho do lexema
            i += 1
        return i

    # Percorre o texto até encontra o proximo indice de caracter sem ser espaçamento. aa == aaaa
    # Percorre o texto verificando se o caracter é valido e o incrementa a palavra.
    def parse_text(self, text):
        begin_lex = self.calc_lexema_index(text,0)
        prox_i = begin_lex+1

        while begin_lex < len(text):    # index inicial
            lexema = text[begin_lex]
            lex_valid, tokens = self.verificar_lexema(lexema)
            
            while prox_i < len(text):   # index final
                lexema += text[prox_i]
                lex_prox_valid, tokens = self.verificar_lexema(lexema)
                if lex_valid and not lex_prox_valid:
                    break
                prox_i+=1

            lex_valid, tokens = self.verificar_lexema(lexema)
            self.symbols_table[lexema] = tokens

            begin_lex = self.calc_lexema_index(text,prox_i) # pega o index do proximo lexema
            prox_i = begin_lex+1




    # Faz a analise lexica,
    # Vai verificando  se o lexema encontrado ja ta na TS, se tiver retorna se nao tiver faz recursao passando ele + 1 para verificar novamente.
# Gerador de analisador léxico e sintático

Tal trabalho tem como objetivo fazer um gerador de analisador léxico e sintático para a disciplina de Linguagens Formais e Compiladores da UFSC (INE5421).

## Equipe do trabalho:
- Anthony Bernardo Kamers (19204700)
- Antonio S. Montagner    (19203742)

Este readme contará, além das especificações do gerador de análise léxica e sintática, o manual de uso e instalação, a divisão de trabalho entre os integrantes do grupo e uso CLI de determinadas ferramentas do projeto.

### As etapas de desenvolvimento serão divididas em duas partes:
- Analisador léxico
- Analisador sintático

______

# Analisador léxico (peso 4)
Algoritmos a serem implementados

- [X] Conversão de Expressão Regular (ER) para Autômato Finito Determinístico (AFD) -> disponível algoritmo no livro do Aho
- [X] União de Autômatos via epsilon-transição
- [X] Determinização de Autômatos
- [ ] Construção da Tabela de Símbolos (TS)
  - Deve ser incluído palavras reservadas e outras informações importantes (para auxiliar nas etapas do analisador sintático)

Fluxo de execução do analisador léxico
1. Inclusão de expressões regulares para todos padrões de tokens, usando definições regulares
2. Para cada ER deve ser gerado o AFD correspondente
3. Os AFD devem ser unidos com epsilon-transições
    - Isso formará um AFND
4. O AFND resultante deve ser determinizado gerando a tabela de análise léxica (TAL)
5. O analisador léxico entrará então com um código fonte
6. O código fonte será analisado, utilizando a TAL e gerará um arquivo de saída com a lista de todos os tokens encontrados (ou reportar erro em caso de entrada inválida)

______

# Analisador sintático (peso 6)
Algoritmos a serem implementados

- [X] Se preditivo LL(1)
  - Eliminar recursão à esquerda
  - Fatoração
  - Cálculo de Firsts e Follows
  - Geração de tabela de análise LL(1)
  - Algoritmo que implementa Autômato de pilha para análise de sentenças que faz uso da tabela LL(1)
- [ ] Se LR Canônico
  - Cálculo de Firsts e Follows
  - Algoritmos de analisador LR Canônico (livro do Aho) para geração da tabela SLR(1) e para análise de sentenças de entrada SLR(1)
- [ ] Deve receber e validar Gramática Livre de Contexto (GLC)
  - Descreve código fonte (pseudo-linguagem usado para teste do analisador)
  - Identifica terminais (tokens) e não terminais
    - pode ser explícita em uma lista de terminais e uma de não-terminais

Fluxo de execução do analisador sintático
1. Leitura token a token do arquivo resultante da análise léxica
2. Uso da TAL e do algoritmo que simula a pilha para validação da sentença de entrada
3. Saída: Valida ou invalida código fonte de entrada

______

## Observações
- Usar epsilon como &
- Tabelas de análise (léxica e sintática) devem poder ser visualizadas
- AF gerados pela conversão de ERs deve poder ser visualizada
- Pilha de análise deve ser apresentada
- Funções separadas devem ser executadas, de maneira a testar cada funcionalidade de maneira separada
  - Isso facilita a correção por parte da professora, além de poder visualizar cada etapa com mais facilidade
  - É aconselhável separar entradas e saídas para cada etapa, para assegurar da assertividade de cada etapa
- É aconselhável fazer testes unitários, para garantir a corretude de funções já implementadas (para eventuais atualizações no futuro)
- Também pode ser feita uma pipeline utilizando o github-pro, para facilitar demais implementações (como automatização de testes e entradas de arquivos (conforme especificado na seção abaixo))

______

## Explicação do trabalho de maneira prática
```text
DEFINICOES REGULARES
{
    "digit": [0,1,2,3,4,5,6,7,8,9],
    "letter": [a,b,c,...],
    "id": [[letter],[AND],[(letter OR digit)*]],
    "er": [[a],[OPTIONAL],[(a OR b)+]]
}

ARQUIVO FONTE
program teste;
var a: integer;
begin
.
.
.
end

TABELA DE SIMBOLOS (TS)
[(program, PR), (teste, id)]

LISTA DE TOKENS
[(program, PR), (id, 1), (;, SE)]
```

## Formatos de entrada

Os formatos de entrada de exemplo estão na pasta entradas/

Vale informar que para cada tipo, será descrito a seguir as especificações

- Autômatos Finitos (AF)
  - número de estados
  - estado inicial
  - estados finais
  - alfabeto
  - transições (uma por linha)
- Expressões Regulares (ER)
  - definicao-reg1: ER1
  - definicao-reg2: ER2
  - ...
- Gramáticas
  - S -> aSb | &
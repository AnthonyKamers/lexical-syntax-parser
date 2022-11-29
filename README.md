# Gerador de analisador léxico e sintático

Tal trabalho tem como objetivo fazer um gerador de analisador léxico
e sintático para a disciplina de Linguagens Formais e Compiladores
da UFSC (INE5421).

Para isso foi utilizado um gerador de analizador sintático preditivo LL(1).

## Equipe do trabalho:
- Anthony Bernardo Kamers (19204700)
- Antonio S. Montagner    (19203742)


## Execução:
Para executar a aplicação:
    
- Requisitos:
    - Python 3.9 ou mais recente

- Comandos:
    - python main.py (Windows)
    - python3 main.py (Linux)

- Execução e Funcionalidades:
  - Ao executar a aplicação, será pedido entrada, de forma interativa,
  dependendo da intenção do usuário. O usuário poderar escolher entre
  as opções fornecidas.
  - Para sair ou voltar para as opções anteriores, basta
  digitar o número '0' ou qualquer número que não esteja nas opções;
  Se for colocado um caractere de texto, será pedido para colocar um
  número na página de opções de funcionalidades.

- Testes completos
  - Como forma de testar todas as funcionalidades dos analisadores léxico
  e sintático, foram testados os seguintes arquivos (disponibilizados em `entradas/`:
    - `ER/`: exemplo1.er
    - `codigo-fonte/`: exemplo1.codigo
    - `gramaticas/`: variavel.grammar
  - Apenas estes foram fornecidos inicialmente abrangendo todas as funcionalidades
  do programa, mas nada impede de criar novos códigos, fazer novos arquivos ou selecionar 
  outro arquivo já existente para testar as funcionalidades. 


## Documentação
Todas as classes e métodos que fazem parte do processo de análise léxica
e sintática foram comentados rigorosamente, sendo os padrões de documentação
definidos pelo Python. Além disso, também foi gerada uma documentação automatizada
em HTML com o gerador Python-Sphinx, disponibilizada em `html/index.html`.


## Passos necessários para execução e teste
Para que todas as etapas sejam testadas e executadas com sucesso,
será dada uma breve explicação de como deve ser o padrão dos arquivos
de entrada para autômatos finitos (AF), expressões regulares (ER),
gramática e código fonte.


### AF
O formato é o mesmo especificado pela professor no trabalho, sendo:
* primeira linha: quantidade de estados
* segunda linha: estado inicial
* terceira linha: estados finais separado por ,
* quarta linha: alfabeto separado por ,
* quinta linha em diante: transições no formato estado,alfabeto,estado_novo

Há vários exemplos de AF testados em `entradas/AF/`.


### ER
Para fazer o parse de expressões regulares, algumas modificações foram
necessárias:
* Formato geral: DEF_ER: er;
* Para facilitar o parse de algumas funcionalidades, foi necessário fazer
a operação de concatenação sendo feito via parênteses;
  * Desta forma, um exemplo de expressão regular que deva ser "abb", deve
  ser colocada da seguinte maneira: ABB: a(b)(b);
* Não são testadas operações de concatenação dentro das concatenações,
logo a seguinte expressão não será
reconhecida corretamente: EXPR: a(b(b));
* Outros identificadores como OR (|), FECHO (*), FECHO POSITIVO (+) e
produção com epsilon opcional (?) são feitos de maneira idêntica aos
estudados em sala de aula;
* Também são reconhecidos os padrões `[a-z]`, `[A-Z]`, `[0-9]`, `[a-zA-Z]`,
que são convertidos diretamente para um OR entre todos os elementos do
alfabeto e/ou algarismos.
* Há vários exemplos de expressões regulares de exemplo em `entradas/ER/`.


### Gramáticas
Para se fazer análise do arquivo de gramáticas, colocamos
uma restrição: em produções que têm mais de um símbolo,
os símbolos devem ser separados por espaço.

Logo para um não terminal S que transita para aA ou bB (`S -> aA | bB`),
ficaria da seguinte forma: `S -> a A | b B`;

Também é importante que siga o seguinte padrão: o símbolo
do não terminal, seguido de espaço, seguido de `-`, seguido
de `>`, seguido de espaço e continuar com as produções
como explicado anteriomente;

Cada produções de não terminais deve ser dada em uma única linha;

Também vale contar que para linhas começadas com #, a linha
inteira é ignorada. Isso é importante para fazer anotações,
tal como é usualmente feito em linguagens de programação.

Para exemplos de gramáticas que foram testadas e são reconhecidas,
podem ser testados os arquivos disponíveis em `entradas/gramaticas/`.


### Código-fonte
Para fornecer códigos-fonte de entrada, é necessário colocar cada
elemento definido nas expressões regulares e gramática, separados por espaços.
Vale considerar também que a leitura do arquivo é dado linha a linha e não
caracter a caracter, tendo algumas restrições caso coloque na gramática ou ER
a separação por quebra de linha `\n`.

# ComportaData

Protótipo acadêmico em Python para registrar e explorar dados comportamentais pelo modelo ABC: **Antecedente, Comportamento e Consequência**.

Desenvolvido por **Fernanda do Vale**, o projeto conecta conhecimentos de Psicologia à prática de programação e organização de dados.

## Sobre o projeto

O programa funciona localmente pelo terminal e salva registros em um arquivo CSV. Cada registro reúne data, antecedente, comportamento, consequência, frequência e duração em minutos.

**Status:** protótipo acadêmico em desenvolvimento, com leitura e gravação de registros CSV.

## Funcionalidades da versão atual

- Cadastrar registros ABC com validação dos campos digitados.
- Consultar os registros carregados do CSV e os novos cadastros.
- Salvar os registros em `registros.csv`, preservando os dados carregados ao iniciar.
- Exibir quantidade de registros, frequência total e duração média por registro.
- Identificar os comportamentos, antecedentes e consequências que aparecem em mais registros.

Na análise, “comportamento mais frequente” representa a contagem de registros com aquele comportamento, e não a soma do campo frequência. Em caso de empate, o programa apresenta o primeiro item encontrado.

## Tecnologias e conceitos praticados

- Python 3 e bibliotecas padrão `csv` e `os`.
- Listas, dicionários e funções.
- Estruturas condicionais e de repetição.
- Entrada de dados pelo terminal.
- Escrita de arquivos CSV e estatísticas descritivas simples.

Não é necessário instalar pacotes adicionais.

## Como executar

1. Instale o Python 3.
2. Baixe o repositório ou clone pelo terminal:

   ```bash
   git clone https://github.com/fdvale/primeiro-projeto.git
   cd primeiro-projeto
   ```

3. Execute:

   ```bash
   python main.py
   ```

   No Windows, você também pode usar `py main.py`. Em sistemas que usam esse comando, execute `python3 main.py`.

4. Escolha uma opção no menu:

   | Opção | Ação |
   |---|---|
   | 1 | Novo registro |
   | 2 | Ver registros |
   | 3 | Analisar dados |
   | 4 | Sair |

Digite os comandos de execução no terminal, antes de abrir o programa. No menu, digite apenas o número da opção.

## Exemplo fictício de preenchimento

| Campo | Exemplo |
|---|---|
| Data | 30/09/2026 |
| Antecedente | Apresentação de uma tarefa |
| Comportamento | Pedir ajuda |
| Consequência | Receber orientação |
| Frequência | 2 |
| Duração | 1.5 |

No terminal, use ponto ou vírgula para separar as casas decimais da duração. No CSV, o programa salva a duração com ponto. O arquivo `registros.csv` é criado na mesma pasta de `main.py` após o primeiro cadastro.

## Leitura e preservação do CSV

Ao iniciar, o programa procura `registros.csv` na mesma pasta de `main.py`. Se o arquivo existir, carrega os registros e converte frequência e duração para números. Se não existir, inicia sem registros e cria o CSV após o primeiro cadastro.

Novos registros são salvos junto com os anteriores. A opção de análise sem dados exibe uma mensagem e retorna ao menu.

Se o CSV tiver cabeçalho incorreto, campos ausentes, números inválidos, negativos ou duração não finita, o programa encerra sem alterar o arquivo. Confira o conteúdo antes de tentar novamente. Aceita CSV em UTF-8 com ou sem BOM.

## Testar com exemplos fictícios

A pasta `exemplos` contém `registros_exemplo_ficticios.csv`, com 20 registros criados apenas para demonstração.

1. Feche o programa. Se já houver um `registros.csv`, faça uma cópia de segurança antes de substituí-lo.
2. Copie o arquivo de exemplos para a pasta de `main.py` e renomeie a cópia para `registros.csv`.
3. Execute o programa e escolha a opção 2 ou 3.

Com os exemplos sem alterações, a análise apresenta 20 registros, frequência total de 40 e duração média de 2.85 minutos por registro. Os exemplos permanecem separados do CSV de uso.

## Testes automatizados

Na pasta do projeto, execute:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam a leitura, a preservação dos registros ao reabrir, a análise vazia, o primeiro cadastro a proteção contra CSV inválido e a recuperação após entradas inválidas no terminal. Usam pastas temporárias e dados fictícios.

## Validação do cadastro

Quando uma entrada é inválida, o programa explica o problema e solicita novamente o mesmo campo.

| Campo | Valores aceitos |
|---|---|
| Menu | Inteiro de 1 a 4 |
| Data | Data existente no formato dd/mm/aaaa, incluindo validação de anos bissextos |
| Antecedente, comportamento e consequência | Texto obrigatório |
| Frequência | Inteiro maior ou igual a zero |
| Duração | Número finito maior ou igual a zero, com ponto ou vírgula decimal |

A validação de datas e textos se aplica ao cadastro pelo terminal. A leitura de CSV mantém as verificações de estrutura e números descritas acima.


## Estrutura do repositório

| Arquivo | Finalidade |
|---|---|
| `main.py` | Programa com leitura, cadastro, consulta e análise |
| `README.md` | Apresentação e instruções |
| `.gitignore` | Exclui dados locais e arquivos temporários do Git |
| `tests/test_main.py` | Testes automatizados de regressão |
| `exemplos/registros_exemplo_ficticios.csv` | Dados fictícios para demonstração |

O CSV gerado durante o uso não é incluído no repositório. Os exemplos apresentados são fictícios.

## Próximas melhorias

- Ampliar as análises e a apresentação dos resultados.

Esses itens são propostas para futuras versões, ainda não implementadas.

## Autoria

**Fernanda do Vale** — [GitHub](https://github.com/fdvale)


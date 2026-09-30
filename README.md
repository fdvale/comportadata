# ComportaData

Protótipo acadêmico em Python para registrar e explorar dados comportamentais pelo modelo ABC: **Antecedente, Comportamento e Consequência**.

Desenvolvido por **Fernanda do Vale**, o projeto conecta conhecimentos de Psicologia à prática de programação e organização de dados.

## Sobre o projeto

O programa funciona localmente pelo terminal e salva registros em um arquivo CSV. Cada registro reúne data, antecedente, comportamento, consequência, frequência e duração em minutos.

**Status:** protótipo inicial. Este repositório contém a versão original do código, com limitações documentadas abaixo.

## Funcionalidades da versão atual

- Cadastrar registros ABC.
- Consultar os registros cadastrados durante a execução atual.
- Exportar os registros da execução para `registros.csv`.
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

Use ponto para separar as casas decimais da duração. O arquivo `registros.csv` é criado na mesma pasta de `main.py` após o primeiro cadastro.

## Limitações conhecidas

- Os registros começam vazios a cada execução: o CSV existente não é carregado.
- Ao cadastrar um registro em uma nova execução, o CSV anterior é sobrescrito com os registros da execução atual.
- Selecionar a análise sem registros causa um erro de divisão por zero.
- Entradas não numéricas nos campos numéricos podem encerrar o programa.
- Não há validação de datas, valores negativos ou campos de texto vazios.

Essas limitações precisam ser resolvidas antes de usar o programa para armazenar dados que devam ser preservados.

## Estrutura do repositório

| Arquivo | Finalidade |
|---|---|
| `main.py` | Código original do programa |
| `README.md` | Apresentação e instruções |
| `.gitignore` | Exclui dados locais e arquivos temporários do Git |

O CSV gerado durante o uso não é incluído no repositório. Os exemplos apresentados são fictícios.

## Próximas melhorias

- Recuperar registros do CSV ao iniciar.
- Tratar entradas inválidas e análises sem dados.
- Validar os campos de cadastro.
- Ampliar as análises e a apresentação dos resultados.

Esses itens são propostas para futuras versões, ainda não implementadas.

## Autoria

**Fernanda do Vale** — [GitHub](https://github.com/fdvale)

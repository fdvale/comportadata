import csv
import math
import os
import sys

pasta_projeto = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(pasta_projeto, "registros.csv")

opcao = 0
campos = [
    "data",
    "antecedente",
    "comportamento",
    "consequencia",
    "frequencia",
    "duracao"
]


def carregar_registros():
    """Lê o CSV existente e converte frequência e duração para números."""
    if not os.path.exists(caminho_csv):
        return []

    registros_carregados = []
    with open(caminho_csv, "r", newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo, strict=True)
        if leitor.fieldnames is None:
            return []
        if len(leitor.fieldnames) != len(campos) or set(leitor.fieldnames) != set(campos):
            raise ValueError("O cabeçalho do CSV deve conter: " + ", ".join(campos))

        for registro in leitor:
            if None in registro or any(valor is None for valor in registro.values()):
                raise ValueError(f"Quantidade de campos inválida na linha {leitor.line_num}.")
            try:
                registro["frequencia"] = int(registro["frequencia"])
                registro["duracao"] = float(registro["duracao"])
            except ValueError as erro:
                raise ValueError(
                    f"Frequência ou duração inválida na linha {leitor.line_num}."
                ) from erro
            if (
                registro["frequencia"] < 0
                or registro["duracao"] < 0
                or not math.isfinite(registro["duracao"])
            ):
                raise ValueError(f"Valor numérico inválido na linha {leitor.line_num}.")
            registros_carregados.append(registro)

    return registros_carregados


def salvar_registros(registros):
    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)

        escritor.writeheader()
        escritor.writerows(registros)

try:
    registros = carregar_registros()
except (OSError, ValueError, csv.Error) as erro:
    print(f"Não foi possível carregar registros.csv: {erro}")
    print("O programa foi encerrado sem alterar o CSV. Confira o arquivo antes de tentar novamente.")
    sys.exit(1)

while opcao != 4:
    print("\n=== COMPORTADATA ===")
    print("1 - Novo registro")
    print("2 - Ver registros")
    print("3 - Analisar dados")
    print("4 - Sair")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        data = input("Digite a data do registro (dd/mm/aaaa): ").strip()
        antecedente = input("Digite o antecedente: ").strip().lower()
        comportamento = input("Digite o comportamento: ").strip().lower()
        consequencia = input("Digite a consequência: ").strip().lower()

        frequencia = int(input("Quantas vezes ocorreu? "))
        duracao = float(input("Qual foi a duração em minutos? "))

        registro = {
            "data": data,
            "antecedente": antecedente,                 
            "comportamento": comportamento,
            "consequencia": consequencia,
            "frequencia": frequencia,
            "duracao": duracao
        }
        registros.append(registro)

        salvar_registros(registros)

        print("\nRegistro salvo com sucesso!")

        print("\n===== REGISTRO =====")
        print("Data:", data)
        print("Antecedente:", antecedente)
        print("Comportamento:", comportamento)
        print("Consequência:", consequencia)
        print("Frequência:", frequencia)
        print("Duração:", duracao, "minutos")

    elif opcao == 2:
        if len(registros) == 0:
            print("\nNenhum registro cadastrado.")
        else:
            print("\n=== REGISTROS ===")

            for registro in registros:
                print("Data:", registro["data"])
                print("Antecedente:", registro["antecedente"])
                print("Comportamento:", registro["comportamento"])
                print("Consequência:", registro["consequencia"])
                print("Frequência:", registro["frequencia"])
                print("Duração:", registro["duracao"], "minutos")
                print("------------------------")
        
    elif opcao == 3:
        if len(registros) == 0:
            print("\nNão existem dados suficientes para análise.")
            continue

        print("\n=== ANÁLISE DOS DADOS ===")

        quantidade = len(registros)

        frequencia_total = 0
        duracao_total = 0

        contagem_comportamentos = {}
        contagem_antecedentes = {}
        contagem_consequencias = {}

        for registro in registros:
            frequencia_total += registro["frequencia"]
            duracao_total += registro["duracao"]

            comportamento = registro["comportamento"]
            antecedente = registro["antecedente"]
            consequencia = registro["consequencia"]

            if comportamento in contagem_comportamentos:
                contagem_comportamentos[comportamento] += 1
            else:
                contagem_comportamentos[comportamento] = 1

            if antecedente in contagem_antecedentes:
                contagem_antecedentes[antecedente] += 1
            else:
                contagem_antecedentes[antecedente] = 1

            if consequencia in contagem_consequencias:
                contagem_consequencias[consequencia] += 1
            else:
                contagem_consequencias[consequencia] = 1

        media_duracao = duracao_total / quantidade

        comportamento_mais_frequente = max(
            contagem_comportamentos,
            key=contagem_comportamentos.get
        )

        antecedente_mais_frequente = max(
            contagem_antecedentes,
            key=contagem_antecedentes.get
        )

        consequencia_mais_frequente = max(
            contagem_consequencias,
            key=contagem_consequencias.get
        )

        print("Quantidade de registros:", quantidade)
        print("Frequência total:", frequencia_total)
        print("Duração média:", round(media_duracao, 2), "minutos")
        print("Comportamento mais frequente:", comportamento_mais_frequente)
        print("Antecedente mais frequente:", antecedente_mais_frequente)
        print("Consequência mais frequente:", consequencia_mais_frequente)

    elif opcao == 4:
        print("Encerrando o programa...")

    else:
        print("Opção inválida.")


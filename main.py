import csv
from datetime import datetime
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


def ler_texto(mensagem):
    """Solicita um texto obrigatório e mantém a padronização em minúsculas."""
    while True:
        valor = input(mensagem).strip().lower()
        if valor:
            return valor
        print("Este campo não pode ficar vazio. Digite uma descrição.")


def ler_data():
    """Solicita uma data existente no formato dd/mm/aaaa."""
    while True:
        valor = input("Digite a data do registro (dd/mm/aaaa): ").strip()
        try:
            data = datetime.strptime(valor, "%d/%m/%Y")
            formato = f"{data.day:02d}/{data.month:02d}/{data.year:04d}"
            if valor == formato:
                return valor
        except ValueError:
            pass
        print("Data inválida. Use dd/mm/aaaa, por exemplo: 30/09/2026.")


def ler_inteiro(mensagem, minimo=0, maximo=None):
    """Repete a pergunta até receber um inteiro dentro dos limites."""
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor >= minimo and (maximo is None or valor <= maximo):
                return valor
        except ValueError:
            pass
        if maximo is None:
            print(f"Digite um número inteiro maior ou igual a {minimo}.")
        else:
            print(f"Digite um número inteiro entre {minimo} e {maximo}.")


def ler_duracao():
    """Aceita minutos não negativos com ponto ou vírgula decimal."""
    while True:
        try:
            texto = input("Qual foi a duração em minutos? ").strip()
            valor = float(texto.replace(",", "."))
            if math.isfinite(valor) and valor >= 0:
                return valor
        except ValueError:
            pass
        print("Digite uma duração válida maior ou igual a zero, como 1,5 ou 1.5.")


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

    opcao = ler_inteiro("Escolha uma opção: ", minimo=1, maximo=4)

    if opcao == 1:
        data = ler_data()
        antecedente = ler_texto("Digite o antecedente: ")
        comportamento = ler_texto("Digite o comportamento: ")
        consequencia = ler_texto("Digite a consequência: ")

        frequencia = ler_inteiro("Quantas vezes ocorreu? ")
        duracao = ler_duracao()

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

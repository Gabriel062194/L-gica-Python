import json
import os
from datetime import datetime

ARQUIVO_PRODUTOS = "produtos.json"
ARQUIVO_MOVIMENTACOES = "movimentacoes.json" # Arquivos usados para armazenar os dados

# FUNÇÕES DE ARMAZENAMENTO

def carregar_dados(arquivo): # Carrega os dados de um arquivo JSON

    try:
        if not os.path.exists(arquivo):
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump([], f)

        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

            if not isinstance(dados, list):
                raise ValueError("Formato de arquivo invalidado.")

            return dados

    except (json.JSONDecodeError, OSError, ValueError) as erro:
        print(f"Erro ao carregar {arquivo}: {erro}")
        return []

def salvar_dados(arquivo, dados): # Salva os dados no arquivo JSON

    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        return True

    except OSError as erro:
        print(f"Erro ao salvar arquivo: {erro}")
        return False

# FUNÇÕES AUXILIARES

def buscar_produto(codigo):
    produtos = carregar_dados(ARQUIVO_PRODUTOS)

    for produto in produtos:
        if produto["codigo"] == codigo:
            return produto

    return None

def ler_inteiro(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))

            if minimo is not None and valor < minimo:
                print(f"Por gentileza, informe um valor maior ou igual a {minimo}.")
                continue

            return valor

        except ValueError:
            print("Digite um número inteiro válido.")

def ler_preco(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))

            if valor <= 0:
                print("O preço deve ser maior que zero.")
                continue

            return valor

        except ValueError:
            print("Digite um preço válido.")

# CADASTRO DE PRODUTOS

def cadastrar_produto():
    produtos = carregar_dados(ARQUIVO_PRODUTOS)

    print("\n===== CADASTRAR PRODUTO =====")

    codigo = ler_inteiro("Código: ", 1)

    if buscar_produto(codigo):
        print("Já existe um produto cadastrado com esse mesmo código! Por gentileza, insira um inédito.")
        return

    nome = input("Nome do produto: ").strip()

    if not nome:
        print("O nome é de caráter obrigatório!")
        return

    quantidade = ler_inteiro("Quantidade inicial: ", 0)
    minimo = ler_inteiro("Estoque mínimo: ", 0)
    preco = ler_preco("Preço unitário: R$ ")

    produto = {
        "codigo": codigo,
        "nome": nome,
        "quantidade": quantidade,
        "estoque_minimo": minimo,
        "preco": preco
    }

    produtos.append(produto)

    if salvar_dados(ARQUIVO_PRODUTOS, produtos):
        print("Produto registrado com sucesso!")

def listar_produtos():
    produtos = carregar_dados(ARQUIVO_PRODUTOS)

    print("\n===== LISTA DE PRODUTOS =====")

    if not produtos:
        print("Nenhum produto foi cadastrado.")
        return

    print("-" * 75)
    print(f"{"Código":<10}{"Nome":<25}{"Quantidade":<15}{"Mínimo":<10}{"Preço":<10}")
    print("-" * 75)

    for p in produtos:
        print(
            f"{p["codigo"]:<10}"
            f"{p["nome"]:<25}"
            f"{p["quantidade"]:<15}"
            f"{p["estoque_minimo"]:<10}"
            f"R$ {p["preco"]:.2f}"
        )

    print("-" * 75)

def alterar_produto():
    produtos = carregar_dados(ARQUIVO_PRODUTOS)

    print("\n===== ALTERAR PRODUTO =====")

    codigo = ler_inteiro("Código do produto: ", 1)

    for produto in produtos:
        if produto["codigo"] == codigo:

            print(f"Produto encontrado: {produto["nome"]}")

            nome = input("Novo nome (ENTER mantém): ").strip()
            if nome:
                produto["nome"] = nome

            produto["estoque_minimo"] = ler_inteiro(
                "Novo estoque mínimo: ", 0
            )

            produto["preco"] = ler_preco("Novo preço: R$ ")

            if salvar_dados(ARQUIVO_PRODUTOS, produtos):
                print("Produto alterado com sucesso!")

            return

    print("Produto não encontrado em nosso sistema!")

def excluir_produto():
    produtos = carregar_dados(ARQUIVO_PRODUTOS)

    print("\n===== EXCLUIR PRODUTO =====")

    codigo = ler_inteiro("Código do produto: ", 1)

    for produto in produtos:
        if produto["codigo"] == codigo:

            confirmacao = input(
                f"Confirma a exclusão de {produto["nome"]}? (S/N): "
            ).upper()

            if confirmacao == "S":
                produtos.remove(produto)

                if salvar_dados(ARQUIVO_PRODUTOS, produtos):
                    print("Produto excluído com sucesso!")

            return

    print("Produto não encontrado!")

# MOVIMENTAÇÃO DE ESTOQUE

def registrar_movimentacao(tipo):
    produtos = carregar_dados(ARQUIVO_PRODUTOS)

    print(f"\n===== REGISTRAR {tipo.upper()} =====")

    codigo = ler_inteiro("Código do produto: ", 1)

    produto = None

    for p in produtos:
        if p["codigo"] == codigo:
            produto = p
            break

    if produto is None:
        print("Produto não encontrado!")
        return

    print(f"Produto: {produto["nome"]}")
    print(f"Estoque atual: {produto["quantidade"]}")

    quantidade = ler_inteiro("Quantidade: ", 1)

    if tipo == "SAÍDA":
        if quantidade > produto["quantidade"]:
            print("ERRO: estoque insuficiente!")
            return

        produto["quantidade"] -= quantidade

    else:
        produto["quantidade"] += quantidade

    movimentacoes = carregar_dados(ARQUIVO_MOVIMENTACOES)

    movimentacao = {
        "codigo_produto": codigo,
        "nome_produto": produto["nome"],
        "tipo": tipo,
        "quantidade": quantidade,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    movimentacoes.append(movimentacao)

    if salvar_dados(ARQUIVO_PRODUTOS, produtos): # Vai salvar os dois arquivos
        if salvar_dados(ARQUIVO_MOVIMENTACOES, movimentacoes):
            print(f"{tipo} registrada com absoluto êxito!")
            print(f"Novo estoque: {produto["quantidade"]}")

def registrar_entrada():
    registrar_movimentacao("ENTRADA")

def registrar_saida():
    registrar_movimentacao("SAÍDA")

# CONSULTA DE ESTOQUE

def consultar_produto():
    print("\n===== CONSULTAR PRODUTO =====")
    print("1 - Consultar por código")
    print("2 - Consultar por nome")

    opcao = input("Escolha: ")

    produtos = carregar_dados(ARQUIVO_PRODUTOS)

    if opcao == "1":
        codigo = ler_inteiro("Código: ", 1)

        resultados = [
            p for p in produtos
            if p["codigo"] == codigo
        ]

    elif opcao == "2":
        nome = input("Nome do produto: ").strip().lower()

        resultados = [
            p for p in produtos
            if nome in p["nome"].lower()
        ]

    else:
        print("Opção inválida!")
        return

    if not resultados:
        print("Nenhum produto encontrado.")
        return

    for p in resultados:
        print("\nCódigo:", p["codigo"])
        print("Nome:", p["nome"])
        print("Quantidade:", p["quantidade"])
        print("Estoque mínimo:", p["estoque_minimo"])
        print(f"Preço: R$ {p["preco"]:.2f}")

# PRODUTOS COM ESTOQUE LIMITADO

def produtos_estoque_baixo():
    produtos = carregar_dados(ARQUIVO_PRODUTOS)

    print("\n===== PRODUTOS COM ESTOQUE BAIXO =====")

    encontrados = False

    for p in produtos:

        if p["quantidade"] <= p["estoque_minimo"]:

            encontrados = True

            print(
                f"Produto: {p["nome"]} | "
                f"Quantidade: {p["quantidade"]} | "
                f"Mínimo: {p["estoque_minimo"]}"
            )

    if not encontrados:
        print("Nenhum produto foi vistoriado com estoque baixo.")

# RELATÓRIO DE MOVIMENTAÇÕES

def relatorio_movimentacoes():
    movimentacoes = carregar_dados(ARQUIVO_MOVIMENTACOES)

    print("\n===== RELATÓRIO DE TRANSAÇÕES =====")

    if not movimentacoes:
        print("Nenhuma movimentação registrada.")
        return

    for m in movimentacoes:
        print(
            f"Data: {m["data"]} | "
            f"Produto: {m["nome_produto"]} | "
            f"Tipo: {m["tipo"]} | "
            f"Quantidade: {m["quantidade"]}"
        )

# MENU PRINCIPAL

def menu():
    while True:

        print("\n")
        print("=" * 45)
        print("       SISTEMA DE CONTROLE DE ESTOQUE")
        print("=" * 45)

        print("1 - Cadastrar produto")
        print("2 - Alterar produto")
        print("3 - Excluir produto")
        print("4 - Listar produtos")
        print("5 - Registrar entrada")
        print("6 - Registrar saída")
        print("7 - Consultar produto")
        print("8 - Produtos com estoque limitado")
        print("9 - Relatório de movimentações")
        print("0 - Sair")

        print("=" * 45)

        opcao = input("Escolha uma opção daquelas ofertadas: ")

        if opcao == "1":
            cadastrar_produto()

        elif opcao == "2":
            alterar_produto()

        elif opcao == "3":
            excluir_produto()

        elif opcao == "4":
            listar_produtos()

        elif opcao == "5":
            registrar_entrada()

        elif opcao == "6":
            registrar_saida()

        elif opcao == "7":
            consultar_produto()

        elif opcao == "8":
            produtos_estoque_baixo()

        elif opcao == "9":
            relatorio_movimentacoes()

        elif opcao == "0":
            print("Sistema encerrado. Até breve!")
            break

        else:
            print("Opção invalidada! Tente de novo.")

# EXECUÇÃO DO SISTEMA

if __name__ == "__main__":
    menu()


    
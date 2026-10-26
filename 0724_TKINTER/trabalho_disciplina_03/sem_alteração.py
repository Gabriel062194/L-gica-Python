import json
import os
from datetime import datetime

ARQUIVO = "movimentacoes.json"

def carregar_dados(): # Carrega as movimentações salvas no arquivo JSON
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, ensure_ascii=False, indent=4)
        return []

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        print("Erro: o arquivo JSON está vazio ou inválido.")
        return []

def salvar_dados(movimentacoes): # Salva as movimentações no arquivo JSON
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(
            movimentacoes,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

def gerar_id(movimentacoes): # Gera o próximo identificador disponível
    if not movimentacoes:
        return 1

    return max(m["id"] for m in movimentacoes) + 1

def adicionar_movimentacao(movimentacoes, tipo): # Adiciona uma receita ou despesa
    descricao = input("Digite a descrição: ").strip()

    if not descricao:
        print("Erro: a descrição não pode ficar vazia.")
        return

    try:
        valor = float(input("Digite o valor: R$ ").replace(",", "."))

        if valor <= 0:
            print("Erro: o valor deve ser maior que zero.")
            return

    except ValueError:
        print("Erro: digite um valor numérico válido.")
        return

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    movimentacao = {
        "id": gerar_id(movimentacoes),
        "descricao": descricao,
        "valor": valor,
        "tipo": tipo,
        "data": data
    }

    movimentacoes.append(movimentacao)
    salvar_dados(movimentacoes)

    print(f"{tipo} cadastrada com sucesso!")
    print(f"Identificador: {movimentacao['id']}")
    print(f"Data e hora: {data}")

def listar_movimentacoes(movimentacoes): # Lista todas as movimentações
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return

    print("\n===== MOVIMENTAÇÕES FINANCEIRAS =====")

    for m in movimentacoes:
        print("-" * 40)
        print(f"ID: {m['id']}")
        print(f"Descrição: {m['descricao']}")
        print(f"Valor: R$ {m['valor']:.2f}")
        print(f"Tipo: {m['tipo']}")
        print(f"Data: {m['data']}")

def consultar_saldo(movimentacoes): # Calcula e consulta o saldo atual
    receitas = sum(
        m["valor"] for m in movimentacoes
        if m["tipo"] == "Receita"
    )

    despesas = sum(
        m["valor"] for m in movimentacoes
        if m["tipo"] == "Despesa"
    )

    saldo = receitas - despesas

    print("\n===== SALDO FINANCEIRO =====")
    print(f"Total de receitas: R$ {receitas:.2f}")
    print(f"Total de despesas: R$ {despesas:.2f}")
    print(f"Saldo atual: R$ {saldo:.2f}")

def excluir_movimentacao(movimentacoes): # Exclui uma movimentação pelo identificador
    if not movimentacoes:
        print("Não há movimentações para excluir.")
        return

    listar_movimentacoes(movimentacoes)

    try:
        identificador = int(
            input("\nDigite o ID da movimentação a excluir: ")
        )
    except ValueError:
        print("Erro: digite um identificador numérico válido.")
        return

    for m in movimentacoes:
        if m["id"] == identificador:
            movimentacoes.remove(m)
            salvar_dados(movimentacoes)
            print("Movimentação excluída com sucesso!")
            return

    print("Erro: movimentação não encontrada.")

def gerar_relatorio(movimentacoes): # Gera o relatório financeiro
    receitas = sum(
        m["valor"] for m in movimentacoes
        if m["tipo"] == "Receita"
    )

    despesas = sum(
        m["valor"] for m in movimentacoes
        if m["tipo"] == "Despesa"
    )

    saldo = receitas - despesas
    quantidade = len(movimentacoes)

    print("\n===== RELATÓRIO FINANCEIRO =====")
    print(f"Total de receitas: R$ {receitas:.2f}")
    print(f"Total de despesas: R$ {despesas:.2f}")
    print(f"Saldo atual: R$ {saldo:.2f}")
    print(f"Quantidade de movimentações: {quantidade}")

def menu(): # Menu principal do sistema
    movimentacoes = carregar_dados()

    while True:
        print("\n===== CONTROLE DE GASTOS PESSOAIS =====")
        print("1 - Adicionar Receita")
        print("2 - Adicionar Despesa")
        print("3 - Listar Movimentações")
        print("4 - Consultar Saldo")
        print("5 - Excluir Movimentação")
        print("6 - Gerar Relatório")
        print("7 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_movimentacao(movimentacoes, "Receita")

        elif opcao == "2":
            adicionar_movimentacao(movimentacoes, "Despesa")

        elif opcao == "3":
            listar_movimentacoes(movimentacoes)

        elif opcao == "4":
            consultar_saldo(movimentacoes)

        elif opcao == "5":
            excluir_movimentacao(movimentacoes)

        elif opcao == "6":
            gerar_relatorio(movimentacoes)

        elif opcao == "7":
            print("Sistema encerrado. Até logo!")
            break

        else:
            print("Opção inválida! Escolha uma opção de 1 a 7")

if __name__ == "__main__": # Inicia o programa
    menu()
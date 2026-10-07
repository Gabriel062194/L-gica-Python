import os

ARQUIVO_SALDO = "contas.txt"
SALDO_INICIAL = 1000.00

def buscar_saldo(conta): # Busca o saldo da conta no arquivo.
    
    if not os.path.exists(ARQUIVO_SALDO):
        return SALDO_INICIAL

    with open(ARQUIVO_SALDO, "r") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(";")

            if len(dados) == 2 and dados[0] == conta:
                return float(dados[1])

    # Se a conta ainda não existir, começa com R$ 1.000,00
    return SALDO_INICIAL

def salvar_saldo(conta, saldo): # Salva ou atualiza o saldo da conta no arquivo.
    
    contas = {}

    if os.path.exists(ARQUIVO_SALDO):
        with open(ARQUIVO_SALDO, "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")

                if len(dados) == 2:
                    contas[dados[0]] = dados[1]

    contas[conta] = f"{saldo:.2f}"

    with open(ARQUIVO_SALDO, "w") as arquivo:
        for numero_conta, valor in contas.items():
            arquivo.write(f"{numero_conta};{valor}\n")

def valor_valido(valor): # Verifica se o valor é considerado inteiro e não negativo.
    
    if valor < 0:
        return False

    if valor != int(valor):
        return False

    return True

def realizar_saque(saldo): # Realiza o saque e informa a quantidade de cada cédula.
    
    valor = input("Digite o valor que deseja sacar: R$ ")

    try:
        valor = float(valor.replace(",", "."))

        if not valor_valido(valor):
            print("Erro: informe um valor inteiro e não negativo.")
            return saldo

        valor = int(valor)

        if valor == 0:
            print("Erro: o valor do saque deve ser maior que zero.")
            return saldo

        if valor > saldo:
            print("Erro: saldo insuficiente.")
            return saldo

        # Cédulas disponíveis no caixa
        cedulas = [100, 50, 20, 10, 5, 2]

        # Verifica se é possível formar o valor com as cédulas disponíveis
        restante = valor
        quantidade_cedulas = {}

        for cedula in cedulas:
            quantidade = restante // cedula
            quantidade_cedulas[cedula] = quantidade
            restante = restante % cedula

        if restante != 0:
            print("Erro: o caixa não possui cédulas para formar esse valor.")
            print("Digite um valor que possa ser formado pelas cédulas disponíveis.")
            return saldo

        # Atualiza o saldo
        saldo -= valor

        print("\nSaque realizado com sucesso!")
        print(f"Valor sacado: R$ {valor:.2f}")
        print("Cédulas entregues:")

        for cedula in cedulas:
            quantidade = quantidade_cedulas[cedula]

            if quantidade > 0:
                print(f"R$ {cedula}: {quantidade} cédula(s)")

        print(f"Novo saldo: R$ {saldo:.2f}")

        return saldo

    except ValueError:
        print("Erro: digite apenas valores numéricos.")
        return saldo

def realizar_deposito(saldo): # Efetua um depósito.
    
    valor = input("Digite o valor que deseja depositar: R$ ")

    try:
        valor = float(valor.replace(",", "."))

        if not valor_valido(valor):
            print("Erro: o depósito não pode ser negativo ou fracionário.")
            return saldo

        valor = int(valor)

        if valor == 0:
            print("Erro: o valor do depósito deve ser maior que zero.")
            return saldo

        saldo += valor

        print("\nDepósito realizado com sucesso!")
        print(f"Valor depositado: R$ {valor:.2f}")
        print(f"Novo saldo: R$ {saldo:.2f}")

        return saldo

    except ValueError:
        print("Erro: digite apenas valores numéricos.")
        return saldo

# INÍCIO DO PROGRAMA

print("=" * 40)
print("       CAIXA ELETRÔNICO")
print("=" * 40)

conta = input("Digite o número da conta: ")

# O número da conta é usado apenas para identificar o saldo.
saldo = buscar_saldo(conta)

print(f"\nConta acessada: {conta}")
print(f"Saldo disponível: R$ {saldo:.2f}")

while True:
    print("\n" + "=" * 40)
    print("             MENU")
    print("=" * 40)
    print("1 - Consultar saldo")
    print("2 - Sacar dinheiro")
    print("3 - Depositar dinheiro")
    print("4 - Sair")
    print("=" * 40)

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print(f"\nSeu saldo atual é: R$ {saldo:.2f}")

    elif opcao == "2":
        saldo = realizar_saque(saldo)

    elif opcao == "3":
        saldo = realizar_deposito(saldo)

    elif opcao == "4":
        salvar_saldo(conta, saldo)

        print("\nOperação finalizada.")
        print(f"Saldo salvo: R$ {saldo:.2f}")
        print("Obrigado por utilizar o caixa eletrônico!")
        break

    else:
        print("\nErro: opção inválida. Escolha uma opção de 1 a 4.")
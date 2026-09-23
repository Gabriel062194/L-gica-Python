import os

ARQUIVO_SALDO = "contas.txt"

CEDULAS = [100, 50, 20, 10, 5, 2]

def carregar_saldo(conta): # O saldo da conta é buscado no arquivo.
    
    if os.path.exists(ARQUIVO_SALDO):
        with open(ARQUIVO_SALDO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")

                if len(dados) == 2 and dados[0] == conta:
                    return float(dados[1])

    # Conta inativa
    
    return 1000.00

def salvar_saldo(conta, saldo): # Salva/atualiza no arquivo o saldo da conta.

    contas = {}

    if os.path.exists(ARQUIVO_SALDO):
        with open(ARQUIVO_SALDO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")

                if len(dados) == 2:
                    contas[dados[0]] = dados[1]

    contas[conta] = f"{saldo:.2f}"

    with open(ARQUIVO_SALDO, "w", encoding="utf-8") as arquivo:
        for numero_conta, valor in contas.items():
            arquivo.write(f"{numero_conta};{valor}\n")

def consta_valor_inteiro(valor): # Análise para saber se o valor informado é inteiro ou não.
    
    return valor.is_integer()

def calcular_cedulas(valor): # Cálculo da quantidade de cédulas para o saque do cliente.
    
    quantidade_cedulas = {}

    for cedula in CEDULAS:
        quantidade = valor // cedula
        quantidade_cedulas[cedula] = int(quantidade)
        valor %= cedula

    return quantidade_cedulas, valor

# PROGRAMA INICIALIZANDO

print("=" * 40)
print("       CAIXA ELETRÔNICO")
print("=" * 40)

conta = input("Por favor, comece digitando o número da conta: ")
senha = input("Agora, avance com a senha: ")

# Senha solicitada, porém não validada.
saldo = carregar_saldo(conta)

# A senha é solicitada, mas não é validada.
saldo = carregar_saldo(conta)

print("\nAcesso realizado com sucesso!")

while True:
    print("\n" + "=" * 40)
    print("MENU")
    print("=" * 40)
    print("1 - Consultar saldo")
    print("2 - Sacar dinheiro")
    print("3 - Depositar dinheiro")
    print("4 - Sair")
    print("=" * 40)

    opcao = input("Escolha uma opção: ")

    # CONSULTAR SALDO
    if opcao == "1":
        print(f"\nSeu saldo atual é: R$ {saldo:.2f}")

    # SACAR DINHEIRO
    elif opcao == "2":
        valor_texto = input("Digite o valor que deseja sacar: R$ ")

        try:
            valor = float(valor_texto.replace(",", "."))

            if valor < 0:
                print("Erro: o valor do saque não pode ser negativo.")

            elif not eh_valor_inteiro(valor):
                print("Erro: o caixa não aceita valores fracionários.")

            elif valor == 0:
                print("Erro: o valor do saque deve ser maior que zero.")

            elif valor > saldo:
                print("Erro: saldo insuficiente para realizar o saque.")

            else:
                cedulas, resto = calcular_cedulas(valor)

                # Se sobrar algum valor, o caixa não consegue formar o saque.
                if resto != 0:
                    print(
                        "Erro: o caixa não possui cédulas suficientes "
                        "para formar esse valor."
                    )
                    print(
                        "Valores devem ser compatíveis com as cédulas "
                        "disponíveis: R$ 100, R$ 50, R$ 20, R$ 10, R$ 5 e R$ 2."
                    )

                else:
                    saldo -= valor

                    print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")
                    print("Cédulas entregues:")

                    for cedula in CEDULAS:
                        quantidade = cedulas[cedula]

                        if quantidade > 0:
                            print(f"R$ {cedula}: {quantidade} cédula(s)")

                    print(f"Saldo restante: R$ {saldo:.2f}")

        except ValueError:
            print("Erro: digite um valor numérico válido.")

    # DEPOSITAR DINHEIRO
    elif opcao == "3":
        valor_texto = input("Digite o valor que deseja depositar: R$ ")

        try:
            valor = float(valor_texto.replace(",", "."))

            if valor < 0:
                print("Erro: o valor do depósito não pode ser negativo.")

            elif valor == 0:
                print("Erro: o valor do depósito deve ser maior que zero.")

            else:
                saldo += valor

                print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
                print(f"Novo saldo: R$ {saldo:.2f}")

        except ValueError:
            print("Erro: digite um valor numérico válido.")

    # SAIR
    elif opcao == "4":
        salvar_saldo(conta, saldo)

        print("\nOperação encerrada.")
        print(f"Saldo salvo: R$ {saldo:.2f}")
        print("Obrigado por utilizar o caixa eletrônico!")
        break

    # OPÇÃO INVÁLIDA
    else:
        print("Erro: opção inválida. Escolha uma opção de 1 a 4.")
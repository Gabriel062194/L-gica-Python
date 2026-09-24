import os

ARQUIVO_SALDO = "contas.txt"

CEDULAS = [100, 50, 20, 10, 5, 2]
SENHA_PADRAO = "1234"
SALDO_INICIAL = 1000.00


def carregar_saldo(conta):
    """Busca o saldo da conta no arquivo."""
    
    if os.path.exists(ARQUIVO_SALDO):
        with open(ARQUIVO_SALDO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")

                if len(dados) == 2 and dados[0] == conta:
                    try:
                        return float(dados[1])
                    except ValueError:
                        return SALDO_INICIAL

    # Conta nova começa com o saldo inicial
    return SALDO_INICIAL


def salvar_saldo(conta, saldo):
    """Salva ou atualiza o saldo da conta no arquivo."""

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


def calcular_cedulas(valor):
    """Calcula a quantidade de cada cédula necessária para o saque."""

    quantidade_cedulas = {}

    for cedula in CEDULAS:
        quantidade = valor // cedula
        quantidade_cedulas[cedula] = quantidade
        valor %= cedula

    return quantidade_cedulas, valor


def realizar_saque(saldo):
    """Realiza o saque e retorna o novo saldo."""

    valor_texto = input(
        "Digite o valor com o qual deseja sacar de sua conta: R$ "
    )

    try:
        valor = float(valor_texto.replace(",", "."))
    except ValueError:
        print("ERRO: faça a digitação de uma quantia válida.")
        return saldo

    if valor <= 0:
        print("ERRO: a quantia sacada deve ser superior a zero.")
        return saldo

    if not valor.is_integer():
        print("ERRO: este caixa não aceita valores fracionados.")
        return saldo

    if valor > saldo:
        print("ERRO: quantia maior que o saldo disponível.")
        return saldo

    # Trabalhamos com inteiro porque as cédulas são inteiras.
    valor = int(valor)

    cedulas, resto = calcular_cedulas(valor)

    if resto != 0:
        print(
            "ERRO: este caixa não possui cédulas suficientes "
            "para formar o valor solicitado."
        )
        print(
            "Os valores devem ser compatíveis com as cédulas: "
            "R$ 100, R$ 50, R$ 20, R$ 10, R$ 5 e R$ 2."
        )
        return saldo

    saldo -= valor

    print(f"\nSaque de R$ {valor:.2f} efetuado com sucesso!")
    print("Cédulas entregues ao cliente:")

    for cedula in CEDULAS:
        quantidade = cedulas[cedula]

        if quantidade > 0:
            print(f"R$ {cedula}: {quantidade} cédula(s)")

    print(f"Saldo restante: R$ {saldo:.2f}")

    return saldo


def realizar_deposito(saldo):
    """Realiza um depósito e retorna o novo saldo."""

    valor_texto = input(
        "Digite a quantia desejada para o depósito: R$ "
    )

    try:
        valor = float(valor_texto.replace(",", "."))
    except ValueError:
        print("ERRO: faça a digitação de uma quantia válida.")
        return saldo

    if valor <= 0:
        print("ERRO: o valor do depósito deve ser superior a zero.")
        return saldo

    saldo += valor

    print(f"\nDepósito de R$ {valor:.2f} efetuado com sucesso!")
    print(f"Novo saldo: R$ {saldo:.2f}")

    return saldo


def exibir_menu():
    """Exibe o menu principal."""

    print("\n" + "=" * 40)
    print("MENU")
    print("=" * 40)
    print("1 - Consulta de saldo")
    print("2 - Saque rápido")
    print("3 - Deposite aqui o seu dinheiro")
    print("4 - Sair")
    print("=" * 40)


def autenticar():
    """Solicita conta e senha ao usuário."""

    print("=" * 40)
    print("       CAIXA ELETRÔNICO")
    print("=" * 40)

    conta = input("Por favor, digite o número da conta: ")
    senha = input("Agora, digite a senha: ")

    if senha != SENHA_PADRAO:
        print("\nERRO: senha incorreta.")
        return None

    print("\nAcesso permitido com sucesso!")

    return conta


# PROGRAMA PRINCIPAL

conta = autenticar()

if conta is not None:

    saldo = carregar_saldo(conta)

    while True:

        exibir_menu()

        opcao = input("Escolha uma das quatro opções: ")

        # OPÇÃO 1 - CONSULTA DE SALDO
        if opcao == "1":
            print(f"\nSeu saldo atual é de: R$ {saldo:.2f}")

        # OPÇÃO 2 - SAQUE
        elif opcao == "2":
            saldo = realizar_saque(saldo)

            # Salva imediatamente após o saque
            salvar_saldo(conta, saldo)

        # OPÇÃO 3 - DEPÓSITO
        elif opcao == "3":
            saldo = realizar_deposito(saldo)

            # Salva imediatamente após o depósito
            salvar_saldo(conta, saldo)

        # OPÇÃO 4 - SAIR
        elif opcao == "4":
            salvar_saldo(conta, saldo)

            print("\nOperação encerrada.")
            print(f"Saldo salvo: R$ {saldo:.2f}")
            print(
                "Obrigado por utilizar o nosso caixa eletrônico! "
                "Até mais!"
            )

            break

        # OPÇÃO INVÁLIDA
        else:
            print(
                "ERRO: opção inválida. "
                "Por favor, escolha entre as opções disponíveis."
            )
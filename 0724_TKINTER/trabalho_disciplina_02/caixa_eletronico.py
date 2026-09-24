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

print("\nAcesso permitido com sucesso!")

while True:
    print("\n" + "=" * 40)
    print("MENU")
    print("=" * 40)
    print("1 - Consulta de saldo")
    print("2 - Saque Rápido")
    print("3 - Deposite aqui o seu dinheiro")
    print("4 - SAIR")
    print("=" * 40)

    opcao = input("Escolha umas das quatro opções: ")

    # OPÇÃO 1 - CONSULTA DE SALDO
    if opcao == "1":
        print(f"\nSeu saldo atual é de: R$ {saldo:.2f}")

    # OPÇÃO 2 - SAQUE RÁPIDO
    elif opcao == "2":
        valor_texto = input("Digite o valor com o qual desejas sacar de sua conta: R$ ")

        try:
            valor = float(valor_texto.replace(",", "."))
            if valor < 0:
                print("ERRO: o valor desse saque não poderá estar negativado.")
            elif not consta_valor_inteiro(valor):
                print("ERRO: este caixa não aceita valores fracionados.")
            elif valor == 0:
                print("ERRO: a quantia sacada deve de ser superior a zero.")
            elif valor > saldo:
                print("ERRO: quantia maior à que consta na conta.")
            else:
                cedulas, resto = calcular_cedulas(valor)

                # Caso ocorra de sobrar um valor razoável, o caixa fica impossibilitado de formar o saque.
                if resto != 0:
                    print("ERRO: este caixa não possui a quantidade suficiente de cédulas disponíveis para formar o valor solicitado.")
                    print("Os valores devem ser compatíveis com as cédulas já existentes: R$ 100, R$ 50, R$ 20, R$ 10, R$ 5 e R$ 2.")
                else:
                    saldo -= valor

                    print(f"\nSaque solicitado de R$ {valor:.2f} efetuado com sucesso! Faça bom proveito!")
                    print("Cédulas entregues ao cliente: ")

                    for cedula in CEDULAS:
                        quantidade = cedulas[cedula]

                        if quantidade > 0:
                            print(f"R$ {cedula}: {quantidade} cédula(s)")
                            
                    print(f"Saldo restante: R$ {saldo:.2f}")

        except ValueError:
            print("ERRO: faça a digitação de uma quantia válida.")

    # OPÇÃO 3 - DEPOSITE AQUI O SEU DINHEIRO
    elif opcao == "3":
        valor_texto = input("Digite a quantia desejável ao depósito: R$ ")

        try:
            valor = float(valor_texto.replace(",", "."))
            if valor < 0:
                print("ERRO: o valor do depósito não poderá estar negativado.")
            elif valor == 0:
                print("ERRO: o depósito solicitado deve de ser superior a zero.")
            else:
                saldo += valor

                print(f"\nDepósito solicitado de R$ {valor:.2f} efetuado com sucesso! Fique de olho nos rendimentos!")
                print(f"Novo saldo: R$ {saldo:.2f}")

        except ValueError:
            print("ERRO: faça a digitação de uma quantia válida.")

    # OPÇÃO 4 - SAIR
    elif opcao == "4":
        salvar_saldo(conta, saldo)

        print("\nOperação encerrada.")
        print(f"Saldo salvo: R$ {saldo:.2f}")
        print("Obrigado pela preferência de usar o nosso caixa eletrônico! Até mais!")
        break

    # "OPÇÃO 5" - INVALIDAÇÃO
    else:
        print("ERRO: opção invalidada. Por favor, escolha entre as opções ofertadas.")
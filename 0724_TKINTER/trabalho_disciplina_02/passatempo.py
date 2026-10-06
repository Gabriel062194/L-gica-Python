import random

print("\nOlá, tudo bem? Seja muito bem vindo ao nosso sistema de caixa eletrônico. Para começar, digite os seus dados de acesso!\n")

# Variáveis globais
balance = 1000
withdraw = 5
account_data = 0

cpf = int(input("Digite o seu CPF: "))
password = int(input("Agora, digite a sua senha: "))

# Bloco de Sistemas
if cpf == 123 and password == 123:
    print("Olá, seja muito bem vindo à sua conta")
    print("(1) EXTRATO\n(2) SACAR\n(3) DEPOSITAR\n(4) FECHAR")
    account_data = int(input("Digite o que você deseja realizar:"))

    if account_data == 1:
        account_number = random.randint(1000,9999) # Geração de números aleatórios

        print("Número da conta:", account_number)
        print("Saldo: R${:.2f}".format(balance))
        print("Saques disponíveis:", withdraw)

    elif account_data == 2:
        withdraw_ok = int(input("Digite um valor desejável para sacar: "))
        if withdraw_ok <= balance:
            balance = balance - withdraw_ok # Soma do valor da variável BALANCE depois de realizar o saque
            print("Você sacou R${:.2f} da sua conta.".format(withdraw_ok))
            print("Agora você possui R${:.2f} disponível em conta.".format(balance))
            withdraw = withdraw -1 # Saques ainda disponíveis
            print("Você só pode realizar mais {} saques da sua conta.".format(withdraw))

        else:
            print("Você não tem esse valor disponível na conta!")

    elif account_data == 3:
        deposit = int(input("Digite o valor que tu desejas depositar: "))
        balance = deposit + balance # Valor que o cliente terá na conta após depositar o dinheiro
        print("Você depositou R${:.2f} na sua conta com sucesso! O montante disponível restante ficou em R${:.2f}.".format(deposit, balance))

    elif account_data == 4:
        exit("Agradecemos pelo uso do nosso sistema. Até breve!")

    else:
        print("Opção inválida!")

else:
    print("Dados desatualizados e/ou inválidos! Tente novamente.")
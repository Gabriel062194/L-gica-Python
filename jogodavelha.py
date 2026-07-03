tabuleiro = [[" " for _ in range(3)] for _ in range(3)]

def mostrar_tabuleiro():
    print("\nTabuleiro:\n\n")
    for i in range(3):
        print(" | ".join(tabuleiro[i]))
        if i < 2:
            print("_" * 9)
        print()

def jogar():
    jogador_atual = "X"
    jogadas = 0

    while True:
        mostrar_tabuleiro()

        print(f"Jogador {jogador_atual}")
        linha = int(input("Escolha a linha (0, 1, 2): "))
        coluna = int(input("Escolha a coluna (0, 1, 2): "))

        if tabuleiro[linha][coluna] != " ":
            print("Posição já ocupada! Tente novamente.")
            continue
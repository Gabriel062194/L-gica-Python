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

        tabuleiro[linha][coluna] = jogador_atual
        jogadas += 1

        if verificar_vitoria(jogador_atual):
            mostrar_tabuleiro()
            print(f"O jogador {jogador_atual} venceu!")
            break

        if jogadas == 9:
            mostrar_tabuleiro()
            print("Empate!")
            break

        jogador_atual = "O" if jogador_atual == "X" else "X"
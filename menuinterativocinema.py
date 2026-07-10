def exibir_menu():
    print("=== MENU INTERATIVO DO CINEMA ===")
    print("1 - Listar filmes disponíveis")
    print("2 - Comprar ingresso")
    print("3 - Sair")

def cadastrar_filme(filmes):
    titulo = input("Digite o título do filme: ")
    genero = input("Digite o gênero do filme: ")
    filmes.append({"titulo": titulo, "genero": genero})
    print(f"Filme "{titulo} cadastrado com sucesso!)
          
def listar_filmes(filmes):
    if not filmes:
        print("Nenhum filme cadastrado.")
    else:
        print("Filmes disponíveis:")
        for i, filme in enumerate(filmes, start=1):
            print(f"{i}. {filme["titulo"]} - {filme["genero"]}")

def comprar_ingresso(filmes):
    if not filmes:
        print("Nenhum filme disponível para compra.")
        else:
        listar_filmes(filmes)
        escolha = int(input("Digite o número do filme que deseja comprar o ingresso: "))
        if 1 <= escolha <= len(filmes):
            filme_escolhido = filmes[escolha - 1]
            print(f"Ingresso comprado para o filme: {filme_escolhido["titulo"]}")
        
def main():
    filmes = []
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        if opçao == "1":
            listar_filmes(filmes)
        elif opçao == "2":
            comprar_ingresso(filmes)
        elif opçao == "3":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")
if __name__ == "__ main__":
    main()



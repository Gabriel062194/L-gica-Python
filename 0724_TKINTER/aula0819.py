from tkinter import *
from tkinter import ttk
import random
from PIL import Image, ImageTk

cor0 = "#FFFFFF"
cor1 = "#333333"
cor2 = "#fcc058"
cor3 = "#fff873"
cor4 = "#34eb3d"
cor5 = "#e85151"
fundo = "#3d3b3b"

janela = Tk()
janela.title("Pedra, Papel, Tesoura")
janela.geometry("260x280")
janela.configure(bg=fundo)


frame_cima = Frame(janela, width=260, height=100, bg=cor1, relief="raised")
frame_cima.grid(row=0, column=0, sticky=NW)
frame_baixo = Frame(janela, width=260, height=300, bg=cor0, relief="flat")
frame_baixo.grid(row=1, column=0, sticky=NW)

app_pessoa = Label(frame_cima, text="Jogador", height=1, anchor="center",
                   bg=cor1, fg=cor0, font=("Ivy 10 bold"))
app_pessoa.place(x=10, y=70)
app_pessoa_linha = Label(frame_cima, text="", height=1, anchor="center",
                         bg=cor1, fg=cor0, font=("Ivy 10 bold"))
app_pessoa.place(x=0, y=0)

app_vs = Label(frame_cima, text=":", height=1, anchor="center",
               bg=cor1, fg=cor0, font=("Ivy 30 bold"))
app_vs.place(x=125, y=20)

app_pessoa_pontos = Label(frame_cima, text="0", height=1, anchor="center",
                          bg=cor1, fg=cor0, font=("Ivy 30 bold"))
app_pessoa_pontos.place(x=50, y=20)

app_pc = Label(frame_cima, text="PC", height=1, anchor="center",
               bg=cor1, fg=cor0, font=("Ivy 10 bold"))
app_pc.place(x=205, y=70)
app_pc_linha = Label(frame_cima, text="", height=1, anchor="center",
                     bg=cor1, fg=cor0, font=("Ivy 10 bold"))
app_pc_linha.place(x=255, y=0)
app_pc_pontos = Label(frame_cima, text="0", height=1, anchor="center",
                      bg=cor1, fg=cor0, font=("Ivy 30 bold"))
app_pc_pontos.place(x=170, y=20)

app_empate = Label(frame_cima, text="", width=255, anchor="center",
                   bg=cor3, fg=cor0, font=("Ivy 10 bold"))
app_empate.place(x=0, y=95)


global escolha_pessoa
global escolha_pc
global pontos_pessoa
global rodadas
pontos_pessoa = 0
pontos_pc = 0
rodadas = 5


def terminar_jogo():
    pass

def jogar(jogada):
    global pontos_pessoa
    global pontos_pc
    global rodadas
    opcoes = ["pedra", "papel", "tesoura"]

    app_pessoa_linha["bg"] = cor0
    app_pc_linha["bg"] = cor0
    app_empate["bg"] = cor0

    if rodadas > 0:
        print(rodadas)
        escolha_pc = random.choice(opcoes)
        escolha_pessoa = jogada
        print(escolha_pessoa ["text"], escolha_pc)
        rodadas -= 1
    if testa_empate(escolha_pessoa, escolha_pc):
        app_empate["bg"] = cor3
    eli testa_vitoria_pessoa(escolha_pessoa)











 





    
    
    
    

    
    
    
    
    elif testa_vitoria_pessoa(escolha_pessoa, escolha_pc):
        pontos_pessoa +=10
        app_pessoa_linha["bg"] = cor4
    elif testa_vitoria_pc(escolha_pessoa, escolha_pc):
        pontos_pc += 10
        app_pc_linha["bg"] = cor4






    else:
        terminar_jogo()



def iniciar_jogo():
    global icone_pedra
    global icone_mao
    global icone_tesoura
    global icone_pedra
    global icone_mao
    global icone_tesoura

    icone_pedra = Image.open("./imagens/pedra.png")
    icone_pedra = icone_pedra.resize((50,50),Image.Resampling.LANCZOS)
    icone_pedra = ImageTk.PhotoImage(icone_pedra)
    bnt_pedra = Button(frame_baixo,command=lambda: jogar("pedra"),width=50, height=50,
                    image=icone_pedra, bg=cor0, fg=cor0,
                    compound="center",font=("ivy 10 bold"),
                    anchor="center", relief="flat")
    bnt_pedra.place(x=15, y=60)

    #icone_papel = Image.open("./imagens/papel.png")

    icone_mao = Image.open("./imagens/mao.png")
    icone_mao= icone_mao.resize((50,50),Image.Resampling.LANCZOS)
    icone_mao = ImageTk.PhotoImage(icone_mao)
    bnt_mao = Button(frame_baixo,command=lambda: jogar("papel"), width=50, height=50,
                    image=icone_mao, bg=cor0, fg=cor0,
                    compound="center",font=("ivy 10 bold"),
                    anchor="center", relief="flat")
    bnt_mao.place(x=100, y=60)


    icone_tesoura = Image.open("./imagens/tesoura.png")
    icone_tesoura= icone_tesoura.resize((50,50),Image.Resampling.LANCZOS)
    icone_tesoura = ImageTk.PhotoImage(icone_tesoura)
    bnt_tesoura = Button(frame_baixo,command=lambda: jogar("tesoura"), width=50, height=50,
                    image=icone_tesoura, bg=cor0, fg=cor0,
                    compound="center",font=("ivy 10 bold"),
                    anchor="center", relief="flat")
    bnt_tesoura.place(x=185, y=60)


bnt_iniciar = Button(frame_baixo, width=30, height=2,
                     command=iniciar_jogo,
                   bg=cor1, fg=cor0,
                   compound="center",font=("ivy 10 bold"),
                   anchor="center", relief="flat",text="jogar")

bnt_iniciar.place(x=5, y=130)

app_jogada_pc = Label(frame_baixo, text="", height=1,anchor="center",bg=cor0, fg=cor1, font=("ivy 10 bold"))
app_jogada_pc.place(x=190,y=10)

app_jogada_pessoa = Label(frame_baixo,text="",height=1,anchor="center",bg=cor0,fg=cor1, font=("ivy 10 bold"))
app_jogada_pessoa.place(x=10,y=10)

#app_vencedor = (frame_baixo,text="", height=1,)
terminar_jogo
janela.mainloop()

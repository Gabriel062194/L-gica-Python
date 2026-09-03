import tkinter as tk
from tkinter import ttk

# Dicionário das cores
DIGITOS = {
    "Preto": (0, "#000000"),
    "Marrom": (1, "#8B4513"),
    "Vermelho": (2, "#FF0000"),
    "Laranja": (3, "#FFA500"),
    "Amarelo": (4, "#FFFF00"),
    "Verde": (5, "#008000"),
    "Azul": (6, "#0000FF"),
    "Violeta": (7, "#EE82EE"),
    "Cinza": (8, "#808080"),
    "Branco": (9, "#FFFFFF")
}

# Dicionário dos multiplicadores
MULTIPLICADORES = {
    "Preto": (1, "#000000"),
    "Marrom": (10, "#8B4513"),
    "Vermelho": (100, "#FF0000"),
    "Laranja": (1000, "#FFA500"),
    "Amarelo": (10000, "#FFFF00"),
    "Verde": (100000, "#008000"),
    "Azul": (1000000, "#0000FF"),
    "Ouro": (0.1, "#D4AF37"),
    "Prata": (0.01, "#C0C0C0")
}

# Dicionário das tolerâncias
TOLERANCIAS = {
    "Marrom": ("±1%", "#8B4513"),
    "Vermelho": ("±2%", "#FF0000"),
    "Verde": ("±0.5%", "#008000"),
    "Azul": ("±0.25%", "#0000FF"),
    "Violeta": ("±0.1%", "#EE82EE"),
    "Ouro": ("±5%", "#D4AF37"),
    "Prata": ("±10%", "#C0C0C0")
}

def atualizar_resistor(*args):
    #1 - Obter as cores selecionadas
    c1 = var_f1.get()
    c2 = var_f2.get()
    cm = var_mult.get()
    ct = var_tol.get()

    #2 - Atualizar as cores das faixas no Canvas
    canvas.itemconfig(faixa1, fill=DIGITOS[c1][1])
    canvas.itemconfig(faixa2, fill=DIGITOS[c2][1])
    canvas.itemconfig(faixam, fill=MULTIPLICADORES[cm][1])
    canvas.itemconfig(faixat, fill=TOLERANCIAS[ct][1])

    #3 - Cálculo do valor da resistência
    val1 = DIGITOS[c1][0]
    val2 = DIGITOS[c2][0]
    mult = MULTIPLICADORES[cm][0]
    tol = TOLERANCIAS[ct][0]

    resistencia = (val1 * 10 + val2) * mult

    #4 - Formatar o valor da resistência
    if resistencia >= 1_000_000:
        res_str = f"{resistencia / 1_000_000:.2f} MΩ"
    elif resistencia >= 1_000:
        res_str = f"{resistencia / 1_000:.2f} kΩ"
    elif resistencia >= 1:
        res_str = f"{resistencia:.2f} Ω"
    else:
        res_str = f"{resistencia:.2f} Ω"

    #5 - Atualizando o resultado
    lbl_resultado.config(
        text=f"Resultado: {res_str} {tol}"
    )

# Configuração da janela principal
root = tk.Tk()
root.title("Calculadora de Resistores")
root.geometry("450x430")
root.resizable(False, False)

# Desenho do resistor
canvas = tk.Canvas(
    root,
    width=400,
    height=120,
    bg="#F0F0F0"
)
canvas.pack(pady=20)
# Fios do resistor
canvas.create_line(
    20, 60,
    380, 60,
    width=6,
    fill="#A0A0A0"
)
# Corpo do resistor
canvas.create_rectangle(
    100, 30,
    300, 90,
    fill="#EEDC82",
    outline="#D2B48C",
    width=2
)
# Faixas coloridas
faixa1 = canvas.create_rectangle(
    125, 30, 140, 90,
    fill="#000000",
    width=0
)
faixa2 = canvas.create_rectangle(
    160, 30, 175, 90,
    fill="#000000",
    width=0
)
faixam = canvas.create_rectangle(
    195, 30, 210, 90,
    fill="#000000",
    width=0
)
faixat = canvas.create_rectangle(
    260, 30, 275, 90,
    fill="#000000",
    width=0
)

# Variáveis dos menus
var_f1 = tk.StringVar(value="Marrom")
var_f2 = tk.StringVar(value="Preto")
var_mult = tk.StringVar(value="Vermelho")
var_tol = tk.StringVar(value="Ouro")

# Interface dos controles
frame_controles = tk.Frame(root)
frame_controles.pack(pady=5)

labels = [
    "1ª Faixa",
    "2ª Faixa",
    "Multiplicador",
    "Tolerância"
]
variaveis = [
    var_f1,
    var_f2,
    var_mult,
    var_tol
]
opcoes = [
    list(DIGITOS.keys()),
    list(DIGITOS.keys()),
    list(MULTIPLICADORES.keys()),
    list(TOLERANCIAS.keys())
]

for i in range(4):
    lbl = tk.Label(
        frame_controles,
        text=labels[i],
        font=("Arial", 9, "bold")
    )

    lbl.grid(
        row=i,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    cb = ttk.Combobox(
        frame_controles,
        textvariable=variaveis[i],
        values=opcoes[i],
        state="readonly",
        width=15
    )

    cb.grid(
        row=i,
        column=1,
        padx=10,
        pady=5
    )

# Resultado
lbl_resultado = tk.Label(
    root,
    text="",
    font=("Arial", 16, "bold"),
    fg="#333333"
)
lbl_resultado.pack(pady=15)

# Atualização automática
var_f1.trace_add("write", atualizar_resistor)
var_f2.trace_add("write", atualizar_resistor)
var_mult.trace_add("write", atualizar_resistor)
var_tol.trace_add("write", atualizar_resistor)

# Primeira atualização
atualizar_resistor()

# Iniciar programa
root.mainloop()
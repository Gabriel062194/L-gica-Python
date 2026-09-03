import tkinter as tk
from tkinter import ttk, messagebox

# Tabela de cores (Resistores)
CORES = {
    "Preto":   {"valor": 0, "multiplicador": 1, "hex": "#000000"},
    "Marrom":  {"valor": 1, "multiplicador": 10, "hex": "#8B4513"},
    "Vermelho":{"valor": 2, "multiplicador": 100, "hex": "#FF0000"},
    "Laranja": {"valor": 3, "multiplicador": 1000, "hex": "#FF8C00"},
    "Amarelo": {"valor": 4, "multiplicador": 10000, "hex": "#FFD700"},
    "Verde":   {"valor": 5, "multiplicador": 100000, "hex": "#008000"},
    "Azul":    {"valor": 6, "multiplicador": 1000000, "hex": "#0000FF"},
    "Violeta": {"valor": 7, "multiplicador": 10000000, "hex": "#8A2BE2"},
    "Cinza":   {"valor": 8, "multiplicador": 100000000, "hex": "#808080"},
    "Branco":  {"valor": 9, "multiplicador": 1000000000, "hex": "#FFFFFF"},
}
TOLERANCIAS = {
    "Marrom": {"valor": 1, "texto": "±1%", "hex": "#8B4513"},
    "Vermelho": {"valor": 2, "texto": "±2%", "hex": "#FF0000"},
    "Verde": {"valor": 0.5, "texto": "±0,5%", "hex": "#008000"},
    "Azul": {"valor": 0.25, "texto": "±0,25%", "hex": "#0000FF"},
    "Violeta": {"valor": 0.1, "texto": "±0,1%", "hex": "#8A2BE2"},
    "Cinza": {"valor": 0.05, "texto": "±0,05%", "hex": "#808080"},
    "Dourado": {"valor": 5, "texto": "±5%", "hex": "#D4AF37"},
    "Prata": {"valor": 10, "texto": "±10%", "hex": "#C0C0C0"},
}

              



          
        
           
            
         


# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

def calcular_resistencia(cor1, cor2, cor3, tolerancia):
    """
    Calcula o valor do resistor a partir das quatro faixas.
    As três primeiras faixas representam:
        faixa 1 -> primeiro dígito
        faixa 2 -> segundo dígito
        faixa 3 -> multiplicador
        faixa 4 -> tolerância
    """

    digito1 = CORES[cor1]["valor"]
    digito2 = CORES[cor2]["valor"]
    multiplicador = CORES[cor3]["multiplicador"]

    valor = (digito1 * 10 + digito2) * multiplicador

    return valor


def formatar_resistencia(valor):
    """Converte o valor para Ω, kΩ ou MΩ."""

    if valor >= 1_000_000:
        return f"{valor / 1_000_000:g} MΩ"

    elif valor >= 1_000:
        return f"{valor / 1_000:g} kΩ"

    else:
        return f"{valor:g} Ω"


def valor_para_cores(valor):
    """
    Converte um valor de resistência para as três primeiras
    faixas do resistor.
    """

    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    # Encontramos um multiplicador que permita representar
    # o valor usando exatamente dois dígitos.
    multiplicador = 1

    while valor / multiplicador >= 100:
        multiplicador *= 10

    while valor / multiplicador < 10:
        multiplicador /= 10

    numero = valor / multiplicador

    # O valor precisa ser representável por dois dígitos.
    numero_inteiro = round(numero)

    valor_calculado = numero_inteiro * multiplicador

    if abs(valor_calculado - valor) > 0.000001:
        raise ValueError(
            "O valor informado não pode ser representado "
            "exatamente por um resistor de 4 faixas."
        )

    if numero_inteiro < 10 or numero_inteiro > 99:
        raise ValueError("Valor fora do intervalo permitido.")

    primeiro = numero_inteiro // 10
    segundo = numero_inteiro % 10

    # Descobre as cores correspondentes aos dígitos
    cor1 = None
    cor2 = None
    cor3 = None

    for nome, dados in CORES.items():

        if dados["valor"] == primeiro:
            cor1 = nome

        if dados["valor"] == segundo:
            cor2 = nome

        if dados["multiplicador"] == multiplicador:
            cor3 = nome

    if not cor1 or not cor2 or not cor3:
        raise ValueError(
            "Não foi possível encontrar as cores correspondentes."
        )

    return cor1, cor2, cor3


# ============================================================
# INTERFACE GRÁFICA
# ============================================================

class AplicacaoResistor:

    def __init__(self, root):

        self.root = root
        self.root.title("Calculadora de Resistores")
        self.root.geometry("850x650")
        self.root.resizable(False, False)

        self.modo = tk.StringVar(value="cores")

        self.criar_interface()

        self.atualizar_modo()


    # --------------------------------------------------------
    # INTERFACE PRINCIPAL
    # --------------------------------------------------------

    def criar_interface(self):

        titulo = tk.Label(
            self.root,
            text="Calculadora de Código de Cores de Resistores",
            font=("Arial", 20, "bold"),
            fg="#1f2937"
        )

        titulo.pack(pady=15)

        subtitulo = tk.Label(
            self.root,
            text="Escolha um dos modos para calcular o resistor",
            font=("Arial", 11),
            fg="#555555"
        )

        subtitulo.pack()


        # ====================================================
        # SELEÇÃO DO MODO
        # ====================================================

        frame_modo = tk.LabelFrame(
            self.root,
            text="Modo de operação",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )

        frame_modo.pack(fill="x", padx=30, pady=15)

        tk.Radiobutton(
            frame_modo,
            text="Cores → Valor",
            variable=self.modo,
            value="cores",
            command=self.atualizar_modo,
            font=("Arial", 11)
        ).pack(side="left", padx=30)

        tk.Radiobutton(
            frame_modo,
            text="Valor → Cores",
            variable=self.modo,
            value="valor",
            command=self.atualizar_modo,
            font=("Arial", 11)
        ).pack(side="left", padx=30)


        # ====================================================
        # ÁREA DOS MODOS
        # ====================================================

        self.frame_cores = tk.LabelFrame(
            self.root,
            text="Entrada de cores",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=15
        )

        self.frame_cores.pack(
            fill="x",
            padx=30,
            pady=5
        )


        self.frame_valor = tk.LabelFrame(
            self.root,
            text="Entrada de valor",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=15
        )


        # ----------------------------------------------------
        # MODO CORES → VALOR
        # ----------------------------------------------------

        self.combo_cor1 = self.criar_combo(
            self.frame_cores,
            "1ª faixa:",
            list(CORES.keys())
        )

        self.combo_cor2 = self.criar_combo(
            self.frame_cores,
            "2ª faixa:",
            list(CORES.keys())
        )

        self.combo_cor3 = self.criar_combo(
            self.frame_cores,
            "3ª faixa:",
            list(CORES.keys())
        )

        self.combo_tol = self.criar_combo(
            self.frame_cores,
            "Tolerância:",
            list(TOLERANCIAS.keys())
        )

        self.combo_cor1.current(1)
        self.combo_cor2.current(0)
        self.combo_cor3.current(2)
        self.combo_tol.current(6)


        btn_calcular = tk.Button(
            self.frame_cores,
            text="Calcular resistência",
            command=self.calcular_por_cores,
            bg="#2563eb",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=7,
            cursor="hand2"
        )

        btn_calcular.pack(pady=10)


        # ----------------------------------------------------
        # MODO VALOR → CORES
        # ----------------------------------------------------

        tk.Label(
            self.frame_valor,
            text="Valor da resistência:",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=10, pady=10)

        self.entrada_valor = tk.Entry(
            self.frame_valor,
            font=("Arial", 12),
            width=15
        )

        self.entrada_valor.grid(
            row=0,
            column=1,
            padx=10
        )

        tk.Label(
            self.frame_valor,
            text="Ω",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=2)


        tk.Label(
            self.frame_valor,
            text="Tolerância:",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=10, pady=10)

        self.combo_tol_valor = ttk.Combobox(
            self.frame_valor,
            values=list(TOLERANCIAS.keys()),
            state="readonly",
            width=15
        )

        self.combo_tol_valor.grid(
            row=1,
            column=1,
            padx=10
        )

        self.combo_tol_valor.current(6)


        btn_converter = tk.Button(
            self.frame_valor,
            text="Converter para cores",
            command=self.calcular_por_valor,
            bg="#16a34a",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=7,
            cursor="hand2"
        )

        btn_converter.grid(
            row=2,
            column=0,
            columnspan=3,
            pady=10
        )


        # ====================================================
        # RESULTADO
        # ====================================================

        self.label_resultado = tk.Label(
            self.root,
            text="Resultado aparecerá aqui",
            font=("Arial", 15, "bold"),
            fg="#111827"
        )

        self.label_resultado.pack(pady=12)


        # ====================================================
        # DESENHO DO RESISTOR
        # ====================================================

        frame_desenho = tk.LabelFrame(
            self.root,
            text="Representação visual",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )

        frame_desenho.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )

        self.canvas = tk.Canvas(
            frame_desenho,
            width=750,
            height=180,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack()

        self.desenhar_resistor(
            "Marrom",
            "Preto",
            "Vermelho",
            "Dourado"
        )


    # ========================================================
    # CRIA COMBOBOX
    # ========================================================

    def criar_combo(self, parent, texto, valores):

        frame = tk.Frame(parent)
        frame.pack(side="left", padx=8)

        tk.Label(
            frame,
            text=texto,
            font=("Arial", 10)
        ).pack()

        combo = ttk.Combobox(
            frame,
            values=valores,
            state="readonly",
            width=12
        )

        combo.pack()

        return combo


    # ========================================================
    # ALTERAÇÃO DO MODO
    # ========================================================

    def atualizar_modo(self):

        if self.modo.get() == "cores":

            self.frame_valor.pack_forget()

            if not self.frame_cores.winfo_ismapped():
                self.frame_cores.pack(
                    fill="x",
                    padx=30,
                    pady=5
                )

        else:

            self.frame_cores.pack_forget()

            if not self.frame_valor.winfo_ismapped():
                self.frame_valor.pack(
                    fill="x",
                    padx=30,
                    pady=5
                )

            self.label_resultado.config(
                text="Digite o valor da resistência."
            )


    # ========================================================
    # MODO CORES → VALOR
    # ========================================================

    def calcular_por_cores(self):

        try:

            cor1 = self.combo_cor1.get()
            cor2 = self.combo_cor2.get()
            cor3 = self.combo_cor3.get()
            tolerancia = self.combo_tol.get()

            if not cor1 or not cor2 or not cor3 or not tolerancia:
                messagebox.showwarning(
                    "Atenção",
                    "Selecione todas as cores."
                )
                return

            # A primeira faixa não pode ser preta
            if cor1 == "Preto":
                messagebox.showerror(
                    "Erro",
                    "A primeira faixa não pode ser preta."
                )
                return

            valor = calcular_resistencia(
                cor1,
                cor2,
                cor3,
                tolerancia
            )

            texto_valor = formatar_resistencia(valor)

            self.label_resultado.config(
                text=f"Resistência: {texto_valor}   {TOLERANCIAS[tolerancia]['texto']}",
                fg="#166534"
            )

            self.desenhar_resistor(
                cor1,
                cor2,
                cor3,
                tolerancia
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )


    # ========================================================
    # MODO VALOR → CORES
    # ========================================================

    def calcular_por_valor(self):

        try:

            texto = self.entrada_valor.get().replace(",", ".")

            if not texto:
                messagebox.showwarning(
                    "Atenção",
                    "Digite um valor de resistência."
                )
                return

            valor = float(texto)

            cor1, cor2, cor3 = valor_para_cores(valor)

            tolerancia = self.combo_tol_valor.get()

            if not tolerancia:
                tolerancia = "Dourado"

            self.label_resultado.config(
                text=(
                    f"{formatar_resistencia(valor)} → "
                    f"{cor1} | {cor2} | {cor3} | {tolerancia}"
                ),
                fg="#166534"
            )

            self.desenhar_resistor(
                cor1,
                cor2,
                cor3,
                tolerancia
            )

        except ValueError as erro:

            messagebox.showerror(
                "Valor inválido",
                str(erro)
            )


    # ========================================================
    # DESENHO DO RESISTOR
    # ========================================================

    def desenhar_resistor(
        self,
        cor1,
        cor2,
        cor3,
        tolerancia
    ):

        self.canvas.delete("all")

        # Fios
        self.canvas.create_line(
            50, 90,
            200, 90,
            fill="#555555",
            width=5
        )

        self.canvas.create_line(
            550, 90,
            700, 90,
            fill="#555555",
            width=5
        )


        # Corpo do resistor
        self.canvas.create_rectangle(
            200, 45,
            550, 135,
            fill="#D6B27A",
            outline="#8B7355",
            width=3
        )


        # Bordas arredondadas simuladas
        self.canvas.create_oval(
            180, 45,
            220, 135,
            fill="#D6B27A",
            outline="#8B7355",
            width=3
        )

        self.canvas.create_oval(
            530, 45,
            570, 135,
            fill="#D6B27A",
            outline="#8B7355",
            width=3
        )


        # Faixas
        faixas = [
            (270, cor1),
            (330, cor2),
            (390, cor3),
            (475, tolerancia)
        ]

        for x, cor in faixas:

            if cor in CORES:
                cor_hex = CORES[cor]["hex"]

            else:
                cor_hex = TOLERANCIAS[cor]["hex"]

            self.canvas.create_rectangle(
                x,
                45,
                x + 30,
                135,
                fill=cor_hex,
                outline="#333333"
            )


        # Texto das cores
        self.canvas.create_text(
            350,
            160,
            text=(
                f"{cor1}  |  {cor2}  |  "
                f"{cor3}  |  {tolerancia}"
            ),
            font=("Arial", 11, "bold"),
            fill="#333333"
        )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AplicacaoResistor(root)

    root.mainloop()
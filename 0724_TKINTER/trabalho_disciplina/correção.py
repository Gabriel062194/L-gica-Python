import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# TABELAS DO CÓDIGO DE CORES
# ============================================================

CORES = {
    "Preto": "#000000",
    "Marrom": "#8B4513",
    "Vermelho": "#FF0000",
    "Laranja": "#FF8C00",
    "Amarelo": "#FFD700",
    "Verde": "#008000",
    "Azul": "#0000FF",
    "Violeta": "#8A2BE2",
    "Cinza": "#808080",
    "Branco": "#FFFFFF",
}

DIGITOS = {
    "Preto": 0,
    "Marrom": 1,
    "Vermelho": 2,
    "Laranja": 3,
    "Amarelo": 4,
    "Verde": 5,
    "Azul": 6,
    "Violeta": 7,
    "Cinza": 8,
    "Branco": 9,
}

MULTIPLICADORES = {
    "Preto": 1,
    "Marrom": 10,
    "Vermelho": 100,
    "Laranja": 1_000,
    "Amarelo": 10_000,
    "Verde": 100_000,
    "Azul": 1_000_000,
    "Violeta": 10_000_000,
    "Cinza": 100_000_000,
    "Branco": 1_000_000_000,
    "Dourado": 0.1,
    "Prata": 0.01,
}

TOLERANCIAS = {
    "Marrom": 1,
    "Vermelho": 2,
    "Verde": 0.5,
    "Azul": 0.25,
    "Violeta": 0.1,
    "Cinza": 0.05,
    "Dourado": 5,
    "Prata": 10,
}


# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

def calcular_resistencia(cor1, cor2, cor3):
    """
    Converte as três primeiras faixas em um valor de resistência.
    Exemplo:
        Vermelho, Vermelho, Marrom
        2 2 x 10 = 220 Ω
    """
    valor = (DIGITOS[cor1] * 100 +
             DIGITOS[cor2] * 10 +
             DIGITOS[cor3])

    return valor


def calcular_valor_por_cores(cor1, cor2, cor3):
    """
    Calcula o valor final da resistência a partir das três
    faixas significativas.
    """
    valor_base = calcular_resistencia(cor1, cor2, cor3)

    # A terceira faixa funciona como multiplicador.
    return valor_base * 1


def resistencia_para_cores(valor):
    """
    Converte um valor de resistência para três faixas
    significativas.

    O valor é normalizado para a forma:
        AB x 10^C

    Exemplos:
        3300 -> 33 x 100 -> Laranja, Laranja, Vermelho
        4700 -> 47 x 100 -> Amarelo, Violeta, Vermelho
    """

    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    # Procuramos uma representação com duas casas significativas.
    melhor = None

    for cor1, d1 in DIGITOS.items():
        for cor2, d2 in DIGITOS.items():
            significativos = d1 * 10 + d2

            if significativos == 0:
                continue

            for cor3, multiplicador in MULTIPLICADORES.items():
                calculado = significativos * multiplicador

                if abs(calculado - valor) < 0.000001:
                    return cor1, cor2, cor3

                # Guarda a combinação mais próxima
                erro = abs(calculado - valor)

                if melhor is None or erro < melhor[0]:
                    melhor = (erro, cor1, cor2, cor3)

    raise ValueError(
        "Não foi possível representar esse valor usando "
        "o código de 3 faixas."
    )


def formatar_resistencia(valor):
    """
    Exibe a resistência utilizando Ω, kΩ ou MΩ.
    """

    if valor >= 1_000_000:
        return f"{valor / 1_000_000:g} MΩ"

    if valor >= 1_000:
        return f"{valor / 1_000:g} kΩ"

    return f"{valor:g} Ω"


def encontrar_cor_tolerancia(valor):
    """
    Retorna a cor correspondente à tolerância informada.
    """

    for cor, tolerancia in TOLERANCIAS.items():
        if tolerancia == valor:
            return cor

    raise ValueError("Tolerância inválida.")


# ============================================================
# INTERFACE GRÁFICA
# ============================================================

class AplicacaoResistor:

    def __init__(self, root):
        self.root = root

        self.root.title("Calculadora de Resistores")
        self.root.geometry("850x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#20242a")

        self.modo = tk.StringVar(value="cores")

        self.criar_estilo()
        self.criar_interface()

        self.atualizar_modo()

    # --------------------------------------------------------
    # ESTILO
    # --------------------------------------------------------

    def criar_estilo(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TCombobox",
            fieldbackground="white",
            background="white",
            foreground="black",
            padding=5
        )

        style.configure(
            "TButton",
            font=("Arial", 11, "bold"),
            padding=8
        )

        style.configure(
            "TRadiobutton",
            background="#20242a",
            foreground="white",
            font=("Arial", 11)
        )

    # --------------------------------------------------------
    # INTERFACE
    # --------------------------------------------------------

    def criar_interface(self):

        titulo = tk.Label(
            self.root,
            text="CALCULADORA DE RESISTORES",
            font=("Arial", 22, "bold"),
            bg="#20242a",
            fg="#00d9ff"
        )
        titulo.pack(pady=(20, 5))

        subtitulo = tk.Label(
            self.root,
            text="Código de cores • Cálculo de resistência",
            font=("Arial", 11),
            bg="#20242a",
            fg="#cccccc"
        )
        subtitulo.pack(pady=(0, 15))

        # ----------------------------------------------------
        # ESCOLHA DO MODO
        # ----------------------------------------------------

        frame_modo = tk.Frame(
            self.root,
            bg="#2b3038",
            padx=15,
            pady=10
        )
        frame_modo.pack(fill="x", padx=30)

        tk.Label(
            frame_modo,
            text="Modo de operação:",
            bg="#2b3038",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            frame_modo,
            text="Cores → Valor",
            variable=self.modo,
            value="cores",
            command=self.atualizar_modo
        ).pack(side="left", padx=15)

        ttk.Radiobutton(
            frame_modo,
            text="Valor → Cores",
            variable=self.modo,
            value="valor",
            command=self.atualizar_modo
        ).pack(side="left", padx=15)

        # ----------------------------------------------------
        # ÁREA PRINCIPAL
        # ----------------------------------------------------

        self.frame_principal = tk.Frame(
            self.root,
            bg="#20242a"
        )
        self.frame_principal.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        # Painel esquerdo
        self.frame_controles = tk.Frame(
            self.frame_principal,
            bg="#2b3038",
            width=370
        )
        self.frame_controles.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        # Painel direito
        self.frame_visual = tk.Frame(
            self.frame_principal,
            bg="#2b3038"
        )
        self.frame_visual.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.criar_controles()
        self.criar_resistor()

    # --------------------------------------------------------
    # CONTROLES
    # --------------------------------------------------------

    def criar_controles(self):

        tk.Label(
            self.frame_controles,
            text="ENTRADA",
            font=("Arial", 15, "bold"),
            bg="#2b3038",
            fg="#00d9ff"
        ).pack(pady=(20, 15))

        # Frame que será alterado conforme o modo
        self.frame_cores = tk.Frame(
            self.frame_controles,
            bg="#2b3038"
        )

        self.frame_valor = tk.Frame(
            self.frame_controles,
            bg="#2b3038"
        )

        # ----------------------------------------------------
        # MODO CORES
        # ----------------------------------------------------

        self.combos_cores = []

        nomes = [
            "1ª faixa",
            "2ª faixa",
            "3ª faixa"
        ]

        for nome in nomes:

            linha = tk.Frame(
                self.frame_cores,
                bg="#2b3038"
            )
            linha.pack(fill="x", pady=7, padx=20)

            tk.Label(
                linha,
                text=nome,
                width=12,
                anchor="w",
                bg="#2b3038",
                fg="white",
                font=("Arial", 10)
            ).pack(side="left")

            combo = ttk.Combobox(
                linha,
                values=list(DIGITOS.keys()),
                state="readonly",
                width=15
            )

            combo.pack(side="right")

            combo.bind(
                "<<ComboboxSelected>>",
                lambda event: self.processar_cores()
            )

            self.combos_cores.append(combo)

        # Tolerância
        linha_tol = tk.Frame(
            self.frame_cores,
            bg="#2b3038"
        )
        linha_tol.pack(fill="x", pady=7, padx=20)

        tk.Label(
            linha_tol,
            text="Tolerância",
            width=12,
            anchor="w",
            bg="#2b3038",
            fg="white",
            font=("Arial", 10)
        ).pack(side="left")

        self.combo_tolerancia = ttk.Combobox(
            linha_tol,
            values=[
                "Marrom (±1%)",
                "Vermelho (±2%)",
                "Verde (±0,5%)",
                "Azul (±0,25%)",
                "Violeta (±0,1%)",
                "Cinza (±0,05%)",
                "Dourado (±5%)",
                "Prata (±10%)"
            ],
            state="readonly",
            width=15
        )

        self.combo_tolerancia.pack(side="right")

        self.combo_tolerancia.bind(
            "<<ComboboxSelected>>",
            lambda event: self.processar_cores()
        )

        # ----------------------------------------------------
        # MODO VALOR
        # ----------------------------------------------------

        linha_valor = tk.Frame(
            self.frame_valor,
            bg="#2b3038"
        )
        linha_valor.pack(
            fill="x",
            padx=20,
            pady=(10, 15)
        )

        tk.Label(
            linha_valor,
            text="Resistência:",
            bg="#2b3038",
            fg="white",
            font=("Arial", 10)
        ).pack(anchor="w")

        self.entrada_valor = tk.Entry(
            linha_valor,
            font=("Arial", 12),
            bg="white",
            fg="black"
        )
        self.entrada_valor.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            linha_valor,
            text="Ex.: 3300, 4700, 100000",
            bg="#2b3038",
            fg="#aaaaaa",
            font=("Arial", 9)
        ).pack(anchor="w")

        linha_tol2 = tk.Frame(
            self.frame_valor,
            bg="#2b3038"
        )
        linha_tol2.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            linha_tol2,
            text="Tolerância:",
            bg="#2b3038",
            fg="white",
            font=("Arial", 10)
        ).pack(anchor="w")

        self.combo_tolerancia_valor = ttk.Combobox(
            linha_tol2,
            values=[
                "Marrom (±1%)",
                "Vermelho (±2%)",
                "Verde (±0,5%)",
                "Azul (±0,25%)",
                "Violeta (±0,1%)",
                "Cinza (±0,05%)",
                "Dourado (±5%)",
                "Prata (±10%)"
            ],
            state="readonly",
            width=25
        )

        self.combo_tolerancia_valor.pack(
            fill="x",
            pady=5
        )

        # Botão
        self.botao_calcular = ttk.Button(
            self.frame_valor,
            text="CALCULAR CORES",
            command=self.processar_valor
        )
        self.botao_calcular.pack(
            padx=20,
            pady=15,
            fill="x"
        )

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        self.label_resultado_titulo = tk.Label(
            self.frame_controles,
            text="RESULTADO",
            font=("Arial", 13, "bold"),
            bg="#2b3038",
            fg="#00d9ff"
        )
        self.label_resultado_titulo.pack(pady=(25, 5))

        self.label_resultado = tk.Label(
            self.frame_controles,
            text="Selecione as cores",
            font=("Arial", 18, "bold"),
            bg="#2b3038",
            fg="#00ff88",
            wraplength=320
        )
        self.label_resultado.pack(
            padx=20,
            pady=10
        )

    # --------------------------------------------------------
    # DESENHO DO RESISTOR
    # --------------------------------------------------------

    def criar_resistor(self):

        tk.Label(
            self.frame_visual,
            text="VISUALIZAÇÃO",
            font=("Arial", 15, "bold"),
            bg="#2b3038",
            fg="#00d9ff"
        ).pack(pady=(20, 5))

        self.canvas = tk.Canvas(
            self.frame_visual,
            width=410,
            height=300,
            bg="#2b3038",
            highlightthickness=0
        )
        self.canvas.pack()

        self.desenhar_resistor(
            ["Cinza", "Cinza", "Cinza", "Dourado"]
        )

    def desenhar_resistor(self, cores):

        self.canvas.delete("all")

        # Fios
        self.canvas.create_line(
            30, 150,
            100, 150,
            fill="#bfc4c8",
            width=6
        )

        self.canvas.create_line(
            310, 150,
            380, 150,
            fill="#bfc4c8",
            width=6
        )

        # Corpo
        self.canvas.create_polygon(
            90, 115,
            110, 100,
            300, 100,
            320, 115,
            320, 185,
            300, 200,
            110, 200,
            90, 185,
            fill="#d4b483",
            outline="#8c7352",
            width=2
        )

        # Faixas
        posicoes = [125, 165, 205, 265]

        for i, cor in enumerate(cores):

            if cor not in CORES:
                cor_hex = "#000000"
            else:
                cor_hex = CORES[cor]

            self.canvas.create_rectangle(
                posicoes[i],
                100,
                posicoes[i] + 20,
                200,
                fill=cor_hex,
                outline="#222222",
                width=1
            )

            # Borda branca para o branco ficar visível
            if cor == "Branco":
                self.canvas.create_rectangle(
                    posicoes[i],
                    100,
                    posicoes[i] + 20,
                    200,
                    outline="#555555"
                )

        # Texto
        self.canvas.create_text(
            205,
            245,
            text="1ª   2ª   3ª   T",
            fill="white",
            font=("Arial", 11, "bold")
        )

    # --------------------------------------------------------
    # MUDANÇA DE MODO
    # --------------------------------------------------------

    def atualizar_modo(self):

        if self.modo.get() == "cores":

            self.frame_valor.pack_forget()
            self.frame_cores.pack(fill="x")

            self.label_resultado.config(
                text="Selecione as 4 faixas"
            )

            # Valores iniciais
            if not self.combos_cores[0].get():
                self.combos_cores[0].set("Marrom")

            if not self.combos_cores[1].get():
                self.combos_cores[1].set("Preto")

            if not self.combos_cores[2].get():
                self.combos_cores[2].set("Vermelho")

            if not self.combo_tolerancia.get():
                self.combo_tolerancia.set("Dourado (±5%)")

            self.processar_cores()

        else:

            self.frame_cores.pack_forget()
            self.frame_valor.pack(fill="x")

            self.label_resultado.config(
                text="Informe o valor"
            )

            self.desenhar_resistor(
                ["Cinza", "Cinza", "Cinza", "Dourado"]
            )

    # --------------------------------------------------------
    # CORES -> VALOR
    # --------------------------------------------------------

    def processar_cores(self):

        if self.modo.get() != "cores":
            return

        try:
            cor1 = self.combos_cores[0].get()
            cor2 = self.combos_cores[1].get()
            cor3 = self.combos_cores[2].get()
            tolerancia = self.combo_tolerancia.get()

            if not cor1 or not cor2 or not cor3 or not tolerancia:
                return

            # Para o cálculo das três primeiras faixas:
            # as duas primeiras são dígitos e a terceira é
            # o multiplicador.
            base = DIGITOS[cor1] * 10 + DIGITOS[cor2]
            multiplicador = MULTIPLICADORES[cor3]

            valor = base * multiplicador

            nome_tol = tolerancia.split(" ")[0]
            percentual = TOLERANCIAS[nome_tol]

            resultado = (
                f"{formatar_resistencia(valor)}\n"
                f"±{str(percentual).replace('.', ',')}%"
            )

            self.label_resultado.config(
                text=resultado
            )

            self.desenhar_resistor(
                [cor1, cor2, cor3, nome_tol]
            )

        except (KeyError, ValueError):
            messagebox.showerror(
                "Erro",
                "Verifique as cores selecionadas."
            )

    # --------------------------------------------------------
    # VALOR -> CORES
    # --------------------------------------------------------

    def processar_valor(self):

        if self.modo.get() != "valor":
            return

        try:
            texto = self.entrada_valor.get().strip()

            if not texto:
                raise ValueError

            # Aceita vírgula como separador decimal.
            texto = texto.replace(",", ".")

            valor = float(texto)

            if valor <= 0:
                raise ValueError

            cor1, cor2, cor3 = resistencia_para_cores(valor)

            tolerancia_texto = self.combo_tolerancia_valor.get()

            if not tolerancia_texto:
                tolerancia_texto = "Dourado (±5%)"
                self.combo_tolerancia_valor.set(tolerancia_texto)

            cor_tolerancia = tolerancia_texto.split(" ")[0]

            self.label_resultado.config(
                text=(
                    f"{formatar_resistencia(valor)}\n\n"
                    f"{cor1} - {cor2} - {cor3} - "
                    f"{cor_tolerancia}"
                )
            )

            self.desenhar_resistor(
                [cor1, cor2, cor3, cor_tolerancia]
            )

        except ValueError:
            messagebox.showerror(
                "Valor inválido",
                "Digite um valor de resistência válido.\n\n"
                "Exemplos: 330, 1000, 4700, 100000."
            )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AplicacaoResistor(root)

    root.mainloop()
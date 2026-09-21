import tkinter as tk
from tkinter import ttk, messagebox

# TABELA DO CÓDIGO DAS RESPECTIVAS CORES PARA OS RESISTORES

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
    "Dourado": "#FFD700",
    "Prata": "#C0C0C0"
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

def calcular_valor_por_cores(cor1, cor2, cor3):
    """
    Calcula o valor de um resistor de 3 faixas.

    Exemplo:
        Marrom, Preto, Vermelho

        1 0 × 100
        = 1000 Ω
        = 1 kΩ
    """

    if cor1 not in DIGITOS or cor2 not in DIGITOS:
        raise ValueError("As duas primeiras faixas devem ser cores de dígitos.")

    if cor3 not in MULTIPLICADORES:
        raise ValueError("A terceira faixa deve ser um multiplicador.")

    valor_base = DIGITOS[cor1] * 10 + DIGITOS[cor2]

    if valor_base == 0:
        raise ValueError(
            "As duas primeiras faixas não podem formar o valor 00."
        )

    return valor_base * MULTIPLICADORES[cor3]


def formatar_resistencia(valor):
    """
    Formata a resistência usando Ω, kΩ ou MΩ.
    """

    if valor >= 1_000_000:
        return f"{valor / 1_000_000:g} MΩ"

    if valor >= 1_000:
        return f"{valor / 1_000:g} kΩ"

    return f"{valor:g} Ω"


def resistencia_para_cores(valor):
    """
    Converte uma resistência para três faixas.

    Exemplos:

        100 Ω
        -> Marrom, Preto, Marrom

        3300 Ω
        -> Laranja, Laranja, Vermelho

        4700 Ω
        -> Amarelo, Violeta, Vermelho

        1 MΩ
        -> Marrom, Preto, Azul
    """

    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    # Trabalhamos com valores inteiros quando possível.
    valor_original = valor

    # Procuramos todas as combinações possíveis.
    melhor = None

    for cor1, d1 in DIGITOS.items():

        for cor2, d2 in DIGITOS.items():

            significativos = d1 * 10 + d2

            # 00 não representa um resistor válido.
            if significativos == 0:
                continue

            for cor3, multiplicador in MULTIPLICADORES.items():

                calculado = significativos * multiplicador

                erro = abs(calculado - valor_original)

                if melhor is None or erro < melhor[0]:
                    melhor = (
                        erro,
                        cor1,
                        cor2,
                        cor3,
                        calculado
                    )

                # Correspondência exata.
                if abs(calculado - valor_original) < 1e-9:
                    return cor1, cor2, cor3

    # Permite pequena aproximação para valores que não possuem
    # representação exata com apenas duas casas significativas.
    if melhor is not None:

        erro, cor1, cor2, cor3, calculado = melhor

        # Aceita aproximação de até 1%.
        if erro / valor_original <= 0.01:
            return cor1, cor2, cor3

    raise ValueError(
        f"O valor {valor_original:g} Ω não pode ser representado "
        "adequadamente usando 3 faixas."
    )


def extrair_tolerancia(texto):
    """
    Extrai o nome da cor da tolerância.

    Exemplo:
        'Dourado (±5%)' -> 'Dourado'
    """

    if not texto:
        return None

    return texto.split(" ")[0]


def formatar_tolerancia(percentual):
    """
    Formata a tolerância usando vírgula como separador decimal.
    """

    if float(percentual).is_integer():
        return f"{int(percentual)}%"

    return f"{percentual:g}".replace(".", ",") + "%"


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

    # ========================================================
    # ESTILO
    # ========================================================

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
            background="#2b3038",
            foreground="white",
            font=("Arial", 11)
        )

    # ========================================================
    # INTERFACE
    # ========================================================

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

        frame_modo.pack(
            fill="x",
            padx=30
        )

        tk.Label(
            frame_modo,
            text="Modo de operação:",
            bg="#2b3038",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(
            side="left",
            padx=10
        )

        ttk.Radiobutton(
            frame_modo,
            text="Cores → Valor",
            variable=self.modo,
            value="cores",
            command=self.atualizar_modo
        ).pack(
            side="left",
            padx=15
        )

        ttk.Radiobutton(
            frame_modo,
            text="Valor → Cores",
            variable=self.modo,
            value="valor",
            command=self.atualizar_modo
        ).pack(
            side="left",
            padx=15
        )

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

    # ========================================================
    # CONTROLES
    # ========================================================

    def criar_controles(self):

        tk.Label(
            self.frame_controles,
            text="ENTRADA",
            font=("Arial", 15, "bold"),
            bg="#2b3038",
            fg="#00d9ff"
        ).pack(
            pady=(20, 15)
        )

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

            linha.pack(
                fill="x",
                pady=7,
                padx=20
            )

            tk.Label(
                linha,
                text=nome,
                width=12,
                anchor="w",
                bg="#2b3038",
                fg="white",
                font=("Arial", 10)
            ).pack(
                side="left"
            )

            combo = ttk.Combobox(
                linha,
                values=list(DIGITOS.keys())
                if nome != "3ª faixa"
                else list(MULTIPLICADORES.keys()),
                state="readonly",
                width=15
            )

            combo.pack(side="right")

            combo.bind(
                "<<ComboboxSelected>>",
                lambda event: self.processar_cores()
            )

            self.combos_cores.append(combo)

        # ----------------------------------------------------
        # TOLERÂNCIA
        # ----------------------------------------------------

        linha_tol = tk.Frame(
            self.frame_cores,
            bg="#2b3038"
        )

        linha_tol.pack(
            fill="x",
            pady=7,
            padx=20
        )

        tk.Label(
            linha_tol,
            text="Tolerância",
            width=12,
            anchor="w",
            bg="#2b3038",
            fg="white",
            font=("Arial", 10)
        ).pack(
            side="left"
        )

        valores_tolerancia = [
            "Marrom (±1%)",
            "Vermelho (±2%)",
            "Verde (±0,5%)",
            "Azul (±0,25%)",
            "Violeta (±0,1%)",
            "Cinza (±0,05%)",
            "Dourado (±5%)",
            "Prata (±10%)"
        ]

        self.combo_tolerancia = ttk.Combobox(
            linha_tol,
            values=valores_tolerancia,
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
        ).pack(
            anchor="w"
        )

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
        ).pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # TOLERÂNCIA DO MODO VALOR
        # ----------------------------------------------------

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
        ).pack(
            anchor="w"
        )

        self.combo_tolerancia_valor = ttk.Combobox(
            linha_tol2,
            values=valores_tolerancia,
            state="readonly",
            width=25
        )

        self.combo_tolerancia_valor.pack(
            fill="x",
            pady=5
        )

        # ----------------------------------------------------
        # BOTÃO CALCULAR
        # ----------------------------------------------------

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
        # BOTÃO LIMPAR
        # ----------------------------------------------------

        self.botao_limpar = ttk.Button(
            self.frame_valor,
            text="LIMPAR",
            command=self.limpar
        )

        self.botao_limpar.pack(
            padx=20,
            pady=(0, 10),
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

        self.label_resultado_titulo.pack(
            pady=(25, 5)
        )

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

    # ========================================================
    # DESENHO DO RESISTOR
    # ========================================================

    def criar_resistor(self):

        tk.Label(
            self.frame_visual,
            text="VISUALIZAÇÃO",
            font=("Arial", 15, "bold"),
            bg="#2b3038",
            fg="#00d9ff"
        ).pack(
            pady=(20, 5)
        )

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

        # ----------------------------------------------------
        # FIOS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # CORPO
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # FAIXAS
        # ----------------------------------------------------

        posicoes = [125, 165, 205, 265]

        for i, cor in enumerate(cores):

            cor_hex = CORES.get(
                cor,
                "#000000"
            )

            self.canvas.create_rectangle(
                posicoes[i],
                100,
                posicoes[i] + 20,
                200,
                fill=cor_hex,
                outline="#222222",
                width=1
            )

            # Borda para cores claras

            if cor in ("Branco", "Amarelo", "Dourado", "Prata"):

                self.canvas.create_rectangle(
                    posicoes[i],
                    100,
                    posicoes[i] + 20,
                    200,
                    outline="#555555"
                )

        # ----------------------------------------------------
        # LEGENDA
        # ----------------------------------------------------

        self.canvas.create_text(
            205,
            245,
            text="1ª     2ª     3ª     T",
            fill="white",
            font=("Arial", 11, "bold")
        )

    # ========================================================
    # MUDANÇA DE MODO
    # ========================================================

    def atualizar_modo(self):

        if self.modo.get() == "cores":

            self.frame_valor.pack_forget()

            self.frame_cores.pack(
                fill="x"
            )

            # Valores iniciais

            if not self.combos_cores[0].get():
                self.combos_cores[0].set("Marrom")

            if not self.combos_cores[1].get():
                self.combos_cores[1].set("Preto")

            if not self.combos_cores[2].get():
                self.combos_cores[2].set("Vermelho")

            if not self.combo_tolerancia.get():
                self.combo_tolerancia.set(
                    "Dourado (±5%)"
                )

            self.processar_cores()

        else:

            self.frame_cores.pack_forget()

            self.frame_valor.pack(
                fill="x"
            )

            self.label_resultado.config(
                text="Informe o valor"
            )

            self.desenhar_resistor(
                ["Cinza", "Cinza", "Cinza", "Dourado"]
            )

    # ========================================================
    # CORES → VALOR
    # ========================================================

    def processar_cores(self):

        if self.modo.get() != "cores":
            return

        try:

            cor1 = self.combos_cores[0].get()
            cor2 = self.combos_cores[1].get()
            cor3 = self.combos_cores[2].get()

            tolerancia_texto = self.combo_tolerancia.get()

            if not cor1 or not cor2 or not cor3:
                return

            if not tolerancia_texto:
                return

            valor = calcular_valor_por_cores(
                cor1,
                cor2,
                cor3
            )

            nome_tol = extrair_tolerancia(
                tolerancia_texto
            )

            percentual = TOLERANCIAS[nome_tol]

            valor_minimo = valor * (
                1 - percentual / 100
            )

            valor_maximo = valor * (
                1 + percentual / 100
            )

            resultado = (
                f"{formatar_resistencia(valor)}\n"
                f"±{formatar_tolerancia(percentual)}\n\n"
                f"Faixa: "
                f"{formatar_resistencia(valor_minimo)} "
                f"até "
                f"{formatar_resistencia(valor_maximo)}"
            )

            self.label_resultado.config(
                text=resultado
            )

            self.desenhar_resistor(
                [cor1, cor2, cor3, nome_tol]
            )

        except (KeyError, ValueError) as erro:

            self.label_resultado.config(
                text="Combinação inválida"
            )

    # ========================================================
    # VALOR → CORES
    # ========================================================

    def processar_valor(self):

        if self.modo.get() != "valor":
            return

        try:

            texto = self.entrada_valor.get().strip()

            if not texto:
                raise ValueError(
                    "Digite um valor."
                )

            # Aceita vírgula decimal.

            texto = texto.replace(",", ".")

            # ------------------------------------------------
            # Aceita k e M
            #
            # Exemplos:
            # 4.7k
            # 1k
            # 2.2M
            # ------------------------------------------------

            multiplicador_unidade = 1

            texto_lower = texto.lower()

            if texto_lower.endswith("k"):

                multiplicador_unidade = 1_000
                texto = texto[:-1]

            elif texto_lower.endswith("m"):

                multiplicador_unidade = 1_000_000
                texto = texto[:-1]

            valor = float(texto)

            valor *= multiplicador_unidade

            if valor <= 0:
                raise ValueError

            cor1, cor2, cor3 = resistencia_para_cores(
                valor
            )

            tolerancia_texto = (
                self.combo_tolerancia_valor.get()
            )

            if not tolerancia_texto:

                tolerancia_texto = "Dourado (±5%)"

                self.combo_tolerancia_valor.set(
                    tolerancia_texto
                )

            cor_tolerancia = extrair_tolerancia(
                tolerancia_texto
            )

            percentual = TOLERANCIAS[
                cor_tolerancia
            ]

            resultado = (
                f"{formatar_resistencia(valor)}\n\n"
                f"{cor1} - {cor2} - {cor3}\n"
                f"Tolerância: "
                f"±{formatar_tolerancia(percentual)}"
            )

            self.label_resultado.config(
                text=resultado
            )

            self.desenhar_resistor(
                [
                    cor1,
                    cor2,
                    cor3,
                    cor_tolerancia
                ]
            )

        except (ValueError, OverflowError):

            messagebox.showerror(
                "Valor inválido",
                "Digite um valor de resistência válido.\n\n"
                "Exemplos:\n"
                "330\n"
                "1000\n"
                "4700\n"
                "4,7k\n"
                "1M"
            )

    # ========================================================
    # LIMPAR
    # ========================================================

    def limpar(self):

        self.entrada_valor.delete(
            0,
            tk.END
        )

        self.combo_tolerancia_valor.set(
            "Dourado (±5%)"
        )

        self.label_resultado.config(
            text="Informe o valor"
        )

        self.desenhar_resistor(
            ["Cinza", "Cinza", "Cinza", "Dourado"]
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AplicacaoResistor(root)

    root.mainloop()
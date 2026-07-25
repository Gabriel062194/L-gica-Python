import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("SENAI - Sistemas")
root.geometry("800x600")

minha_imagem = tk.PhotoImage(file="imagens em hd 4k.jfif")

label = tk.Label(root, image=minha_imagem)
label.pack(expand=True)

root.mainloop()
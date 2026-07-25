import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry("400x300")

def button_command():
    messagebox.showinfo(
        "Informação",
        "Você clicou no botão!"
    )
button = tk.Button(
    root,
    text="Clique aqui",
    command=button_command)  

button.pack()
def button2_command():
    messagebox.showinfo(
        "Aviso!",
        "Você clicou no botão 2!"
    )
button2 = tk.Button(
    root,
    text="Clique aqui 2",
    command=button2_command
)
button2.pack()
root.mainloop()
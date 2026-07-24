import tkinter as tk

root = tk.Tk()
root.title("SENAI - Desenvolvimento de Sistemas")


title = root.title()


message = tk.Label(root, text=title)


message.pack()


root.geometry("400x200+50+250")

root.mainloop()
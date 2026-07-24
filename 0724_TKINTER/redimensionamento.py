import tkinter as tk

root = tk.Tk()

root.geometry("400x300")

root.resizable(True, True)

root.minsize(300, 200)
root.maxsize(800, 600)

root.attributes("-alpha", 0.5)
root.mainloop()
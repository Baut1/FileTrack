# imports
from tkinter import *
# ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# import functions/methods
from actions import *

# interfaz grafica
root = ttk.Window(themename="superhero")

def btn_nueva_ventana():
  main_frame = Frame(root)
  main_frame.grid(row=1, column=0, sticky="nsew")
  main_panel = MyMainPanel(root, main_frame)

  # Remove the button after opening the new window
  abrir.destroy()

root.title("Archivos")
root.state('zoomed')

abrir = ttk.Button(root,
                   text="Entrar",
                   cursor="hand2",
                   command=btn_nueva_ventana)
abrir.place(relx=0.5, rely=0.5, anchor='center')

# execute main()
if __name__ == "__main__":
  main()

# tkinter mainloop
root.mainloop()
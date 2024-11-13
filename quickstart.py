# imports
from tkinter import *
# ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# import functions/methods
from actions import *

from datetime import date
today = date.today()

# interfaz grafica
root = ttk.Window(themename="superhero")

def btn_nueva_ventana():
  main_frame = Frame(root)
  main_frame.grid(row=1, column=0, sticky="nsew")
  main_panel = MyMainPanel(root, main_frame)

  # Remove the button after opening the new window
  abrir.destroy()
  label_welcome.destroy()
  label_datetime.destroy()

root.title("Archivos")
root.state('zoomed')

Style = ttk.Style()
Style.configure('Open.TButton', font=('Helvetica', 24))

abrir = ttk.Button(root,
                   text="Entrar",
                   cursor="hand2",
                   command=btn_nueva_ventana,
                   width=8,
                   style="Open.TButton")


label_welcome = ttk.Label(root, text="Bienvenido de vuelta")
label_datetime = ttk.Label(root, text=f'Hoy es: {today}')

abrir.place(relx=0.5, rely=0.5, anchor='center')

label_welcome.place(relx=0.5, rely=0.45, anchor='center')
label_datetime.place(relx=0.5, rely=0.55, anchor='center')

# execute main()
if __name__ == "__main__":
  main()

# tkinter mainloop
root.mainloop()
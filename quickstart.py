# imports
from tkinter import *

# import functions/methods
from actions import *

  # print all rows
  # print_all(values)

  # print specific row
  # print_by_id(values, '3')

  # print_filtered_by_client(values, 'juan')

  # print_filtered_by_model(values, 'iPhone 15')

  # print_filtered_by_date(values, '2024-01-15')

  # print_filtered_by_date_last_ten(values)

  # edit specific row
  # update_by_id(values, 2)

  # add(values)

# interfaz grafica
root = Tk()
root.title("Archivos")
root.geometry("800x500")

def btn_nueva_ventana():
  mainFrame = Frame(root)
  mainFrame.grid(row=1, column=0, padx=10, pady=2)
  mainPanel = MyMainPanel(root, mainFrame)
  abrir.destroy()

abrir = Button(root, text="Abrir", command=btn_nueva_ventana)
abrir.place(relx=0.5, rely=0.5, anchor='center')

# execute main()
if __name__ == "__main__":
  main()

# tkinter mainloop
root.mainloop()
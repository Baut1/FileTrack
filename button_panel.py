import ttkbootstrap as ttk

class ButtonPanel:
    def __init__(self, root, buttons_config, search_entry):
        self.root = root
        self.buttons_config = buttons_config
        self.search_entry = search_entry
        self.create_buttons()

    def create_buttons(self):
        for config in self.buttons_config:
            text, row, column, command, bootstyle = config
            ttk.Button(self.root,
                       text=text,
                       bootstyle=bootstyle,
                       cursor="hand2",
                       command=lambda cmd=command, r=row: cmd(self.root, self.search_entry.get(), r)
                       ).grid(row=0, column=column, padx=1, pady=1)

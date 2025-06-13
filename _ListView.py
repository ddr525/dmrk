import customtkinter
import tksvg
from _EditWindow import *
from functools import partial

class ListView(customtkinter.CTkFrame):
    def __init__(self, master, database, **kwargs):
        super().__init__(master, **kwargs)

        self.database = database

        self.update_list()

        self.toplevel = None
        self.lift()           # Bring window to front
        self.focus_force()    # Focus on this window
        self.grab_set()       # Make modal (optional)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def update_list(self):
        self.clear()

        self.list = self.database.get_gases()

        for row, value in enumerate(self.list):
            list_item = customtkinter.CTkLabel(self, text=value.name, font=customtkinter.CTkFont(size=14, weight="bold"), justify='center', text_color="#ffffff")
            list_item.grid(row=row, column=0, padx=10, pady=10)

            svg_image_edit = tksvg.SvgImage(file="icons/edit_16dp_FFFFFF_FILL1_wght400_GRAD0_opsz20.svg")

            svg_image_close = tksvg.SvgImage(file="icons/close_18dp_5F6368_FILL0_wght700_GRAD200_opsz20.svg")

            button = customtkinter.CTkButton(self, width=20, image=svg_image_edit, text="", fg_color="#4f4f4f", hover_color="gray", command=partial(self.open_edit_menu, value), corner_radius=5)
            button.grid(row=row, column=1, padx=5, pady=10)

            button = customtkinter.CTkButton(self, width=20, image=svg_image_close, text="", fg_color="#4f4f4f", hover_color="gray", command=partial(self.remove_element, value.name), corner_radius=5)
            button.grid(row=row, column=2, padx=(5, 10), pady=10)

        self.add_button = customtkinter.CTkButton(self, text="Добавить газ", command=partial(self.open_edit_menu, None))
        self.add_button.grid(row=len(self.list), column=0, columnspan=3, padx=20, pady=(10, 10))

    def remove_element(self, element_name):
        self.database.remove_gas(element_name)
        self.update_list()

    def open_edit_menu(self, element_name : str | None):
        if(self.toplevel is None or not self.toplevel.winfo_exists()):
            self.toplevel = EditWindow(self, element_name, self.database)
            self.toplevel.after(10, self.toplevel.lift)
        else:
            self.toplevel.focus()

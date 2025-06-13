import customtkinter
from _EditGases import EditGases
from _EditSlabs import EditSlabs
from _EditOtherParams import EditOtherParams

class ParametersListButtons(customtkinter.CTkFrame):
    def __init__(self, master, database, **kwargs): 
        super().__init__(master, **kwargs)
        
        self.master = master

        self.configure(fg_color="#7c7878")
        
        self.font=customtkinter.CTkFont(size=13, weight="bold")

        self.logo_label = customtkinter.CTkLabel(self, text="Задаваемые параметры", font=self.font, text_color="#ffffff", justify="left")
        self.logo_label.grid(row=0, column=0, pady=15)
        self.logo_label.grid_configure(sticky="ew")
        self.grid_columnconfigure(0, weight=1)

        self.button = customtkinter.CTkButton(self, width=170, text="Параметры газов", fg_color="#444242", hover_color="gray", border_color="black", border_width=2, text_color="#ffffff", font=self.font)
        self.button.grid(row=1, column=0, pady=6)
        def open_edit_gases():
            EditGases(self, database)
        self.button.configure(command=open_edit_gases)

        self.button = customtkinter.CTkButton(self, width=170, text="Параметры сляба", fg_color="#444242", hover_color="gray", border_color="black", border_width=2, text_color="#ffffff", font=self.font)
        self.button.grid(row=2, column=0, pady=6)
        def open_edit_slabs():
            EditSlabs(self, database)
        self.button.configure(command=open_edit_slabs)

        self.button = customtkinter.CTkButton(self, width=170, text="Прочие параметры", fg_color="#444242", hover_color="gray", border_color="black", border_width=2, text_color="#ffffff", font=self.font)
        self.button.grid(row=3, column=0, pady=6)
        def open_edit_other():
            EditOtherParams(self, database)
        self.button.configure(command=open_edit_other)
import customtkinter as ctk

from _ListView import * 
from _ParameterList import *

class EditGases(ctk.CTkToplevel):
    def __init__(self, master, database, title="New Window", size="700x500"):
        super().__init__(master)
        self.database = database
        self.title(title)
        self.geometry(size)
        self.init_ui()
        self.grab_set()
        self.transient(self)
        self.focus_force()    # Focus on this window


    def init_ui(self):
        self.logo_label = ctk.CTkLabel(self, text="Редактирование параметров газов", font=ctk.CTkFont(size=17, weight="bold"), text_color="#ffffff")
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=30, pady=(10, 5), sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        self.plist = ParameterList(self, database=self.database)
        self.plist.grid(row=1, column=0, pady=10, padx=50)

        block = ctk.CTkFrame(self)
        block.grid(row=1, column=1, pady=10)
        self.logo_label = customtkinter.CTkLabel(block, text="Переменные расчета", font=customtkinter.CTkFont(size=17, weight="bold"), text_color="#ffffff")
        self.logo_label.grid(row=0, column=0, padx=30, pady=(10, 5))
        self.list = ListView(block, database=self.database)
        self.list.grid(row=1, column=0, pady=10)


    
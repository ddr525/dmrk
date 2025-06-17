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
        
        # Кнопки "Подтвердить" и "Отменить"
        confirm_button = ctk.CTkButton(self, text="Подтвердить", width=160, fg_color='#699187', hover_color='#84a59d', text_color='black',
                                                 font=ctk.CTkFont(size=12, weight="bold"), command=self.confirm)
        confirm_button.grid(row=2, column=0, columnspan=2, pady=20)

        cancel_button = ctk.CTkButton(self, text="Отменить", width=160, fg_color='#ed5855', hover_color='#f28482', text_color='black',
                                                font=ctk.CTkFont(size=12, weight="bold"), command=self.close_window)
        cancel_button.grid(row=2, column=1, columnspan=2, pady=20)


    
    def close_window(self):
        self.destroy()

    def confirm(self):
        data = {}
        try:
            for key, entry in self.text_boxes.items():
                value = entry.get()
                try:
                    data[key] = float(value)
                except ValueError:
                    raise ValueError(f"Значение '{key}' должно быть числом!")


            # Обновляем базу данных параметров печи
            self.database.update_furnace_params(data)

            self.close_window()

        except Exception as ex:
            CTkMessagebox(title="Ошибка!", message=str(ex), icon="cancel")
import customtkinter as ctk

from utilities import toFixed

class EditSlabs(ctk.CTkToplevel):
    def __init__(self, master, database, title="New Window", size="550x300"):
        super().__init__(master)
        self.resizable(False, False)
        self.database = database
        self.title(title)
        self.geometry(size)
        self.furnace_params = {
            "Геометрические параметры": {
                "Толщина сляба (s), м": toFixed(database.get_parameters("Толщина сляба (s)").value, 3),
                "Длина сляба (bb), м": toFixed(database.get_parameters("Длина сляба (bb)").value, 3),
                "Ширина сляба (a), м": toFixed(database.get_parameters("Ширина сляба (a)").value, 3),
                "Начальная температура металла (tmn), °C": toFixed(database.get_parameters("Начальная температура металла (tmn)").value, 3),
                "Марка стали (группа нагрева)": [
                    "DX51D (1)",
                    "08кп, 08пс (1)",
                    "10кп (1)",
                    "3кп,3пс, S235JR (1)",
                    "15 (2)",
                    "20 (2)",
                    "25 (2)",
                    "35 (2)",
                    "45 (3)",
                    "17Г1С4 (3)",
                    "10ХНДП(3)",
                    "09Г2С(38Х2МЮА) (3)",
                ]
            },
        }

        self.init_ui()
        self.lift()           # Bring window to front
        self.focus_force()    # Focus on this window
        self.grab_set()       # Make modal (optional)


    def init_ui(self):
        row_counter = 1
        col_counter = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        geo_label = ctk.CTkLabel(self, text="Редактирование параметров сляба", font=ctk.CTkFont(size=14, weight="bold"))
        geo_label.grid(row=row_counter, column=col_counter, columnspan=2, sticky="NSEW", pady=(10, 5), padx=10)

        row_counter += 1

        for key, value in self.furnace_params["Геометрические параметры"].items():
            list_item = ctk.CTkLabel(self, text=key, font=ctk.CTkFont(size=12))
            list_item.grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="E")

            list_item_text_box = ctk.CTkEntry(self, height=25, width=120)
            list_item_text_box.grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="W")
            list_item_text_box.insert(0, str(value))

            row_counter += 1
            if isinstance(value, list):
                list_item_text_box.destroy()
                combo = ctk.CTkComboBox(self, values=value, width=120)
                combo.grid(row=row_counter - 1, column=col_counter + 1, padx=10, pady=5, sticky="W")
                combo.set(value[0])
                combo.configure(width=200, state="readonly")


    